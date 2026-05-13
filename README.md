# Projeto de Pipelines de Dados com Spark e Airflow

## Visão Geral

Este projeto demonstra a construção de pipelines ETL/ELT utilizando **Apache Spark** e **Airflow**, aplicando conceitos da **Medallion Architecture (Bronze, Silver, Gold)** para organização e evolução de um Data Lake.

---

## Estratégia de Ambiente

### Local (Desenvolvimento e Prototipagem)

- Utilizamos **Spark Standalone** em containers Docker (Master + Worker).
- Motivos:
  - Configuração simples e leve.
  - Ideal para validar DAGs e scripts ETL.
  - Permite simular a arquitetura Medallion em pastas locais (`/bronze`, `/silver`, `/gold`).

**Exemplo de DAG com SparkSubmitOperator (local):**

```python
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow import DAG
from datetime import datetime

with DAG(
    dag_id="etl_local_spark",
    start_date=datetime(2026, 3, 13),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    spark_job_transacoes = SparkSubmitOperator(
        task_id="spark_job_transacoes",
        application="/opt/airflow/dags/spark_jobs/transacoes_flat.py",
        conn_id="spark_default",
        verbose=True,
        name="arrow-spark",
    )
```

## Produção (Nuvem)

```text
Em produção, a escolha é diferente:

Databricks é a opção preferencial:

Spark gerenciado (sem necessidade de configurar cluster manualmente).

Integração nativa com cloud (Azure, AWS, GCP).

Suporte direto à Medallion Architecture com Delta Lake.

Ferramentas adicionais para DataOps, observabilidade e MLOps (MLflow).

Spark on Kubernetes também é uma alternativa válida:

Indicado para empresas que já possuem infraestrutura Kubernetes consolidada.

Oferece flexibilidade e controle total sobre configuração e escalabilidade.

Exige maior esforço de engenharia e manutenção.
```

## Exemplo de DAG com DatabricksSubmitRunOperator (produção)

```python
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from airflow import DAG
from datetime import datetime

with DAG(
    dag_id="etl_producao_databricks",
    start_date=datetime(2026, 3, 13),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    spark_job_transacoes = DatabricksSubmitRunOperator(
        task_id="spark_job_transacoes",
        databricks_conn_id="databricks_default",
        existing_cluster_id="cluster-id",
        notebook_task={"notebook_path": "/Repos/projeto/transacoes_flat"},
    )
```

## Como subir o ambiente

1. Certifique-se de ter **Docker** e **Docker Compose** instalados.
2. Crie um arquivo `.env` com as variáveis necessárias (usuário e senha do Postgres, credenciais do Airflow etc.).
3. Suba os containers:

   ```bash
    docker-compose up -
   ```

Verifique se todos os serviços estão rodando:

docker ps

## Acessos principais

Airflow Webserver  
URL: <http://localhost:8080> (localhost in Bing)  
Usuário e senha definidos no .env.

Spark Master UI  
URL: <http://localhost:8080> (localhost in Bing)  
(porta mapeada para o Master).

Spark Worker UI  
URL: <http://localhost:8081> (localhost in Bing)

pgAdmin  
URL: <http://localhost:5050> (localhost in Bing)  
Usuário e senha definidos no .env.

API Python  
URL: <http://localhost:8000> (localhost in Bing)

MongoDB  
Porta: 27017

Redis  
Porta: 6379

## Tecnologias

Tecnologias Utilizadas
Airflow

Apache Spark

Postgres + pgAdmin

MongoDB

Redis

Docker Compose

Python + SQL

Git + CI/CD

Airflow para orquestração de pipelines.

Apache Spark para processamento distribuído.

Docker Compose para ambiente local.

Databricks (produção) ou Spark on Kubernetes (alternativa).

Python e SQL para transformação de dados.

Git + CI/CD para versionamento e automação.

## Arquitetura Medallion

Bronze: dados brutos, ingestão inicial.

Silver: dados limpos e transformados.

Gold: dados prontos para consumo analítico e relatórios.

## tabela aggregates

(.venv) PS C:\Users\roger\bankpy> docker cp "C:\Users\roger\bankpy\data\agregados_spark\part-00000-1fbd50b1-c151-4aa5-9919-30b3fee3f48c-c000.csv" bankpy_db:/tmp/agregados.csv
>>
Successfully copied 2.05kB to bankpy_db:/tmp/agregados.csv
(.venv) PS C:\Users\roger\bankpy> docker exec -it bankpy_db psql -U postgres -d airflow29
>>
psql (15.17 (Debian 15.17-1.pgdg13+1))
Type "help" for help.

airflow29=# \COPY aggregates FROM '/tmp/agregados.csv' DELIMITER ',' CSV;
COPY 2
airflow29=# SELECT * FROM aggregates;
  owner_cpf  | total_valor | media_valor | qtd_transacoes
-------------+-------------+-------------+----------------
 98765432100 |      1100.0 |       220.0 |              5
 12345678901 |      2151.5 |       430.3 |              5
(2 rows)

airflow29=#  = o fluxo manual (Spark → CSV → Postgres)

## Pipeline

esses dois pipelines têm papéis diferentes dentro do seu fluxo de dados:

🔹 etl_clientes_pipeline
Esse é o pipeline mais completo que você montou:

Extract: lê dados de clientes no Postgres.

Transform: converte para JSON.

Load: grava no MongoDB e no Redis.

Spark job: roda o script transacoes_flat.py no cluster Spark para gerar agregados.

Load agregados: carrega os resultados do Spark (CSV) de volta no MongoDB e no Redis.

👉 Em resumo: é um ETL completo de clientes, que integra Postgres → Spark → MongoDB/Redis.

🔹 spark_to_postgres
Esse segundo pipeline é mais simples e focado:

Ele provavelmente roda um job Spark que gera dados transformados e grava diretamente no Postgres.

Serve para cenários em que você quer que o Spark faça o processamento pesado e depois salve o resultado em tabelas relacionais (Postgres), em vez de mandar para Mongo/Redis.

É útil para relatórios, dashboards ou quando você precisa que os dados fiquem disponíveis em SQL.

👉 Em resumo: é um pipeline de integração Spark → Postgres, mais direto e voltado para persistir resultados processados no banco relacional.

✅ Então:

etl_clientes_pipeline = fluxo completo de ETL de clientes, com múltiplos destinos (Mongo + Redis).

spark_to_postgres = fluxo específico para gravar resultados do Spark direto no Postgres.

## Objetivo do spark_to_postgres

Esse pipeline é focado em usar o Spark para processar dados e gravar diretamente no Postgres.
Enquanto o etl_clientes_pipeline distribui os resultados para MongoDB e Redis, o spark_to_postgres mantém tudo dentro do banco relacional.

🔹 Estrutura típica da DAG
O código dessa DAG geralmente tem:

Um SparkSubmitOperator que dispara um job Spark (application=/opt/airflow/dags/spark_jobs/...).

Esse job Spark lê dados brutos (CSV, JSON ou tabelas do Postgres), faz transformações (agregações, joins, limpeza) e gera resultados.

Ao final, o Spark grava os resultados diretamente em uma tabela do Postgres usando o JDBC connector (spark.write.format("jdbc")...).

🔹 Para que serve
Centralizar resultados no Postgres: ideal para relatórios, dashboards e consultas SQL.

Evitar múltiplos destinos: diferente do etl_clientes_pipeline, que espalha dados em Mongo e Redis, aqui o foco é só Postgres.

Simplificar integração: muitos sistemas corporativos já consomem dados direto de Postgres, então esse pipeline facilita.

🔹 Exemplo de fluxo
Spark lê transações de clientes (CSV ou Postgres).

Spark calcula agregados (ex: total gasto por cliente, número de compras).

Spark grava os resultados em uma tabela clientes_agregados no Postgres.

Airflow marca a DAG como concluída.

✅ Em resumo:

etl_clientes_pipeline → ETL completo, integrando Postgres → Spark → MongoDB/Redis.

spark_to_postgres → pipeline direto, Spark processa e grava no Postgres para uso em relatórios/SQL.

## pitch

Localmente eu uso Spark Standalone para prototipar.
Em produção, eu levaria para nuvem usando Databricks, porque ele oferece Spark gerenciado, integração com cloud e suporte nativo à Medallion Architecture.
Se a empresa já tiver Kubernetes consolidado, Spark on K8s também é uma opção, mas Databricks acelera muito a entrega de valor

## Docker-compose.yml

👉 Com esse ajuste, você tem um ambiente completo:

Banco relacional (Postgres + pgAdmin).

NoSQL (MongoDB, Redis).

Orquestração (Airflow).

Processamento distribuído (Spark Master + Worker).

API Python integrada

## 🔹 Infraestrutura com Docker

Criou um docker-compose.yml robusto com múltiplos serviços:

Postgres como banco relacional principal.

PgAdmin para gerenciar o Postgres via interface web.

MongoDB como banco NoSQL.

Redis como cache e armazenamento rápido.

Airflow (init, webserver, scheduler, triggerer) para orquestração de pipelines.

Spark Master e Worker para processamento distribuído.

Configurou volumes e redes para que todos os serviços compartilhem dados e consigam se comunicar.

Ajustou os volumes para que Airflow e Spark enxerguem os mesmos diretórios (/opt/airflow/data e /opt/airflow/dags).

🔹 Configuração do Airflow
Criou conexões automáticas no airflow-init para Postgres, MongoDB e Redis.

Configurou o scheduler e o webserver para rodar corretamente.

Criou e logou com usuário admin no Airflow Webserver.

🔹 Pipelines (DAGs)
etl_clientes_pipeline

Extrai clientes do Postgres.

Transforma em JSON.

Carrega em MongoDB e Redis.

Dispara um job Spark (transacoes_flat.py) para gerar agregados.

Carrega os agregados de volta em MongoDB e Redis.
➝ É o seu ETL completo de clientes.

spark_to_postgres

Pipeline focado em rodar Spark e gravar resultados diretamente no Postgres.
➝ Útil para relatórios e consultas SQL.

🔹 Testes e Validações
Subiu os containers e verificou que o Spark Master e Worker estão vivos.

Ajustou o deploy-mode do SparkSubmitOperator para cluster, garantindo que o driver rode dentro do cluster Spark.

Validou que o Airflow Scheduler voltou a rodar e está processando DAGs.

Já consegue ver suas DAGs listadas na UI do Airflow (etl_clientes_pipeline e spark_to_postgres).

✅ Em resumo: você já montou toda a infraestrutura de dados (Postgres, Mongo, Redis, Spark, Airflow), configurou conexões, criou usuários, e desenvolveu dois pipelines ETL que integram esses sistemas

##

 O erro nos logs (Invalid arguments: {'master': 'spark://spark-master:7077'}) indica que o SparkSubmitOperator está recebendo um kwarg master que a versão do provider não aceita. A solução mais direta e segura agora é remover conn_id="spark_default" (ou qualquer master= explícito) e passar o endereço do master apenas via conf={"spark.master": "..."} no operador. Vou te dar o patch exato e os comandos para aplicar, recarregar o scheduler e testar o job.
Resumo curto
Sim — o Spark gerou os artefatos: _SUCCESS e part-*.csv em /opt/airflow/data/agregados_spark. Isso significa que o job Spark foi executado com sucesso fora (ou independentemente) do registro de sucesso do Airflow. A task do Airflow ficou failed, então o próximo passo é carregar os CSVs no Postgres e, se quiser, investigar por que o Airflow marcou a task como falha.

Situação atual — conclusão curta
Você confirmou que o Spark executou e completou (logs mostram jobs finalizados e a tabela agregada), mas não há arquivos part-*.csv em /opt/airflow/data/agregados_spark. O mount está correto (scheduler e worker veem ./data), então o problema não é volume — é onde o job gravou ou se o commit final não moveu os arquivos para o diretório final.

O que os resultados que você mostrou significam
Mounts OK — C:\Users\roger\bankpy\data -> /opt/airflow/data aparece em ambos os containers.

Touch OK — test_from_scheduler criado no scheduler aparece também no worker.

Spark job rodou — logs mostram FileOutputCommitter e Job finished e a tabela de agregados impressa.

Saída ausente — /opt/airflow/data/agregados_spark existe, mas está vazio (nenhum part-*.csv), e não há_temporary visível. Isso indica que o job não deixou arquivos finais no diretório esperado.

Possíveis causas mais prováveis
O job gravou em outro caminho (ex.: spark-warehouse, outro parâmetro --output, ou caminho relativo).

Os arquivos ficaram em _temporary e não foram renomeados/committed (commit falhou silenciosamente).

O job escreveu localmente no executor e depois não moveu para o volume (menos provável aqui, já que o worker tem o mount).

O código Spark usa um caminho dinâmico diferente do que você acha (parâmetro --output não foi passado ou ignorado).
