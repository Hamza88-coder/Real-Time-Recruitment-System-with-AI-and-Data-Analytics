import os
from typing import List, Optional
import pyspark.sql.functions as F
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, ArrayType



# Définir le schéma pour le JSON
PERSON_SCHEMA = StructType([
   
    StructField("last_name", StringType(), True),
    StructField("full_name", StringType(), True),
    StructField("title", StringType(), True),
    StructField("address", StructType([
        StructField("formatted_location", StringType(), True),
        StructField("city", StringType(), True),
        StructField("region", StringType(), True),
        StructField("country", StringType(), True),
        StructField("postal_code", StringType(), True)
    ]), True),
    StructField("objective", StringType(), True),
    StructField("date_of_birth", StringType(), True),
    StructField("place_of_birth", StringType(), True),
    StructField("phones", StringType(), True),
    StructField("urls", StructType([
        StructField("GitHub", StringType(), True),
        StructField("portfolio", StringType(), True),
        StructField("LinkedIn", StringType(), True),
        StructField("site_web", StringType(), True)
    ]), True),
    StructField("gender", StringType(), True),
    StructField("nationality", StringType(), True),
    StructField("education_details", ArrayType(StructType([
        StructField("etude_title", StringType(), True),
        StructField("etablissement_name", StringType(), True),
        StructField("start_date", StringType(), True),
        StructField("end_date", StringType(), True),
        StructField("etude_city", StringType(), True),
        StructField("etude_region", StringType(), True),
        StructField("end_country", StringType(), True)
    ])), True),
    StructField("work_experience_details", ArrayType(StructType([
        StructField("job_title", StringType(), True),
        StructField("company_name", StringType(), True),
        StructField("city", StringType(), True),
        StructField("region", StringType(), True),
        StructField("sector_of_activity", StringType(), True),
        StructField("start_date", StringType(), True),
        StructField("end_date", StringType(), True)
    ])), True),
    StructField("skills", ArrayType(StringType()), True),
    StructField("language", ArrayType(StructType([
        StructField("name", StringType(), True),
        StructField("level", StringType(), True)
    ])), True),
    StructField("certifications", ArrayType(StructType([
        StructField("name", StringType(), True),
        StructField("etablissement_certification", StringType(), True),
        StructField("date", StringType(), True)
    ])), True)
])

# Exemple de données JSON sous forme de variable
data={
    "titre_du_poste": "Stagiaire Data Engineer (PFE)",
    "societe": "DataTech Solutions",
    "competences": [
        "Python",
        "SQL",
        "Apache Airflow",
        "Talend",
        "MongoDB",
        "Cassandra",
        "AWS",
        "Google Cloud"
    ],
    "lieu": "Lyon, France",
    "type_offre": "stage",
    "type_de_contrat": "Stage PFE",
    "durée": "6 mois",
    "email": "contact@datatechsolutions.fr",
    "telephone": "+33 1 23 45 67 89",
    "type": "hybrid",
    "langues": [
    
        "Français"
    ],
    "salaire": "1 200 ",
    "date_de_debut": "15 janvier 2025",
    "secteur_dactivite": "Technologie de l'information",
    "experience_demande": "None",
    "formation_requise": "Étudiant en informatique ou domaine connexe",
    "avantages": [
        "Assurance santé",
        "Opportunités de formation continue"
    ],
    "site_web": "www.datatechsolutions.fr"
}

# ===================================================================================
#       LOAD ENVIRONMENT VARIABLES & SET CONFIGURATIONS
# ===================================================================================
ADLS_STORAGE_ACCOUNT_NAME = "dataoffre"
ADLS_ACCOUNT_KEY = "1eNXm2As1DuaMeSt2Yjegn22fFCvIUa8nBhknayEyTgfBZb6xEEyZhnvl9OiGT7U4O7cFrygjBE/+ASt1hkNQQ=="  # Add your ADLS account key here  # Add your ADLS account key here

ADLS_CONTAINER_NAME = "offres"
ADLS_FOLDER_PATH = "offres_trav"
OUTPUT_PATH = (
    f"abfss://{ADLS_CONTAINER_NAME}@{ADLS_STORAGE_ACCOUNT_NAME}.dfs.core.windows.net/"
    + ADLS_FOLDER_PATH
)

# Required Spark packages
PACKAGES = [
    "io.delta:delta-spark_2.12:3.0.0",
    "org.apache.hadoop:hadoop-azure:3.3.6",
    "org.apache.hadoop:hadoop-azure-datalake:3.3.6",
    "org.apache.hadoop:hadoop-common:3.3.6",
]


def create_or_get_spark(
    app_name: str, packages: List[str], cluster_manager="local[*]"
) -> SparkSession:
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
        .master(cluster_manager)
        .getOrCreate()
    )
    return spark


from pyspark.sql.functions import col, year, month, dayofmonth, hour




def create_empty_delta_table(
    spark: SparkSession,
    schema: StructType,
    path: str,
    partition_cols: Optional[List[str]] = None,
    enable_cdc: Optional[bool] = False,
):
    # Vérifier si la table Delta existe
    try:
        delta_table = DeltaTable.forPath(spark, path)
        print(f"Delta Table already exists at path: {path}")
    except Exception as e:
        print(f"Delta Table does not exist. Creating new table at: {path}")
        custom_builder = (
            DeltaTable.createIfNotExists(spark)
            .location(path)
            .addColumns(schema)
        )
        if partition_cols:
            custom_builder = custom_builder.partitionedBy(partition_cols)
        if enable_cdc:
            custom_builder = custom_builder.property(
                "delta.enableChangeDataFeed", "true"
            )

        custom_builder.execute()
        print(f"Delta table created at path: {path}")


def save_to_delta(df: DataFrame, output_path: str):
    # Sauvegarder les données traitées dans la table Delta avec la fusion de schémas
    df.write.format("delta") \
        .mode("append") \
        .option("mergeSchema", "true") \
        .save(output_path)
    print("Data written to Delta Table")



# ===================================================================================
#                           MAIN ENTRYPOINT
# ===================================================================================

# Créer une session Spark
spark = create_or_get_spark(
    app_name="json_to_delta", packages=PACKAGES, cluster_manager="local[*]"
)

# Configurer la connexion à Azure
spark.conf.set(
    f"fs.azure.account.key.{ADLS_STORAGE_ACCOUNT_NAME}.dfs.core.windows.net",
    ADLS_ACCOUNT_KEY,
)
print("Spark Session Created")

# Lire les données JSON depuis la variable
df = spark.read.json(spark.sparkContext.parallelize([data]), schema=PERSON_SCHEMA)
print("JSON data loaded")

# Traiter les données

print("Data processed")

# Créer une table Delta vide (si elle n'existe pas encore)
create_empty_delta_table(
    spark=spark,
    schema=PERSON_SCHEMA,
    path=OUTPUT_PATH,
    partition_cols=["first_name"],
    enable_cdc=True,
)

# Sauvegarder les données traitées dans la table Delta
save_to_delta(df, OUTPUT_PATH)