import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Configuração de logging estruturado
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("ValidateData")

def main():
    spark = SparkSession.builder.appName("ValidacaoDados").getOrCreate()

    # Caminhos no DBFS
    clientes_path = "/dbfs/FileStore/tables/clientes_flat.csv"
    contas_path = "/dbfs/FileStore/tables/contas_flat.csv"
    transacoes_path = "/dbfs/FileStore/tables/transactions_flat.csv"

    log.info("Iniciando validação dos datasets...")

    # Carregar DataFrames
    clientes_df = spark.read.option("header", "true").option("inferSchema", "true").csv(clientes_path)
    contas_df = spark.read.option("header", "true").option("inferSchema", "true").csv(contas_path)
    transacoes_df = spark.read.option("header", "true").option("inferSchema", "true").csv(transacoes_path)

    # Estatísticas rápidas
    log.info(f"Total de clientes: {clientes_df.count()}")
    log.info(f"Total de contas: {contas_df.count()}")
    log.info(f"Total de transações: {transacoes_df.count()}")

    contas_df.selectExpr("avg(saldo_inicial) as saldo_medio").show()
    transacoes_df.selectExpr("avg(amount) as valor_medio", "avg(balance_after) as saldo_final_medio").show()

    # =========================
    # Validações extras
    # =========================

    # 1) Checar nulos
    clientes_nulls = clientes_df.filter(col("id").isNull() | col("nome").isNull()).count()
    contas_nulls = contas_df.filter(col("account_id").isNull() | col("cliente_id").isNull()).count()
    transacoes_nulls = transacoes_df.filter(col("account_id").isNull() | col("amount").isNull()).count()

    log.warning(f"Clientes com nulos: {clientes_nulls}")
    log.warning(f"Contas com nulos: {contas_nulls}")
    log.warning(f"Transações com nulos: {transacoes_nulls}")

    # 2) Checar saldos e valores negativos
    contas_negativas = contas_df.filter(col("saldo_inicial") < 0).count()
    transacoes_negativas = transacoes_df.filter(col("amount") < 0).count()
    saldo_final_negativo = transacoes_df.filter(col("balance_after") < 0).count()

    log.warning(f"Contas com saldo inicial negativo: {contas_negativas}")
    log.warning(f"Transações com valor negativo: {transacoes_negativas}")
    log.warning(f"Transações com saldo final negativo: {saldo_final_negativo}")

    # 3) Checar duplicados
    contas_duplicadas = contas_df.groupBy("account_id").count().filter(col("count") > 1).count()
    transacoes_duplicadas = transacoes_df.groupBy("id").count().filter(col("count") > 1).count()

    log.warning(f"Contas duplicadas: {contas_duplicadas}")
    log.warning(f"Transações duplicadas: {transacoes_duplicadas}")

    log.info("Validação concluída com sucesso.")

    spark.stop()

if __name__ == "__main__":
    main()
