from kafka import KafkaProducer
import json
import random
from time import sleep
import config as cfg




# Compteur global pour les offres
compteur_offres = 0
serveur_kafka=cfg.serveur_kafka
topic=cfg.topic
api_key=cfg.username
api_secret=cfg.password


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
    exemples_cv = [
        "Candidat expert en Python et SQL, avec expérience dans le cloud AWS.",
        "Candidat avec des compétences avancées en Java, Spark, et Hadoop.",
        "Ingénieur logiciel avec 5 ans d'expérience en C++, Docker, et Kubernetes.",
        "Étudiant en data science maîtrisant R, Tableau et machine learning.",
        "Développeur front-end avec expertise en JavaScript, React, et TypeScript."
    ]

    while True:
        try:
            # Génération simulée d'une offre
            resume_data = random.choice(exemples_cv)
            offre = f"Offre générée pour : {resume_data}"
            message = {"offre": offre}

            # Envoi à Kafka
            envoyer_vers_kafka(serveur_kafka, topic, message, api_key, api_secret)

            # Pause pour simuler l'arrivée d'offres
            sleep(random.uniform(0.5, 2.0))

        except KeyboardInterrupt:
            print("\nSimulation interrompue par l'utilisateur.")
            break


# Lancer la simulation

simulation_offres(api_key, api_secret, serveur_kafka, topic)
