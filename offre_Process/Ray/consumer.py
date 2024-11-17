import ray 
from kafka import KafkaConsumer
from azure.storage.filedatalake import DataLakeServiceClient
from dotenv import load_dotenv
from groq import Groq
import json
import re
import os
import time

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Variables globales
account_url = os.getenv("AZURE_ACCOUNT_URL")
groq_api_key = os.getenv("GROQ_API_KEY")
kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
kafka_group_id = os.getenv("KAFKA_GROUP_ID")
azure_storage_key = os.getenv("AZURE_STORAGE_KEY")

# Initialiser Ray
ray.init()

# Vérification des variables d'environnement critiques
if not all([account_url, groq_api_key, kafka_bootstrap_servers, kafka_group_id, azure_storage_key]):
    raise ValueError("Une ou plusieurs variables d'environnement sont manquantes.")

# Fonction pour initialiser le client ADLS avec une clé d'accès
def initialize_adls_client():
    try:
        # Vérification de la clé d'accès
        if not azure_storage_key:
            raise ValueError("La clé d'accès (AZURE_STORAGE_KEY) est manquante.")

        # Initialiser le client avec la clé d'accès
        service_client = DataLakeServiceClient(account_url=account_url, credential=azure_storage_key)
        print("Connexion au Data Lake réussie avec la clé d'accès.")
        return service_client
    except Exception as e:
        raise RuntimeError(f"Erreur d'initialisation du client ADLS : {str(e)}")

# Fonction pour uploader le fichier JSON dans ADLS
def upload_to_adls(file_name, content, file_system_name, directory_name):
    try:
        # Vérification et conversion du contenu en chaîne UTF-8
        if isinstance(content, str):
            content_utf8 = content.encode('utf-8')  # Convertir en bytes UTF-8 si c'est déjà une chaîne
        else:
            content_utf8 = content  # Si le contenu est déjà en bytes, pas besoin de conversion
        
        service_client = initialize_adls_client()
        file_system_client = service_client.get_file_system_client(file_system_name)
        directory_client = file_system_client.get_directory_client(directory_name)

        # Créer ou ouvrir le fichier dans ADLS
        file_client = directory_client.create_file(file_name)
        file_client.append_data(data=content_utf8, offset=0, length=len(content_utf8))
        file_client.flush_data(len(content_utf8))

        print(f"Fichier {file_name} envoyé avec succès à ADLS dans {directory_name}.")
    except Exception as e:
        print(f"Erreur lors de l'envoi vers ADLS : {str(e)}")

# Fonction Ray pour extraire les informations d'une offre d'emploi
@ray.remote
def extract_job_info(job_posting_text):
    try:
        # Initialiser le client Groq
        client = Groq(api_key=groq_api_key)

        # Préparer le prompt pour Groq
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

        # Appel de l'API Groq
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": request_content}],
            temperature=0,
            max_tokens=1024,
            top_p=1,
            stream=True,
        )

        # Collecte et traitement de la réponse JSON
        extracted_data = ""
        for chunk in completion:
            extracted_data += chunk.choices[0].delta.content or ""

        # Extraction du JSON du texte brut
        json_match = re.search(r"\{.*\}", extracted_data, re.DOTALL)
        if json_match:
            json_data = json.loads(json_match.group(0))
            return json_data
        else:
            return {"error": "JSON non trouvé dans la sortie."}
    except Exception as e:
        return {"error": f"Erreur lors de l'extraction des données : {str(e)}"}

# Configurer le consommateur Kafka
consumer = KafkaConsumer(
    'offres_travail',
    bootstrap_servers=kafka_bootstrap_servers,
    group_id=kafka_group_id,
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

# Lire les messages Kafka et traiter chaque offre d'emploi

file_system_name = os.getenv("file_system_name")
directory_name = os.getenv("directory_name")

for message in consumer:
    job_posting_text = message.value.decode("utf-8")

    # Envoi du texte de l'offre d'emploi à Ray
    handle = extract_job_info.remote(job_posting_text)
    result = ray.get(handle)

    # Création du nom de fichier avec horodatage
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_file = f"resultat_offre_{timestamp}.json"

    # Conversion des résultats en JSON
    json_content = json.dumps(result, ensure_ascii=False, indent=4)

    # Envoi des résultats à ADLS
    try:
        upload_to_adls(output_file, json_content, file_system_name, directory_name)
    except Exception as e:
        print(f"Erreur d'envoi du fichier {output_file} : {str(e)}")

    print(f"Résultat JSON envoyé à ADLS : {output_file}")
    print(json.dumps(result, indent=4, ensure_ascii=False))
