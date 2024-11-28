from pyspark.sql import SparkSession

# Créer une session Spark
spark = SparkSession.builder \
    .appName("SegmentationCandidats") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
    .getOrCreate()

# Lire les données depuis PostgreSQL
jdbc_url = "jdbc:postgresql://localhost:5433/candidat"
table_name = "personnel"
properties = {
    "user": "postgres",
    "password": "papapapa",
    "driver": "org.postgresql.Driver"
}

df_candidats = spark.read.jdbc(url=jdbc_url, table="personnel", properties=properties)
df_candidats.show()
