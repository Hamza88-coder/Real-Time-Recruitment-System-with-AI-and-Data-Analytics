import sys
import time
import cv2
import concurrent.futures  # Import pour exécuter des tâches en parallèle
from kafka import KafkaProducer  # Import du producteur Kafka pour envoyer des messages
import config as cfg  # Import de la configuration externe pour les paramètres

# Fonction qui traite chaque trame (image) individuellement
# Elle encode l'image au format JPG puis l'envoie au sujet Kafka
def process_frame(producer, topic, frame):
    # Encodage de l'image en format .jpg
    ret, buffer = cv2.imencode('.jpg', frame)
    # Si l'encodage est réussi, on envoie l'image encodée au sujet Kafka
    if ret:
        producer.send(topic, buffer.tobytes())

# Fonction qui lit et publie les trames vidéo dans un sujet Kafka
def publish_video(producer, topic, video_file="video.mp4"):
    # Ouverture du fichier vidéo
    video = cv2.VideoCapture(video_file)
    print('Publishing video...')
    
    # Récupérer le nombre d'images par seconde (FPS) de la vidéo
    fps = video.get(cv2.CAP_PROP_FPS)
    # Calculer le délai à appliquer entre chaque trame pour respecter le taux de FPS
    delay = 1 / fps

    # Utilisation d'un pool de threads pour traiter plusieurs trames en parallèle
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Boucle qui lit les trames de la vidéo
        while video.isOpened():
            # Lire une trame de la vidéo
            success, frame = video.read()
            # Si la trame n'est pas lue correctement (fin de la vidéo, erreur de lecture, etc.)
            if not success:
                print("Bad read!")  # Message d'erreur
                break  # On sort de la boucle

            # Redimensionner la trame à une largeur de 720 pixels
            # La hauteur est ajustée proportionnellement pour garder le ratio
            frame = cv2.resize(frame, (720, int(frame.shape[0] * (720 / frame.shape[1]))))

            # Soumettre la trame à un thread du pool pour l'envoyer à Kafka
            executor.submit(process_frame, producer, topic, frame)

            # Délai entre chaque envoi pour respecter le taux de FPS
            time.sleep(delay)
    
    # Libérer la ressource vidéo une fois la publication terminée
    video.release()
    print('Publish complete')

# Point d'entrée du script (si le fichier est exécuté directement)
if __name__ == "__main__":
    # Récupérer le nom du sujet Kafka à partir de la configuration
    topic = cfg.topic

    # Initialiser le producteur Kafka avec les paramètres de configuration
    producer = KafkaProducer(
        bootstrap_servers='localhost:29092',  # Adresse du serveur Kafka
        batch_size=15728640,  # Taille maximale d'un lot avant d'être envoyé
        linger_ms=100,  # Temps maximum avant d'envoyer un lot, même incomplet
        max_request_size=15728640,  # Taille maximale des requêtes Kafka (15 MB)
        value_serializer=lambda v: v  # Sérialiseur pour transformer les données en octets
    )

    # Appeler la fonction pour publier la vidéo sur Kafka
    publish_video(producer, topic)
