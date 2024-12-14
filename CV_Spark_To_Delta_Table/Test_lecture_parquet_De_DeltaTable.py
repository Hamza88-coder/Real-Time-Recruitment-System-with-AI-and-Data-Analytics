from pyspark.sql import SparkSession

# Configuration Azure
STORAGE_ACCOUNT_NAME = "a..............."
STORAGE_ACCOUNT_KEY = "b...........................................................="
CONTAINER_NAME = "cv1"
PARQUET_FILE_PATH = "delta-table/part-00000-e8831429-466c-47a9-9517-06aecdc0b839-c000.snappy.parquet"

# Créer la session Spark
spark = SparkSession.builder \
    .appName("Lecture Parquet depuis ADLS") \
    .config(f"fs.azure.account.key.{STORAGE_ACCOUNT_NAME}.dfs.core.windows.net", STORAGE_ACCOUNT_KEY) \
    .getOrCreate()

# Chemin du fichier Parquet
parquet_path = f"abfss://{CONTAINER_NAME}@{STORAGE_ACCOUNT_NAME}.dfs.core.windows.net/{PARQUET_FILE_PATH}"

# Lire les données Parquet
df = spark.read.parquet(parquet_path)

# Afficher un aperçu des données dans le DataFrame
df.show(truncate=False)

# Afficher le schéma pour référence
df.printSchema()

