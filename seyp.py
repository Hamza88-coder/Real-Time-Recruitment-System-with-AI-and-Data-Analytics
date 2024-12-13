import os
import subprocess
import sys
import requests
import tarfile

def setup_pyspark():
    # Installe pyspark et findspark s'ils ne sont pas déjà installés
    try:
        import pyspark
    except ImportError:
        print("Installation de PySpark...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyspark", "findspark", "delta-spark"])

    import findspark

    # Configuration des chemins pour Spark et Java
    spark_home = os.environ.get("SPARK_HOME", "C:/spark")
    java_home = os.environ.get("JAVA_HOME", "C:/Program Files/Java/jdk-17")

    # Télécharger Spark si nécessaire
    if not os.path.exists(spark_home):
        print("Téléchargement et installation de Spark...")
        url = "https://downloads.apache.org/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz"
        tar_file = "spark-3.4.1-bin-hadoop3.tgz"

        # Télécharger le fichier Spark
        response = requests.get(url, stream=True)
        with open(tar_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

        # Extraire Spark
        with tarfile.open(tar_file, "r:gz") as tar:
            tar.extractall()
        os.rename("spark-3.4.1-bin-hadoop3", "C:/spark")
        os.remove(tar_file)

    # Configurer les variables d'environnement
    os.environ["SPARK_HOME"] = spark_home
    os.environ["JAVA_HOME"] = java_home
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
    os.environ["PATH"] += f";{spark_home}/bin;{java_home}/bin"

    findspark.init(spark_home=spark_home)

    # Test de la configuration
    print("Configuration terminée. Test de PySpark...")
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.appName("Test").getOrCreate()
    print("PySpark est prêt !")
    spark.stop()

setup_pyspark()
