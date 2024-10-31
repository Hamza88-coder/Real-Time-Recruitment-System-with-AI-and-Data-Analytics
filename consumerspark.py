from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import requests
import json
import io
import config

# Initialiser la session Spark
spark = SparkSession.builder \
    .appName("KafkaSparkConsumer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3") \
    .getOrCreate()

# Configuration de l'API d'EdenAI
API_URL = "https://api.edenai.run/v2/ocr/resume_parser"
HEADERS = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYzZjMTg5YzMtODQ1NS00ZjBiLWI0ZDEtMTRmNDQzNjA0ZTlmIiwidHlwZSI6ImFwaV90b2tlbiJ9._jV9WMpjWlhUXKsOY8YRCmqQTw65fROW8Sj7HYsEaP8'
}

# Fonction pour appeler l'API EdenAI
def parse_resume(content_bytes):
    files = {
        "file": ("resume.pdf", io.BytesIO(content_bytes), "application/pdf")
    }
    
    # Ajouter le paramètre providers requis
    data = {
        "providers": "affinda"  # Vous pouvez aussi utiliser "eden-ai" ou d'autres fournisseurs supportés
    }
    
    response = requests.post(API_URL, headers=HEADERS, data=data, files=files)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erreur dans l'API EdenAI: {response.status_code}, {response.text}")

# Fonction de traitement des micro-lots pour chaque message
def process_batch(df, epoch_id):
    messages = df.collect()
    
    for row in messages:
        try:
            # Obtenir les données PDF depuis Kafka (en bytes)
            pdf_data = row['value']
            
            print(f"Type de données PDF : {type(pdf_data)}")
            print(f"Taille des données PDF : {len(pdf_data)} bytes")
            
            # Appeler l'API EdenAI pour extraire les données du CV
            extraction = parse_resume(pdf_data)
            
            # Convertir les données extraites en JSON structuré
            extraction_json = json.dumps(extraction)
            
            # Créer un DataFrame Spark à partir des données extraites
            extraction_df = spark.read.json(spark.sparkContext.parallelize([extraction_json]))
            
            # Sauvegarder le DataFrame dans un fichier JSON
            extraction_df.write.mode("append").json("extracted_resume_data.json")
            print("Les données extraites sont sauvegardées dans 'extracted_resume_data.json'")
            
        except Exception as e:
            print(f"Erreur lors du traitement du message Kafka : {e}")

# Lire les données de Kafka avec Spark Streaming
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "192.168.0.186:29093") \
    .option("subscribe", config.topic) \
    .option("startingOffsets", "earliest") \
    .load() \
    .selectExpr("CAST(value AS BINARY) as value")

# Appliquer le traitement de chaque batch avec process_batch
query = kafka_df.writeStream \
    .foreachBatch(process_batch) \
    .start()

query.awaitTermination()
