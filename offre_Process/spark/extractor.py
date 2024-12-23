import json
import requests
from kafka import KafkaConsumer
from pyspark.sql import SparkSession
from schema import OFFRE_SCHEMA
from dotenv import load_dotenv
load_dotenv()
import os


GROQ_API_URL  = os.getenv("GROQ_API_URL ")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def process_message_groq(message: str):
    """Traite un message et le formate dans le format JSON voulu."""
    try:
        # Envoi du texte à l'API Groq pour extraction des données
        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json',
        }
        payload = {
            'text': message  # Le texte de l'offre que vous envoyez à l'API
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=payload)

        # Vérifiez si la requête a réussi
        if response.status_code == 200:
            job_posting = response.json()

            # Structure des données selon le format souhaité
            formatted_job_posting = {
                "titre_du_poste": job_posting.get("job_title", ""),
                "societe": job_posting.get("company_name", ""),
                "competences": job_posting.get("skills", []),
                "lieu": job_posting.get("location", ""),
                "type_offre": job_posting.get("offer_type", ""),
                "type_de_contrat": job_posting.get("contract_type", ""),
                "durée": job_posting.get("duration", ""),
                "email": job_posting.get("email", ""),
                "telephone": job_posting.get("phone", ""),
                "type": job_posting.get("work_type", ""),
                "langues": job_posting.get("languages", []),
                "salaire": job_posting.get("salary", ""),
                "date_de_debut": job_posting.get("start_date", ""),
                "secteur_dactivite": job_posting.get("industry", ""),
                "experience_demande": job_posting.get("required_experience", ""),
                "formation_requise": job_posting.get("required_education", ""),
                "avantages": job_posting.get("benefits", []),
                "site_web": job_posting.get("website", "")
            }

            # Afficher ou sauvegarder sous le format JSON
            return (json.dumps(formatted_job_posting, indent=4))

        else:
            print(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Error processing message: {e}")
