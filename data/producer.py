
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
    texts = ["text", "Message 2", "Message 3", "Message 4"]

    # Appeler la fonction pour publier les textes sur Kafka
    publish_texts(producer, topic, texts)
