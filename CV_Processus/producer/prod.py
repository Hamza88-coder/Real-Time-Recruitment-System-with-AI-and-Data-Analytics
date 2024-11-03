from kafka import KafkaProducer
import config
# 1. Créer un producer Kafka
producer = KafkaProducer(bootstrap_servers='localhost:29092')

# 2. Lire le fichier PDF en mode binaire
with open('document.pdf', 'rb') as fichier_pdf:
    contenu_pdf = fichier_pdf.read()

# 3. Envoyer les données en bytes dans Kafka
producer.send(config.topic, contenu_pdf)
producer.flush()
producer.close()
