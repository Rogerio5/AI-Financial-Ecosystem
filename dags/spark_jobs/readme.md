# 🚀 BankPy — ETL + Spark Integration

## 📌 Fluxo de dados com ETL (Airflow)

```text
Postgres ──► Airflow DAG (etl_clientes_pipeline.py) ──► JSON (/data/transacoes.json) ──► MongoDB ──► Redis
```

O ETL principal é orquestrado pelo Airflow.

Extrai dados do Postgres, transforma em JSON e carrega no MongoDB e Redis

## 📌 Fluxo de dados com Spark

```text
Postgres ──► Airflow ETL ──► JSON (/data/transacoes.json) ──► Spark Job (job_transacoes.py) ──► Agregados (/data/agregados_spark/)
```

O Spark Job lê os dados transformados em JSON.

Realiza agregações distribuídas (soma, média, quantidade de transações por cliente).

Salva os resultados em data/agregados_spark/

## 📌 Integração ETL + Spark

O ETL continua funcionando normalmente via Airflow.

Após gerar o JSON, o Spark é disparado como task adicional ou manualmente.

Assim, o pipeline combina ETL tradicional com Big Data distribuído

Exemplo de integração no DAG:

```bash
from airflow.operators.python import PythonOperator
import subprocess

def run_spark_job():
    subprocess.run("python", "spark_jobs/job_transacoes.py"], check=True)

spark_task = PythonOperator(
    task_id="spark_job_transacoes",
    python_callable=run_spark_job,
    dag=dag,
)

# Dependência: Spark roda depois que o Mongo terminou
load_mongo_task >> spark_task
```

## 🎯 Resultado esperado

Dados extraídos e transformados pelo ETL

Dados carregados em MongoDB e Redis

Spark gera estatísticas avançadas e salva em CSV/Parquet

Projeto demonstra robustez e escalabilidade com Airflow + Spark

---

## ✅ Melhorias aplicadas

Logs estruturados → cada etapa gera mensagens claras com timestamp e nível

Checagem de nulos → identifica registros incompletos.

Validação de saldos → detecta valores negativos em contas e transações

Duplicados → garante que não haja contas ou transações repetidas

---

## 🚀 Benefícios diretos

Rastreabilidade → cada execução deixa registros claros (com hora e nível de severidade), facilitando entender o que aconteceu em caso de falha

Qualidade dos dados → você detecta nulos, duplicados e valores negativos antes de salvar, evitando que dados ruins contaminem os agregados ou modelos de ML

Performance → ao particionar e validar, consultas futuras no Delta Lake ficam mais rápidas e consistentes

Confiabilidade → o pipeline não segue adiante com dados incorretos, reduzindo risco de erros em Superset, Grafana ou relatórios

Escalabilidade → com logs e validações, fica mais fácil rodar em clusters maiores sem perder controle sobre a integridade dos dados

---

## ✅ O que você ganha com isso

Logs estruturados → rastreabilidade clara em cada etapa.

Validação de dados → detecta nulos e negativos antes de salvar.

Confiabilidade → evita que dados ruins contaminem Delta Lake.

Padronização → todos os scripts seguem o mesmo padrão de qualidade.