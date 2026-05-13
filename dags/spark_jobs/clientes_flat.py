import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count
from pyspark.sql.types import LongType, DoubleType

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("ClientesFlat")

def main():
    spark = SparkSession.builder.appName("BankPyClientesCSV").getOrCreate()

    df = spark.read.csv("/dbfs/FileStore/tables/clientes_flat.csv", header=True, inferSchema=True)
    log.info(f"Total de clientes carregados: {df.count()}")

    df = df.withColumn("id", col("id").cast(LongType())) \
           .withColumn("renda_estimada", col("renda_estimada").cast(DoubleType()))

    # Validação de nulos
    nulls = df.filter(col("id").isNull() | col("nome").isNull()).count()
    log.warning(f"Clientes com nulos: {nulls}")

    agregados = df.groupBy("estado").agg(
        avg("renda_estimada").alias("media_renda"),
        count("*").alias("qtd_clientes")
    )

    agregados.write.format("delta").mode("overwrite").save("/mnt/bankpy/silver/agregados_clientes")
    log.info("Agregados de clientes gravados em Delta Lake")

    spark.stop()

if __name__ == "__main__":
    main()
