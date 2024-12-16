from kafka import KafkaProducer
import json
import random
from time import sleep
import config as cfg

# Compteur global pour les offres
compteur_offres = 0
serveur_kafka = cfg.serveur_kafka
topic = cfg.topic
api_key = cfg.username
api_secret = cfg.password

# Liste d'exemples pour chaque section de l'offre
titres_poste = ["Stagiaire Data Engineer (PFE)", "Data Analyst Junior", "Développeur Backend", "Ingénieur Machine Learning"]
societes = ["DataTech Solutions", "Tech Innovations", "DataWorks", "AlgoConsulting"]
lieux = ["Lyon, France", "Paris, France", "Télétravail", "Marseille, France"]
salaires = [1200, 1500, 1800, 2000]  # en EUR
langues_requises = ["Anglais, Français", "Français", "Anglais"]
formations = ["Étudiant en informatique ou domaine connexe", "Diplômé en ingénierie logicielle", "Master en Data Science"]
competences = [
    "Excellente maîtrise de Python et SQL",
    "Expérience avec des outils ETL comme Apache Airflow ou Talend",
    "Connaissance des bases de données NoSQL (MongoDB, Cassandra)",
    "Familiarité avec les plateformes cloud (AWS, Google Cloud)"
]

def envoyer_vers_kafka(serveur_kafka, topic, message, api_key, api_secret):
    try:
        # Configuration du producteur Kafka avec SASL_SSL
        producer = KafkaProducer(
            bootstrap_servers=[serveur_kafka],
            value_serializer=lambda m: json.dumps(m).encode('utf-8'),
            security_protocol="SASL_SSL",
            sasl_mechanism="PLAIN",
            sasl_plain_username=api_key,
            sasl_plain_password=api_secret,
        )

        # Envoi du message
        producer.send(topic, message)
        producer.flush()  # Assure que le message est bien envoyé
        global compteur_offres
        compteur_offres += 1  # Incrémente le compteur
        print(f"Offre numéro {compteur_offres} envoyée avec succès à Kafka.")
    except Exception as e:
        print(f"Erreur lors de l'envoi à Kafka : {str(e)}")


def simulation_offres(api_key, api_secret, serveur_kafka, topic):
    while True:
        try:
            # Génération simulée d'une offre complète
            offre = {
                "Titre du poste": random.choice(titres_poste),
                "Société": random.choice(societes),
                "Lieu": random.choice(lieux),
                "Type de contrat": "Stage PFE de 6 mois",
                "Description du poste": "Assistance à la conception, à la mise en œuvre et à l'optimisation de pipelines de données.",
                "Compétences requises": random.sample(competences, 3),
                "Email": "contact@domaine.fr",
                "Téléphone": "+33 1 23 45 67 89",
                "Type": "Hybride",
                "Langues requises": random.choice(langues_requises),
                "Salaire": f"{random.choice(salaires)} EUR par mois",
                "Date de début": "15 janvier 2025",
                "Secteur d'activité": "Technologie de l'information",
                "Formation requise": random.choice(formations),
                "Avantages": ["Assurance santé", "Opportunités de formation continue"],
                "Site web": "www.domaine.fr"
            }

            # Envoi de l'offre complète à Kafka
            message = {"offre": offre}
            envoyer_vers_kafka(serveur_kafka, topic, message, api_key, api_secret)

            # Pause pour simuler l'arrivée d'offres
            sleep(random.uniform(0.5, 2.0))

        except KeyboardInterrupt:
            print("\nSimulation interrompue par l'utilisateur.")
            break


# Lancer la simulation
simulation_offres(api_key, api_secret, serveur_kafka, topic)
