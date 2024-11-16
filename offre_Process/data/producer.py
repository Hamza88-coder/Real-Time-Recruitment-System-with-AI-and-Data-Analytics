text="""
Titre du poste : Stagiaire Data Engineer (PFE)
Société : DataTech Solutions
Lieu : Lyon, France (Télétravail partiel possible)
Type de contrat : Stage PFE de 6 mois

Description du poste :
DataTech Solutions recherche un stagiaire Data Engineer passionné pour rejoindre notre équipe dynamique. Vous serez responsable de l'assistance à la conception, à la mise en œuvre et à l'optimisation de nos pipelines de données. Votre mission consistera à collaborer avec les équipes de développement et d'analytique pour garantir l'intégrité et l'accessibilité des données.

Compétences requises :

Excellente maîtrise de Python et SQL
Expérience avec des outils ETL comme Apache Airflow ou Talend (souhaitée)
Connaissance des bases de données NoSQL (MongoDB, Cassandra) (souhaitée)
Familiarité avec les plateformes cloud (AWS, Google Cloud) (souhaitée)
Email : contact@datatechsolutions.fr
Téléphone : +33 1 23 45 67 89
Type : Hybride
Langues requises : Anglais, Français
Salaire : 1 200 EUR par mois
Date de début : 15 janvier 2025
Secteur d'activité : Technologie de l'information
Formation requise : Étudiant en informatique ou domaine connexe

Avantages :

Assurance santé
Opportunités de formation continue
Site web : www.datatechsolutions.fr

"""

import time
from kafka import KafkaProducer  # Import du producteur Kafka pour envoyer des messages
import config as cfg  # Import de la configuration externe pour les paramètres

# Fonction qui envoie un texte à Kafka
def send_text(producer, topic, text):
    # Envoi du texte au topic Kafka
    producer.send(topic, text.encode('utf-8'))

# Fonction principale pour envoyer une série de messages texte à Kafka
def publish_texts(producer, topic, texts):
    print('Publishing texts...')
    
    for text in texts:
        # Appel de la fonction pour envoyer le texte au topic Kafka
        send_text(producer, topic, text)

        # Délai entre chaque envoi pour simuler un envoi régulier
        time.sleep(1)
    
    print('Publish complete')

# Point d'entrée du script (si le fichier est exécuté directement)
if __name__ == "__main__":
    # Récupérer le nom du topic Kafka à partir de la configuration
    topic = cfg.topic

    # Initialiser le producteur Kafka avec les paramètres de configuration
    producer = KafkaProducer(
        bootstrap_servers='localhost:29092',  # Adresse du serveur Kafka
        linger_ms=100,  # Temps maximum avant d'envoyer un lot, même incomplet
        value_serializer=lambda v: v  # Sérialiseur pour transformer les données en octets
    )

    # Liste des textes à envoyer
    texts = [text, "Message 2", "Message 3", "Message 4"]

    # Appeler la fonction pour publier les textes sur Kafka
    publish_texts(producer, topic, texts)
