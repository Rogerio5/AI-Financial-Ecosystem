import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, avg, count
from pyspark.sql.types import LongType, DoubleType

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("TransacoesFlat")

def main():
    spark = SparkSession.builder.appName("BankPyTransacoesCSV").getOrCreate()

    df = spark.read.csv("/dbfs/FileStore/tables/transactions_flat.csv", header=True, inferSchema=True)
    log.info(f"Total de transações carregadas: {df.count()}")

    df = df.withColumn("owner_cpf", col("owner_cpf").cast(LongType())) \
           .withColumn("amount", col("amount").cast(DoubleType()))

    # Validação de valores negativos
    negativos = df.filter(col("amount") < 0).count()
    saldo_negativo = df.filter(col("balance_after") < 0).count()
    log.warning(f"Transações com valor negativo: {negativos}")
    log.warning(f"Transações com saldo final negativo: {saldo_negativo}")

    agregados = df.groupBy("owner_cpf").agg(
        spark_sum("amount").alias("total_valor"),
        avg("amount").alias("media_valor"),
        count("*").alias("qtd_transacoes")
    )

    agregados.write.format("delta").mode("overwrite").save("/mnt/bankpy/silver/agregados_transacoes")
    log.info("Agregados de transações gravados em Delta Lake")

    spark.stop()

if __name__ == "__main__":
    main()
