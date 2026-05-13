import pandas as pd
import psycopg2, json, datetime, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("MLUtils")

def connect_postgres():
    return psycopg2.connect("dbname=bankpy user=postgres password=123 host=db port=5432")

def save_result(model_name, prediction, customer_id=None):
    conn = connect_postgres()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ml_results (model_name, run_date, customer_id, prediction)
        VALUES (%s, %s, %s, %s)
    """, (model_name, datetime.datetime.now(), customer_id, json.dumps(prediction)))
    conn.commit()
    cur.close()
    conn.close()
    log.info(f"Resultado salvo no Postgres: {model_name}, customer_id={customer_id}")

def load_transactions():
    return pd.read_csv("data/transactions_flat.csv")

def load_clientes():
    return pd.read_csv("data/clientes_flat.csv")
