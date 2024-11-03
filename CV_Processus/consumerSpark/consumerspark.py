from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType, StructType, StructField
import fitz
import yaml
from groq import Groq
import json
import re
from io import BytesIO
from datetime import datetime
import os

# Initialisation de Spark
spark = SparkSession.builder.appName("PDF_Processor").getOrCreate()

# Création du dossier pour les résultats JSON s'il n'existe pas
RESULTS_DIR = "extracted_results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Chargement de la configuration
def load_config():
    CONFIG_PATH = "config.yaml"
    with open(CONFIG_PATH) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        return data['GROQ_API_KEY']

# Fonction d'extraction du texte directement depuis les bytes
def extract_text_from_bytes(pdf_bytes):
    try:
        memory_buffer = BytesIO(pdf_bytes)
        with fitz.open(stream=memory_buffer, filetype="pdf") as doc:
            text = ""
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text += page.get_text("text")
            return text
    except Exception as e:
        return f"Erreur lors de l'extraction du texte: {str(e)}"
    finally:
        memory_buffer.close()

# Fonction d'analyse avec Groq
def ats_extractor(resume_data, api_key):
    prompt = '''
    You are an AI bot designed to act as a professional for parsing resumes. You are given a resume, and your job is to extract the following information:
    1. first name
    2. last name
    1. full name
    4. title
    5. address
    6. objective
    7. date_of_birth
    8. place_of_birth
    9. phones
    10. urls
    11. gender
    12. nationality
    13. education details
    14. total years education
    15. experience details
    16. total years experience
    17. skills
    18. projects
    19. languages
    20. certifications 
    Provide the extracted information in JSON format only,If a field does not exist, do "None".
    Expected example:
    {
  "first_name": "Le prénom du candidat.",
  "last_name": "Le nom de famille du candidat.",
  "full_name": "Le nom complet du candidat (prénom et nom).",
  "title": "Titre professionnel du candidat (ex: Stagiare, Ingénieur, Développeur).",
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
  "phones": "Liste des numéros de téléphone du candidat.",
  "email": "Adresse email principale du candidat.",
  "urls": {
       "GitHub": "Lien vers le profil GitHub du candidat.",
       "portfolio": "Lien vers le portfolio en ligne du candidat.",
       "LinkedIn": "Lien vers le profil LinkedIn du candidat.",
       "site_web": "Lien vers le site web personnel ou professionnel du candidat."
  },
  "gender": "Genre du candidat (ex: masculin, féminin).",
  "nationality": "Nationalité ou citoyenneté du candidat.",
  "education_details": [ (liste des etude de condidat)
    {
      "etude_title": "Titre ou diplôme obtenu (ex: Licence, Master, Doctorat).",
      "etablissement_name": "Nom de l’établissement d’enseignement.",
      "start_date": "Date de début des études (format AAAA-MM-JJ).",
      "end_date": "Date de fin des études ou date prévue de fin (format AAAA-MM-JJ).",
      "etude_city": "Ville où les études ont été effectuées.",
      "etude_region": "Région où les études ont été effectuées.",
      "etude_contry": "Pays où les études ont été effectuées."
    }
  ],
  "total_years_education": "Nombre total d'années de formation du candidat (ex 2.5 ce signifiee 2 annees et demi annee).",
  "work_experience_details": [(liste des experience de condidat)
    {
      "job_title": "Intitulé du poste occupé.",
      "company_name": "Nom de l’entreprise ou de l’organisation.",
      "city": "Ville où l’emploi a été exercé.",
      "region": "Région où l’emploi a été exercé.",
      "sector_of_activity": "Secteur d’activité de l’entreprise.",
      "start_date": "Date de début du poste (format AAAA-MM-JJ).",
      "end_date": "Date de fin du poste ou « actuel » pour les postes en cours."
    }
  ],
  "total_years_work_experience": "Nombre total d'années d’expérience professionnelle.",
  "skills": [
    "Liste des compétences et technologies maitrisées par le candidat (ex: Java, gestion de projet)."
  ],
  "projects":[(liste de projetcs){
      "name":
      "outils":[liste de outils utilisee dans ce projet]
}]
  "language": [
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

    '''
    
    try:
        groq_client = Groq(api_key=api_key)
        messages = [
            {"role": "system", "content": prompt},
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
            return {"error": "JSON non trouvé dans la sortie."}
            
    except Exception as e:
        return {"error": f"Erreur lors de l'analyse: {str(e)}"}

# Fonction pour sauvegarder les résultats en JSON
def save_results_to_json(offset, text, analysis):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{RESULTS_DIR}/resume_analysis_{offset}_{timestamp}.json"
        
        results = {
            "offset": offset,
            "timestamp": timestamp,
            "extracted_text": text,
            "analysis": json.loads(analysis) if isinstance(analysis, str) else analysis
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du fichier JSON: {str(e)}")
        return False

# Chargement de la clé API
api_key = load_config()

# Définition du schéma de sortie
output_schema = StructType([
    StructField("pdf_text", StringType(), True),
    StructField("analysis_result", StringType(), True)
])

# UDF pour le traitement complet
@udf(returnType=output_schema)
def process_pdf_udf(value):
    try:
        # Les données arrivent déjà en bytes depuis Kafka
        pdf_bytes = value
        
        # Extraction du texte directement depuis les bytes
        extracted_text = extract_text_from_bytes(pdf_bytes)
        
        # Analyse avec Groq
        analysis_result = ats_extractor(extracted_text, api_key)
        
        return (extracted_text, json.dumps(analysis_result))
    except Exception as e:
        error_msg = f"Erreur lors du traitement: {str(e)}"
        return (error_msg, json.dumps({"error": error_msg}))

# Fonction de traitement pour chaque micro-batch
def process_batch(df, epoch_id):
    # Conversion du DataFrame en liste de dictionnaires pour traitement
    rows = df.collect()
    for row in rows:
        save_results_to_json(
            row['offset'],
            row['extracted_text'],
            row['analysis_result']
        )

# Lecture du stream Kafka
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "192.168.1.21:29093") \
    .option("subscribe", "TopicCV") \
    .load()

# Application du traitement
processed_df = df.select(
    col("offset"),
    process_pdf_udf(col("value")).alias("processed_data")
)

# Extraction des colonnes du struct retourné par l'UDF
final_df = processed_df.select(
    col("offset"),
    col("processed_data.pdf_text").alias("extracted_text"),
    col("processed_data.analysis_result").alias("analysis_result")
)

# Configuration des streams de sortie
# 1. Console output
console_query = final_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

# 2. Sauvegarde JSON via foreachBatch
json_query = final_df.writeStream \
    .foreachBatch(process_batch) \
    .start()

# Attente de la terminaison des deux streams
spark.streams.awaitAnyTermination()
