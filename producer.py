from kafka import KafkaProducer

# Configuration du producteur Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    max_request_size=15728640,  # Augmentation de la taille max des requêtes
    value_serializer=lambda v: v  # Sérialisation binaire
)

# Lecture du fichier PDF en mode binaire
with open("document.pdf", "rb") as file:
    pdf_data = file.read()

# Envoi des données PDF au topic Kafka
producer.send("distributed-video1", pdf_data)
print("PDF publié avec succès dans Kafka.")
producer.flush()
