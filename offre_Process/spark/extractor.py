import os
import time
import json
from typing import List, Optional
from dotenv import load_dotenv
from kafka import KafkaConsumer
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType
from delta.tables import DeltaTable
from extractor import extract_job_info

# Charger les variables d'environnement
load_dotenv()
ADLS_STORAGE_ACCOUNT_NAME = os.getenv("ADLS_STORAGE_ACCOUNT_NAME")
ADLS_ACCOUNT_KEY = os.getenv("ADLS_ACCOUNT_KEY")
ADLS_CONTAINER_NAME = os.getenv("ADLS_CONTAINER_NAME")
ADLS_FOLDER_PATH = os.getenv("ADLS_FOLDER_PATH")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID")

# Configuration Kafka Consumer
consumer = KafkaConsumer(
    'offres_travail',
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    group_id=KAFKA_GROUP_ID,
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

# Configuration Spark
PACKAGES = [
    "io.delta:delta-spark_2.12:3.0.0",
    "org.apache.hadoop:hadoop-azure:3.3.6",
    "org.apache.hadoop:hadoop-azure-datalake:3.3.6",
    "org.apache.hadoop:hadoop-common:3.3.6",
]

OUTPUT_PATH = (
    f"abfss://{ADLS_CONTAINER_NAME}@{ADLS_STORAGE_ACCOUNT_NAME}.dfs.core.windows.net/"
    + ADLS_FOLDER_PATH
)

def create_or_get_spark(app_name: str, packages: List[str]) -> SparkSession:
    jars = ",".join(packages)
    spark = (
        SparkSession.builder.appName(app_name)
        .config("spark.streaming.stopGracefullyOnShutdown", True)
        .config("spark.jars.packages", jars)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .config(
            "fs.abfss.impl", "org.apache.hadoop.fs.azurebfs.SecureAzureBlobFileSystem"
        )
        .getOrCreate()
    )
    return spark

def create_empty_delta_table(spark: SparkSession, schema: StructType, path: str, partition_cols: Optional[List[str]] = None):
    try:
        DeltaTable.forPath(spark, path)
        print(f"Delta Table already exists at path: {path}")
    except Exception:
        custom_builder = (
            DeltaTable.createIfNotExists(spark)
            .location(path)
            .addColumns(schema)
        )
        if partition_cols:
            custom_builder = custom_builder.partitionedBy(partition_cols)
        custom_builder.execute()
        print(f"Delta table created at path: {path}")

def save_to_delta(df: DataFrame, output_path: str):
    df.write.format("delta").mode("append").option("mergeSchema", "true").save(output_path)
    print("Data written to Delta Table")

# Initialiser Spark
spark = create_or_get_spark(app_name="kafka_to_delta", packages=PACKAGES)

# Configurer la connexion Azure
spark.conf.set(
    f"fs.azure.account.key.{ADLS_STORAGE_ACCOUNT_NAME}.dfs.core.windows.net",
    ADLS_ACCOUNT_KEY,
)
print("Spark Session Created")

# Boucle principale pour lire et traiter les messages Kafka
for message in consumer:
    try:
        # Lire le texte de l'offre d'emploi
        job_posting_text = message.value.decode("utf-8")

        # Extraire les informations
        extracted_data = extract_job_info(job_posting_text)

        # Vérifier les erreurs dans l'extraction
        if "error" in extracted_data:
            print(f"Error extracting data: {extracted_data['error']}")
            continue

        # Sauvegarde temporaire au format JSON
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = f"resultat_offre_{timestamp}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(extracted_data, f, ensure_ascii=False, indent=4)

        # Charger les données dans Spark DataFrame
        df = spark.read.json(spark.sparkContext.parallelize([json.dumps(extracted_data)]))

        # Créer une table Delta vide si elle n'existe pas
        create_empty_delta_table(
            spark=spark,
            schema=df.schema,
            path=OUTPUT_PATH,
            partition_cols=["titre_du_poste", "secteur_dactivite"],
        )

        # Sauvegarder dans la table Delta
        save_to_delta(df, OUTPUT_PATH)

    except Exception as e:
        print(f"Error processing message: {e}")
