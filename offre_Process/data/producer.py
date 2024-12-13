import re
import json
import random
from kafka import KafkaProducer
from time import sleep
import config as cfg
from offre_Process.spark.gen import serveur_kafka  # Import de la configuration externe pour les paramètres
from notoyage_data.llama_formation_sector import api_key

def generer_offre_emploi(api_key, resume_data):
    try:
        from groq import Groq  # Import du client Groq

        groq_client = Groq(api_key=api_key)

        # Messages pour le modèle
        messages = [
            {
                "role": "system",
                "content": "Tu es un assistant chargé de générer des offres d'emploi basées sur un modèle structuré."
            },
            {
                "role": "user",
                "content": f"""Voici les informations de base d'un candidat :
                {resume_data}
                Génère une offre d'emploi sous un format texte suivant ce modèle :
                Titre du poste : Stagiaire Data Engineer (PFE)
                Société : DataTech Solutions
                Compétences requises : Python, SQL, Apache Airflow, Talend, MongoDB, Cassandra, AWS, Google Cloud
                Lieu : Lyon, France
                Type d'offre : stage
                Type de contrat : Stage PFE
                Durée : 6 mois
                Email : contact@datatechsolutions.fr
                Téléphone : +33 1 23 45 67 89
                Type : Hybride
                Langues requises : Anglais, Français
                Salaire : 1 200 EUR par mois
                Date de début : 15 janvier 2025
                Secteur d'activité : Technologie de l'information
                Expérience demandée : None
                Formation requise : Étudiant en informatique ou domaine connexe
                Avantages : Assurance santé, Opportunités de formation continue
                Site web : www.datatechsolutions.fr
                """
            }
        ]

        # Appel au modèle
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )

        # Extraction du contenu généré
        data = response.choices[0].message.content

        # Vérifier si un texte bien formé est retourné
        if data:
            return data.strip()
        else:
            return "Erreur : Aucune donnée générée."

    except Exception as e:
        return f"Erreur lors de l'analyse : {str(e)}"

def envoyer_vers_kafka(serveur_kafka, topic, message):
    try:
        # Configuration du producteur Kafka
        producer = KafkaProducer(
            bootstrap_servers=[serveur_kafka],
            value_serializer=lambda m: json.dumps(m).encode('utf-8')
        )
        
        # Envoi du message
        producer.send(topic, message)
        producer.flush()  # Assure que le message est bien envoyé
        print("Message envoyé avec succès à Kafka.")
    except Exception as e:
        print(f"Erreur lors de l'envoi à Kafka : {str(e)}")

# Simulation d'offres illimitées
def simulation_offres(api_key, serveur_kafka, topic):
    exemples_cv = [
        "Candidat expert en Python et SQL, avec expérience dans le cloud AWS.",
        "Candidat avec des compétences avancées en Java, Spark, et Hadoop.",
        "Ingénieur logiciel avec 5 ans d'expérience en C++, Docker, et Kubernetes.",
        "Étudiant en data science maîtrisant R, Tableau et machine learning.",
        "Développeur front-end avec expertise en JavaScript, React, et TypeScript."
    ]

    while True:
        try:
            # Choisir aléatoirement un CV
            resume_data = random.choice(exemples_cv)

            # Générer l'offre
            offre = generer_offre_emploi(api_key, resume_data)

            # Vérification et envoi
            if "Erreur" not in offre:
                # Convertir en format JSON
                message = {"offre": offre}
                envoyer_vers_kafka(serveur_kafka, topic, message)
            else:
                print(offre)

            # Pause pour simuler des arrivées d'offres espacées
            sleep(random.uniform(0.5, 2.0))

        except KeyboardInterrupt:
            print("\nSimulation interrompue par l'utilisateur.")
            break
topic = cfg.topic
serveur_kafka=cfg.serveur_kafka
api_key=cfg.api_key

# Lancer la simulation
simulation_offres(api_key, serveur_kafka, topic)
