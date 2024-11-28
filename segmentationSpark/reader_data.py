from pyspark.sql import SparkSession

class CandidatDataLoader:
    def __init__(self, jdbc_url, table_name, properties):
        """
        Initialise la classe pour charger les données depuis PostgreSQL.
        :param jdbc_url: URL de connexion JDBC à la base de données PostgreSQL.
        :param table_name: Nom de la table à lire.
        :param properties: Propriétés de connexion (utilisateur, mot de passe, etc.).
        """
        self.jdbc_url = jdbc_url
        self.table_name = table_name
        self.properties = properties

        # Créer la session Spark
        self.spark = SparkSession.builder \
            .appName("SegmentationCandidats") \
            .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
            .getOrCreate()

    def load_data(self):
        """
        Charge les données depuis PostgreSQL.
        :return: DataFrame Spark contenant les données de la table.
        """
        df = self.spark.read.jdbc(url=self.jdbc_url, table=self.table_name, properties=self.properties)
        return df

# Exemple d'utilisation
if __name__ == "__main__":
    jdbc_url = "jdbc:postgresql://localhost:5433/candidat"
    table_name = "personnel"
    properties = {
        "user": "postgres",
        "password": "papapapa",
        "driver": "org.postgresql.Driver"
    }

    # Créer une instance de la classe et charger les données
    data_loader = CandidatDataLoader(jdbc_url, table_name, properties)
    df_candidats = data_loader.load_data()

    # Afficher les données
    df_candidats.show()
