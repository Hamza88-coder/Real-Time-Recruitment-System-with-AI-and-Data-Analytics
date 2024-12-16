import os
import json
import re
from io import BytesIO
from typing import List
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, from_json
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, DoubleType
from delta.tables import DeltaTable
import fitz
from groq import Groq

# ===================================================================================
#       CONFIGURATION
# ===================================================================================
# Azure Data Lake Storage Configuration
STORAGE_ACCOUNT_NAME = "adl............."
STORAGE_ACCOUNT_KEY = "b.................................="
CONTAINER_NAME = "cv1"
DELTA_TABLE_PATH = f"abfss://{CONTAINER_NAME}@{STORAGE_ACCOUNT_NAME}.dfs.core.windows.net/delta-table"

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = "192.168.1.13:29093"
KAFKA_TOPIC = "TopicCV"

# Groq API Key
GROQ_API_KEY = "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"

# Delta Table Schema
PERSON_SCHEMA = StructType([
    StructField("first_name", StringType(), True),
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
    StructField("email", StringType(), True),
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
        StructField("etude_country", StringType(), True)
    ])), True),
    StructField("total_years_education", DoubleType(), True),
    StructField("work_experience_details", ArrayType(StructType([
        StructField("job_title", StringType(), True),
        StructField("company_name", StringType(), True),
        StructField("city", StringType(), True),
        StructField("region", StringType(), True),
        StructField("sector_of_activity", StringType(), True),
        StructField("start_date", StringType(), True),
        StructField("end_date", StringType(), True)
    ])), True),
    StructField("total_years_work_experience", DoubleType(), True),
    StructField("skills", ArrayType(StringType()), True),
    StructField("projects", ArrayType(StructType([
        StructField("name", StringType(), True),
        StructField("outils", ArrayType(StringType()), True)
    ])), True),
    StructField("languages", ArrayType(StructType([
        StructField("name", StringType(), True),
        StructField("level", StringType(), True)
    ])), True),
    StructField("certifications", ArrayType(StructType([
        StructField("name", StringType(), True),
        StructField("etablissement_certification", StringType(), True),
        StructField("date", StringType(), True)
    ])), True)
])

# ===================================================================================
#       SPARK SESSION CREATION
# ===================================================================================
def create_spark_session(app_name: str, packages: List[str]) -> SparkSession:
    jars = ",".join(packages)
    spark = (
        SparkSession.builder.appName(app_name)
        .config("spark.jars.packages", jars)
        .config(f"fs.azure.account.key.{STORAGE_ACCOUNT_NAME}.dfs.core.windows.net", STORAGE_ACCOUNT_KEY)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )
    return spark

spark = create_spark_session("Kafka_to_Delta", [
    "io.delta:delta-spark_2.12:3.0.0",
    "org.apache.hadoop:hadoop-azure:3.3.6",
    "org.apache.hadoop:hadoop-azure-datalake:3.3.6",
    "org.apache.hadoop:hadoop-common:3.3.6"
])

# ===================================================================================
#       FUNCTIONS
# ===================================================================================
# LLM Extraction Prompt
LLM_PROMPT = '''
You are an AI system designed to extract structured information from resumes. 
Extract the following fields strictly following this JSON schema:
{
  "first_name": "Le prénom du candidat.",
  "last_name": "Le nom de famille du candidat.",
  "full_name": "Le nom complet du candidat (prénom et nom).",
  "title": "Titre professionnel du candidat (ex: Stagiaire, Ingénieur, Développeur).",
  "address": {
    "formatted_location": "Adresse complète du candidat au format texte.",
    "city": "Ville de résidence du candidat.",
    "region": "Région de résidence du candidat.",
    "country": "Pays de résidence du candidat.",
    "postal_code": "Code postal de l’adresse du candidat."
  },
  "objective": "Objectif de carrière ou déclaration personnelle du candidat.",
  "date_of_birth": "Date de naissance du candidat (format AAAA-MM-JJ).",
  "place_of_birth": "Lieu de naissance du candidat (ville, région, pays).",
  "phones": "Numéro de téléphone principal du candidat.",
  "email": "Adresse email principale du candidat.",
  "urls": {
    "GitHub": "Lien vers le profil GitHub du candidat.",
    "portfolio": "Lien vers le portfolio en ligne du candidat.",
    "LinkedIn": "Lien vers le profil LinkedIn du candidat.",
    "site_web": "Lien vers le site web personnel ou professionnel du candidat."
  },
  "gender": "Genre du candidat (ex: masculin, féminin, autre).",
  "nationality": "Nationalité ou citoyenneté du candidat.",
  "education_details": [
    {
      "etude_title": "Titre ou diplôme obtenu (ex: Licence, Master, Doctorat).",
      "etablissement_name": "Nom de l’établissement d’enseignement.",
      "start_date": "Date de début des études (format AAAA-MM-JJ).",
      "end_date": "Date de fin des études ou date prévue de fin (format AAAA-MM-JJ).",
      "etude_city": "Ville où les études ont été effectuées.",
      "etude_region": "Région où les études ont été effectuées.",
      "etude_country": "Pays où les études ont été effectuées."
    }
  ],
  "total_years_education": "Nombre total d'années de formation du candidat.",
  "work_experience_details": [
    {
      "job_title": "Intitulé du poste occupé.",
      "company_name": "Nom de l’entreprise ou de l’organisation.",
      "city": "Ville où l’emploi a été exercé.",
      "region": "Région où l’emploi a été exercé.",
      "sector_of_activity": "Secteur d’activité de l’entreprise.",
      "start_date": "Date de début du poste (format AAAA-MM-JJ).",
      "end_date": "Date de fin du poste ou 'actuel' pour les postes en cours."
    }
  ],
  "total_years_work_experience": "Nombre total d'années d’expérience professionnelle.",
  "skills": [
    "Liste des compétences et technologies maitrisées par le candidat (ex: Python, Java, gestion de projet)."
  ],
  "projects": [
    {
      "name": "Nom du projet.",
      "outils": ["Liste des outils utilisés dans le projet (ex: Spark, Power BI)."]
    }
  ],
  "languages": [
    {
      "name": "Nom de la langue parlée (ex: anglais, français).",
      "level": "Niveau de maîtrise de la langue (ex: débutant, intermédiaire, avancé, bilingue)."
    }
  ],
  "certifications": [
    {
      "name": "Nom de la certification obtenue.",
      "etablissement_certification": "Nom de l’organisme délivrant la certification.",
      "date": "Date d’obtention de la certification (format AAAA-MM-JJ)."
    }
  ]
}

If a field does not exist, return "None" for that field. Provide the output strictly in JSON format.
'''

def ats_extractor(resume_data, api_key):
    try:
        groq_client = Groq(api_key=api_key)
        messages = [
            {"role": "system", "content": LLM_PROMPT},
            {"role": "user", "content": resume_data}
        ]
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.0,
            max_tokens=1500
        )
        data = response.choices[0].message.content
        json_match = re.search(r"\{.*\}", data, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        else:
            return {"error": "JSON not found in output."}
    except Exception as e:
        return {"error": f"Extraction error: {e}"}

# PDF Text Extraction
def extract_text_from_bytes(pdf_bytes):
    try:
        memory_buffer = BytesIO(pdf_bytes)
        with fitz.open(stream=memory_buffer, filetype="pdf") as doc:
            text = "".join([page.get_text("text") for page in doc])
            return text
    except Exception as e:
        return f"Error extracting text: {e}"

# UDF to Process PDF Data
@udf(returnType=StringType())
def process_message_udf(value):
    pdf_bytes = value
    text = extract_text_from_bytes(pdf_bytes)
    extracted_data = ats_extractor(text, GROQ_API_KEY)
    return json.dumps(extracted_data)

# Create Delta Table if it Doesn't Exist
def create_delta_table(spark: SparkSession, schema: StructType, path: str):
    try:
        DeltaTable.forPath(spark, path)
    except Exception:
        DeltaTable.createIfNotExists(spark) \
            .location(path) \
            .addColumns(schema) \
            .execute()

# ===================================================================================
#       KAFKA STREAM PROCESSING
# ===================================================================================
create_delta_table(spark, PERSON_SCHEMA, DELTA_TABLE_PATH)

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load()

processed_df = df.selectExpr("CAST(value AS BINARY) as value") \
    .withColumn("processed_data", from_json(process_message_udf(col("value")), PERSON_SCHEMA))

# Forcer la correspondance du schéma
final_df = processed_df.select(
    col("processed_data.first_name").alias("first_name"),
    col("processed_data.last_name").alias("last_name"),
    col("processed_data.full_name").alias("full_name"),
    col("processed_data.title").alias("title"),
    col("processed_data.address").alias("address"),
    col("processed_data.objective").alias("objective"),
    col("processed_data.date_of_birth").alias("date_of_birth"),
    col("processed_data.place_of_birth").alias("place_of_birth"),
    col("processed_data.phones").alias("phones"),
    col("processed_data.email").alias("email"),
    col("processed_data.urls").alias("urls"),
    col("processed_data.gender").alias("gender"),
    col("processed_data.nationality").alias("nationality"),
    col("processed_data.education_details").alias("education_details"),
    col("processed_data.total_years_education").alias("total_years_education"),
    col("processed_data.work_experience_details").alias("work_experience_details"),
    col("processed_data.total_years_work_experience").alias("total_years_work_experience"),
    col("processed_data.skills").alias("skills"),
    col("processed_data.projects").alias("projects"),
    col("processed_data.languages").alias("languages"),
    col("processed_data.certifications").alias("certifications")
)

final_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("path", DELTA_TABLE_PATH) \
    .option("checkpointLocation", f"{DELTA_TABLE_PATH}/_checkpoints") \
    .option("mergeSchema", "true") \
    .start() \
    .awaitTermination()

 

