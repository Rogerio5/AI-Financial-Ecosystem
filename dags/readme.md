# 🚀 BankPy — ETL Pipeline

## 📌 Visão Geral

O projeto **BankPy** possui um pipeline de ETL orquestrado pelo **Airflow**, definido no arquivo `etl_clientes_pipeline.py`.  
Esse fluxo tem como objetivo extrair dados de clientes do Postgres, transformá-los em JSON e carregá-los em diferentes destinos para persistência e cache.

---

## 📂 Estrutura de Diretórios

```BANKPY/
├── dags/
│    └── etl_clientes_pipeline.py
├── data/
│    └── transacoes.json
└── ...
```

---

## 🔄 Fluxo de dados com ETL

```text
Postgres ──► Airflow DAG (etl_clientes_pipeline.py) ──► JSON (/data/transacoes.json) ──► MongoDB ──► Redis
```

## 📌 Etapas do ETL

Extract (Postgres) → consulta clientes no banco relacional.

Transform (JSON) → converte os registros em formato JSON.

Load (MongoDB) → insere os documentos no banco NoSQL.

Load (Redis) → armazena os dados em cache com TTL configurado.

## 🎯 Resultado esperado

Dados extraídos do Postgres.

Dados transformados em JSON.

Documentos persistidos no MongoDB.

Cache atualizado no Redis para consultas rápidas.

Pipeline automatizado e agendado diariamente via Airflow.

---

## robustez, performance e segurança a longo prazo

Constraints evitam dados inválidos (saldo negativo, valores negativos).

Índices aceleram consultas analíticas, especialmente quando você começar a cruzar clientes, contas e transações em relatórios.

Auditoria ajuda a rastrear alterações e dá mais segurança

---

## 📊 Como aplicar a padronização

01
Centralizar funções utilitárias
Mover conexão com Postgres e gravação de resultados para ml_utils.py, evitando duplicação de código.
02
Adicionar logs estruturados
Usar logging em todos os scripts para registrar início, fim, métricas e possíveis erros.
03
Uniformizar formato de resultados
Garantir que todos os modelos gravem em ml_results com os mesmos campos: model_name, run_date, customer_id, prediction.
04
Validar dados antes do treino
Checar nulos, tipos e valores inválidos em cada dataset antes de treinar o modelo.
05
Versionar modelos e parâmetros
Salvar também versão do modelo e hiperparâmetros para auditoria e reprodutibilidade.