import os
import json
from typing import List, Optional

from kafka import KafkaConsumer
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType, ArrayType
from delta.tables import DeltaTable

# Définir le schéma pour le JSON
OFFRE_SCHEMA = StructType([
    StructField("titre_du_poste", StringType(), True),
    StructField("societe", StringType(), True),
    StructField("competences", ArrayType(StringType()), True),
    StructField("lieu", StringType(), True),
    StructField("type_offre", StringType(), True),
    StructField("durée", StringType(), True),
    StructField("type_de_contrat", StringType(), True),
    StructField("email", StringType(), True),
    StructField("telephone", StringType(), True),
    StructField("type", StringType(), True),
    StructField("langues", ArrayType(StringType()), True),
    StructField("salaire", StringType(), True),
    StructField("date_de_debut", StringType(), True),
    StructField("secteur_dactivite", StringType(), True),
    StructField("experience_demande", StringType(), True),
    StructField("formation_requise", StringType(), True),
    StructField("avantages", ArrayType(StringType()), True),
    StructField("site_web", StringType(), True)
])

# Variables d'environnement (à remplacer par des valeurs sécurisées en production)
GROQ_API_KEY = "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"
ADLS_STORAGE_ACCOUNT_NAME = "dataoffre"
ADLS_ACCOUNT_KEY = "1eNXm2As1DuaMeSt2Yjegn22fFCvIUa8nBhknayEyTgfBZb6xEEyZhnvl9OiGT7U4O7cFrygjBE/+ASt1hkNQQ=="  # A remplacer par votre clé
ADLS_CONTAINER_NAME = "postes"
ADLS_FOLDER_PATH = "offres_trav"

KAFKA_BOOTSTRAP_SERVERS = "pkc-619z3.us-east1.gcp.confluent.cloud:9092"
KAFKA_GROUP_ID = "groupe_traitement"
KAFKA_API_KEY = "OM3FCB4RLKF3L2AQ"
KAFKA_API_SECRET = "TaIh3NYZANuLKfatv3dHcQLFaigVQvIdG+uY9Sma/eFIPzMXCWvdojhc6Q1+/BWK"
KAFKA_TOPIC = "offres_trav"

OUTPUT_PATH = f"abfss://{ADLS_CONTAINER_NAME}@{ADLS_STORAGE_ACCOUNT_NAME}.dfs.core.windows.net/{ADLS_FOLDER_PATH}"

# Packages requis pour Spark
PACKAGES = [
    "io.delta:delta-spark_2.12:3.0.0",
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

# Entrée principale
if __name__ == "__main__":
    # Créer une session Spark
    spark = create_or_get_spark("json_to_delta", PACKAGES)
    create_empty_delta_table(spark, OFFRE_SCHEMA, OUTPUT_PATH, partition_cols=["societe"])

    print("Listening to Kafka topic...")
    for message in consumer:
        message_value = message.value.decode("utf-8")
        process_message(spark, message_value)