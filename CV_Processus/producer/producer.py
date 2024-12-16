from kafka import KafkaProducer
import config
import os
import time

# 1. Créer un producer Kafka
producer = KafkaProducer(bootstrap_servers='localhost:29092')

# 2. Spécifier le dossier contenant les fichiers PDF
dossier_data = os.path.join(os.path.dirname(__file__), "data")

# 3. Parcourir tous les fichiers dans le dossier et envoyer chaque PDF
for fichier in os.listdir(dossier_data):
    if fichier.endswith('.pdf'):  # Filtrer uniquement les fichiers PDF
        chemin_fichier = os.path.join(dossier_data, fichier)
        with open(chemin_fichier, 'rb') as fichier_pdf:
            contenu_pdf = fichier_pdf.read()
            # 4. Envoyer les données dans Kafka
            producer.send(config.topic, contenu_pdf)
            print(f"Fichier envoyé : {fichier}", flush=True)  # Affichage immédiat
            # Attendre 8 secondes avant d'envoyer le prochain fichier
            time.sleep(2)

# 5. Finaliser le producer
producer.flush()
producer.close()
