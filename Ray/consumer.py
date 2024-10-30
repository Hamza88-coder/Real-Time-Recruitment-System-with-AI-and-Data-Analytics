import ray
from kafka import KafkaConsumer
from pydantic import BaseModel, Field
from langchain.llms import BaseLLM
from langchain.prompts import PromptTemplate
from kor import create_extraction_chain, Object, Text
from groq import Groq
import json
import re
import os
import time

# Initialiser Ray
ray.init()

# Définir la fonction Ray pour traiter chaque offre d'emploi
@ray.remote
def extract_job_info(job_posting_text):
    # Initialiser le client Groq ici
    client = Groq(api_key="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")

    request_content = f"""
Veuillez extraire les informations suivantes de l'offre d'emploi et retournez-les strictement au format JSON sans texte supplémentaire. Si un champ n'existe pas, faites "None".

Exemple attendu :
{{
    "titre_du_poste": "Développeur Python",
    "societe": "TechCorp",
    "competences": ["Python", "Django", "API REST"],
    "lieu": "Paris",
    "type_offre": "Ce champ doit être soit 'stage', soit 'offre de travail'. Si vous prédisez qu'il s'agit d'un stage, veuillez préciser son type : 'PFA' ou 'PFE'",
    "durée": "est-ce que le poste indique une durée pour le travail par exemple 'un stage de 3 mois'",
    "type_de_contrat": "CDI",
    "email": "email de l'entreprise ou de recruteur",
    "telephone": "numéro de téléphone de la société ou de recruteur",
    "type": "sur site, à distance ou hybride",
    "langues": ["anglais", "arabe"],
    "salaire": "le montant de la rémunération proposée pour le poste (par exemple, 50 000 EUR par an)",
    "date_de_debut": "la date de début du travail s'il n'est pas déclaré, mettre None",
    "secteur_dactivite": "secteur dans lequel l'entreprise opère",
    "experience_demande": "nombre d'années d'expérience requises",
    "formation_requise": "niveau de formation ou diplômes requis",
    "avantages": ["avantage 1", "avantage 2"],
    "site_web": "URL du site de l'entreprise"
}}

Texte de l'offre d'emploi : {job_posting_text}
"""

    # Appel de l'API Groq pour générer la réponse
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": request_content}],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Collecte et traitement de la réponse JSON
    extracted_data = ""
    for chunk in completion:
        extracted_data += chunk.choices[0].delta.content or ""

    # Extraction du JSON du texte brut
    try:
        json_match = re.search(r"\{.*\}", extracted_data, re.DOTALL)  # Trouver le JSON entre accolades
        if json_match:
            json_data = json.loads(json_match.group(0))  # Charger le JSON
            return json_data
        else:
            return {"error": "JSON non trouvé dans la sortie."}
    except json.JSONDecodeError as e:
        return {"error": f"Erreur de décodage JSON : {e}"}

# Configurer le consommateur Kafka
consumer = KafkaConsumer(
    'offres_travail',
    bootstrap_servers=['localhost:29092'],
    group_id='groupe_traitement'
)

# Lire les messages en continu et les envoyer à Ray pour traitement
for message in consumer:
    # Récupère le texte de l'offre d'emploi
    job_posting_text = message.value.decode("utf-8")

    # Traiter l'offre d'emploi en parallèle
    handle = extract_job_info.remote(job_posting_text)

    # Récupérer le résultat
    result = ray.get(handle)
    
    # Créer un nom de fichier unique basé sur le timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_file = f"resultat_offre_{timestamp}.json"

    # Écrire le résultat dans un fichier JSON séparé
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print(f"Résultat enregistré dans : {output_file}")
    print(json.dumps(result, indent=4, ensure_ascii=False))
