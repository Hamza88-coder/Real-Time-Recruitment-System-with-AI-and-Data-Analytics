import cv2
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import BinaryType
import os
from datetime import datetime  # Importer le module datetime
import config as cfg

# Créer le répertoire pour les images traitées s'il n'existe pas déjà
output_folder = 'images_traited'
os.makedirs(output_folder, exist_ok=True)
os.environ["PYSPARK_PIN_THREAD"] = "true"

spark = SparkSession.builder \
    .appName("Kafka Spark Structured Streaming App") \
    .master("local[*]") \
    .config("spark.jars.packages", 
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.3," 
        "org.apache.kafka:kafka-clients:3.4.1," 
        "org.apache.commons:commons-pool2:2.11.1") \
    .getOrCreate()
if spark:
    print("Session is created")

# Fonction pour traiter une image et dessiner un rectangle
def process_image_cons(image_bytes):
    np_array = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if frame is not None:
        # Obtenir les dimensions de l'image
        height, width, _ = frame.shape

        # Définir les coordonnées du rectangle (ici, centré dans l'image)
        start_point = (width // 4, height // 4)  # Coin supérieur gauche
        end_point = (width * 3 // 4, height * 3 // 4)  # Coin inférieur droit

        # Dessiner le rectangle sur l'image
        cv2.rectangle(frame, start_point, end_point, (0, 255, 0), 2)  # Vert, épaisseur 2

        # Encoder l'image modifiée en format JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()
    else:
        print("Image decoding failed.")
        return b''  # Retourner une image vide si le décodage échoue

# Créer un UDF pour Spark
process_image_udf = udf(process_image_cons, BinaryType())

kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:29092") \
    .option("subscribe", cfg.topic) \
    .load()

kafka_df = kafka_df.selectExpr("CAST(value AS BINARY) as img_bytes")
processed_df = kafka_df.withColumn("img_bytes", process_image_udf(col("img_bytes")))

def process_batch(df, epoch_id):
    print(f"Traitement du micro-lot {epoch_id}")
    for row in df.collect():
        if row['img_bytes']:  # Vérifiez que les octets de l'image ne sont pas vides
            # Générer un timestamp pour le nom de fichier
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")  # Format : YYYYMMDD_HHMMSS_microsecond
            filename = os.path.join(output_folder, f"{timestamp}.jpg")  # Créer le nom de fichier avec le timestamp
            with open(filename, 'wb') as f:
                f.write(row['img_bytes'])
            print(f"Image sauvegardée : {filename}")
        else:
            print("Aucune image à sauvegarder.")

query = processed_df.writeStream \
    .outputMode("append") \
    .foreachBatch(process_batch) \
    .start()

# Attendre que le stream soit arrêté
query.awaitTermination()
