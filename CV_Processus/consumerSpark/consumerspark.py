import dotenv
import os
import json
from typing import List, Optional
from dotenv import load_dotenv

from kafka import KafkaConsumer
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType, ArrayType
from delta.tables import DeltaTable

from schema import OFFRE_SCHEMA
load_dotenv()



# Variables d'environnement (à remplacer par des valeurs sécurisées en production)
GROQ_API_KEY =os.getenv("GROQ_API_KEY")
ADLS_STORAGE_ACCOUNT_NAME = os.getenv("ADLS_STORAGE_ACCOUNT_NAME")
ADLS_ACCOUNT_KEY = os.getenv("ADLS_ACCOUNT_KEY")  # A remplacer par votre clé
ADLS_CONTAINER_NAME = os.getenv("ADLS_CONTAINER_NAME")
ADLS_FOLDER_PATH = os.getenv("ADLS_FOLDER_PATH")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID")
KAFKA_API_KEY = os.getenv("KAFKA_API_KEY")
KAFKA_API_SECRET = os.getenv("KAFKA_API_SECRET")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC ")

OUTPUT_PATH = f"abfss://{ADLS_CONTAINER_NAME}@{ADLS_STORAGE_ACCOUNT_NAME}.dfs.core.windows.net/{ADLS_FOLDER_PATH}"

# Packages requis pour Spark
PACKAGES = [
    "io.delta:delta-spark_2.12:1.1.0",
    "org.apache.hadoop:hadoop-azure:3.3.6",
    "org.apache.hadoop:hadoop-azure-datalake:3.3.6",
]

def create_or_get_spark(app_name: str, packages: List[str]) -> SparkSession:
    """Créer une session Spark avec Delta et Azure."""
    jars = ",".join(packages)
    spark = (
        SparkSession.builder.appName(app_name)
        .config("spark.jars.packages", jars)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("fs.abfss.impl", "org.apache.hadoop.fs.azurebfs.SecureAzureBlobFileSystem")
        .master("local[*]")
        .getOrCreate()
    )
    spark.conf.set(
        f"fs.azure.account.key.{ADLS_STORAGE_ACCOUNT_NAME}.dfs.core.windows.net",
        ADLS_ACCOUNT_KEY,
    )
    return spark

def create_empty_delta_table(
    spark: SparkSession,
    schema: StructType,
    path: str,
    partition_cols: Optional[List[str]] = None,
    enable_cdc: Optional[bool] = False,
):
    """Créer une table Delta vide si elle n'existe pas."""
    try:
        DeltaTable.forPath(spark, path)
        print(f"Delta Table already exists at path: {path}")
    except Exception:
        print(f"Creating new Delta Table at: {path}")
        custom_builder = DeltaTable.createIfNotExists(spark).location(path).addColumns(schema)
        if partition_cols:
            custom_builder = custom_builder.partitionedBy(partition_cols)
        if enable_cdc:
            custom_builder = custom_builder.property("delta.enableChangeDataFeed", "true")
        custom_builder.execute()

def save_to_delta(df: DataFrame, output_path: str):
    """Sauvegarder les données dans une Delta Table."""
    df.write.format("delta").mode("append").option("mergeSchema", "true").save(output_path)
    print("Data written to Delta Table.")

def process_message(spark: SparkSession, message: str):
    """Traiter un message Kafka et l'enregistrer dans une table Delta."""
    try:
        job_posting = json.loads(message)
        df = spark.createDataFrame([job_posting], schema=OFFRE_SCHEMA)
        save_to_delta(df, OUTPUT_PATH)
    except Exception as e:
        print(f"Error processing message: {e}")

# Configurer le consommateur Kafka pour Confluent
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    group_id=KAFKA_GROUP_ID,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    security_protocol="SASL_SSL",
    sasl_mechanism="PLAIN",
    sasl_plain_username=KAFKA_API_KEY,
    sasl_plain_password=KAFKA_API_SECRET,
)

if __name__ == "__main__":
    # Créer une session Spark
    spark = create_or_get_spark("json_to_delta", PACKAGES)
    
    # Créer une table Delta vide
    create_empty_delta_table(spark, OFFRE_SCHEMA, OUTPUT_PATH, partition_cols=["societe"])
    print("Listening to Kafka topic...")
    
    # Lire les messages de Kafka
    for message in consumer:
        message_value = message.value.decode("utf-8")
        process_message(spark, message_value)
