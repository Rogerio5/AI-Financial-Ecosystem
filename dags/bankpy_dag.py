from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.hooks.base import BaseHook
import logging

log = logging.getLogger(__name__)

default_args = {
    "owner": "rogerio",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
    "email_on_retry": False,
    "email": ["seu_email@gmail.com"]
}

# -----------------------------
# Funções auxiliares
# -----------------------------

def extract_postgres(**kwargs):
    hook = PostgresHook(postgres_conn_id="postgres_default")
    cur = hook.get_conn().cursor()
    cur.execute("SELECT id, nome, email, telefone, cidade, estado, profissao, renda_estimada FROM clientes;")
    rows = cur.fetchall()
    cur.close()
    kwargs["ti"].xcom_push(key="clientes", value=rows)
    return rows

def transform_to_json(**kwargs):
    clientes = kwargs["ti"].xcom_pull(task_ids="extract_postgres", key="clientes")
    clientes_json = [
        {"id": c[0], "nome": c[1], "email": c[2], "telefone": c[3],
         "cidade": c[4], "estado": c[5], "profissao": c[6],
         "renda_estimada": float(c[7]) if c[7] else None}
        for c in clientes
    ]
    kwargs["ti"].xcom_push(key="clientes_json", value=clientes_json)
    return clientes_json

def load_to_mongo(collection, xcom_task, xcom_key):
    def _inner(**kwargs):
        from pymongo import MongoClient
        docs = kwargs["ti"].xcom_pull(task_ids=xcom_task, key=xcom_key) or []
        conn = BaseHook.get_connection("mongo_airflow29")
        uri = f"mongodb://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"
        client = MongoClient(uri, authSource=conn.schema)
        db = client[conn.schema]
        coll = db[collection]
        for doc in docs:
            coll.replace_one({"id": doc.get("id")}, doc, upsert=True)
        client.close()
    return _inner

def load_to_redis(key, xcom_task, xcom_key):
    def _inner(**kwargs):
        import redis, json
        docs = kwargs["ti"].xcom_pull(task_ids=xcom_task, key=xcom_key)
        conn = BaseHook.get_connection("redis_default")
        r = redis.Redis(host=conn.host, port=int(conn.port or 6379), password=conn.password or None)
        r.setex(f"{key}_cache", 3600, json.dumps(docs))
    return _inner

def load_aggregates_postgres():
    import glob, os
    files = sorted(glob.glob("/app/data/agregados_spark/part-*.csv"))
    if not files:
        raise FileNotFoundError("Nenhum CSV encontrado em agregados_spark")
    csv_path = files[-1]
    hook = PostgresHook(postgres_conn_id="postgres_default")
    hook.run("""
        CREATE TABLE IF NOT EXISTS aggregates (
            owner_cpf BIGINT,
            total_valor NUMERIC,
            media_valor NUMERIC,
            qtd_transacoes INT
        );
    """)
    hook.run("TRUNCATE TABLE aggregates;")
    hook.copy_expert(sql="COPY aggregates FROM STDIN WITH (FORMAT csv, DELIMITER ',', HEADER true)", filename=csv_path)

def copy_and_upsert_postgres(**kwargs):
    hook = PostgresHook(postgres_conn_id="postgres_default")
    csv_path = "/opt/airflow/data/transactions_flat.csv"
    hook.run("""
        CREATE TABLE IF NOT EXISTS transacoes_staging (
            id BIGINT,
            account_id TEXT,
            owner_cpf BIGINT,
            date TIMESTAMP,
            type TEXT,
            amount NUMERIC,
            balance_after NUMERIC,
            description TEXT
        );
    """)
    hook.run("TRUNCATE TABLE transacoes_staging;")
    hook.copy_expert(sql="COPY transacoes_staging FROM STDIN WITH CSV HEADER", filename=csv_path)
    upsert_sql = """
    INSERT INTO transacoes (id, account_id, owner_cpf, date, type, amount, balance_after, description)
    SELECT id, account_id, owner_cpf, date, type, amount, balance_after, description
    FROM transacoes_staging
    ON CONFLICT (id) DO UPDATE SET
        account_id = EXCLUDED.account_id,
        owner_cpf = EXCLUDED.owner_cpf,
        date = EXCLUDED.date,
        type = EXCLUDED.type,
        amount = EXCLUDED.amount,
        balance_after = EXCLUDED.balance_after,
        description = EXCLUDED.description;
    """
    hook.run(upsert_sql)
    hook.run("TRUNCATE TABLE transacoes_staging;")

# -----------------------------
# DAG principal
# -----------------------------

with DAG(
    dag_id="bankpy_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 3, 30),
    schedule_interval="@daily",
    catchup=False,
    tags=["bankpy", "spark", "postgres", "mongo", "redis"]
) as dag:

    create_superset = SQLExecuteQueryOperator(
        task_id="create_superset",
        conn_id="postgres_default",
        sql="sql/01-create-superset.sql"
    )

    init_airflow = SQLExecuteQueryOperator(
        task_id="init_airflow",
        conn_id="postgres_default",
        sql="sql/02-init.sql"
    )

    copy_and_upsert = PythonOperator(
        task_id="copy_and_upsert",
        python_callable=copy_and_upsert_postgres
    )

    create_accounts = SQLExecuteQueryOperator(
        task_id="create_accounts",
        conn_id="postgres_default",
        sql="sql/03-create-accounts-and-generate-transacoes.sql"
    )

    extract_clientes = PythonOperator(task_id="extract_postgres", python_callable=extract_postgres)
    transform_clientes = PythonOperator(task_id="transform_to_json", python_callable=transform_to_json)

    load_clientes_mongo = PythonOperator(task_id="load_clientes_mongo", python_callable=load_to_mongo("clientes", "transform_to_json", "clientes_json"))
    load_clientes_redis = PythonOperator(task_id="load_clientes_redis", python_callable=load_to_redis("clientes", "transform_to_json", "clientes_json"))

    spark_job_clientes = SparkSubmitOperator(
        task_id="spark_job_clientes",
        application="/opt/airflow/dags/spark_jobs/clientes_flat.py",
        conn_id="spark_default"
    )

    spark_job_contas = SparkSubmitOperator(
        task_id="spark_job_contas",
        application="/opt/airflow/dags/spark_jobs/contas_flat.py",
        conn_id="spark_default"
    )

    spark_job_transacoes = SparkSubmitOperator(
        task_id="spark_job_transacoes",
        application="/opt/airflow/dags/spark_jobs/transacoes_flat.py",
        conn_id="spark_default"
    )

    check_spark_master = BashOperator(task_id="check_spark_master", bash_command="nc -z spark-master 7077")
    fix_perms = BashOperator(task_id="fix_perms", bash_command="chown -R airflow: /app/data/agregados_spark || true")

    validate_data = SparkSubmitOperator(
        task_id="validate_data",
        application="/opt/airflow/dags/spark_jobs/validate_data.py",
        conn_id="spark_default"
    )

    load_csv = PythonOperator(task_id="load_csv", python_callable=lambda: log.info("Carga CSV original no Postgres"))
    load_aggregates_postgres_task = PythonOperator(task_id="load_aggregates_postgres", python_callable=load_aggregates_postgres)

    saldo_predict = BashOperator(task_id="saldo_predict", bash_command="python /opt/airflow/dags/ml/saldo_predict.py")
    fraude_detect = BashOperator(task_id="fraude_detect", bash_command="python /opt/airflow/dags/ml/fraude_detect.py")
    segmentacao_clientes = BashOperator(task_id="segmentacao_clientes", bash_command="python /opt/airflow/dags/ml/segmentacao_clientes.py")
    recomendacao_produtos = BashOperator(task_id="recomendacao_produtos", bash_command="python /opt/airflow/dags/ml/recomendacao_produtos.py")

    # Dependências
    create_superset >> init_airflow >> copy_and_upsert >> create_accounts
    create_accounts >> extract_clientes >> transform_clientes >> [load_clientes_mongo, load_clientes_redis]

    [load_clientes_mongo, load_clientes_redis] >> check_spark_master >> [spark_job_clientes, spark_job_contas, spark_job_transacoes]

    [spark_job_clientes, spark_job_contas, spark_job_transacoes] >> fix_perms >> validate_data

    validate_data >> [load_csv, load_aggregates_postgres_task]

    # Machine Learning tasks rodam depois da validação
    validate_data >> saldo_predict
    validate_data >> fraude_detect
    validate_data >> segmentacao_clientes
    validate_data >> recomendacao_produtos
