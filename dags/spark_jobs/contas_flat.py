import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, avg, count
from pyspark.sql.types import LongType, DoubleType

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("ContasFlat")

def main():
    spark = SparkSession.builder.appName("BankPyContasCSV").getOrCreate()

    df = spark.read.csv("/dbfs/FileStore/tables/contas_flat.csv", header=True, inferSchema=True)
    log.info(f"Total de contas carregadas: {df.count()}")

    df = df.withColumn("cliente_id", col("cliente_id").cast(LongType())) \
           .withColumn("saldo_inicial", col("saldo_inicial").cast(DoubleType()))

    # Validação de saldos negativos
    negativos = df.filter(col("saldo_inicial") < 0).count()
    log.warning(f"Contas com saldo inicial negativo: {negativos}")

    agregados = df.groupBy("cliente_id").agg(
        spark_sum("saldo_inicial").alias("total_saldo"),
        avg("saldo_inicial").alias("media_saldo"),
        count("*").alias("qtd_contas")
    )

    agregados.write.format("delta").mode("overwrite").save("/mnt/bankpy/silver/agregados_contas")
    log.info("Agregados de contas gravados em Delta Lake")

    spark.stop()

if __name__ == "__main__":
    main()
