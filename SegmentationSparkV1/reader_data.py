from pyspark.sql import SparkSession

class CandidatDataLoader:
    def __init__(self, jdbc_url="jdbc:postgresql://localhost:5432/cond_db"):
        """
        Initialise la classe pour charger les données depuis PostgreSQL.
        :param jdbc_url: URL de connexion JDBC à la base de données PostgreSQL.
        """
        self.jdbc_url = jdbc_url
        self.query = """
        SELECT 
            c.full_name AS candidate_name,
            t.title_name AS title,
            COALESCE(SUM(EXTRACT(YEAR FROM we.end_date) - EXTRACT(YEAR FROM we.start_date)), 0) AS total_years_work_experience,
            COALESCE(SUM(EXTRACT(YEAR FROM ed.end_date) - EXTRACT(YEAR FROM ed.start_date)), 0) AS total_years_education,
            STRING_AGG(DISTINCT s.skill_name, ', ') AS skills,
            STRING_AGG(DISTINCT we.sector_of_activity, ', ') AS sector_of_activity,
            STRING_AGG(DISTINCT CONCAT(l.language_name, ' (', pl.level_name, ')'), ', ') AS language
        FROM 
            candidates c
        LEFT JOIN 
            title t ON c.title_id = t.id
        LEFT JOIN 
            work_experience_details we ON c.id = we.candidate_id
        LEFT JOIN 
            education_details ed ON c.id = ed.candidate_id
        LEFT JOIN 
            candidate_skills cs ON c.id = cs.candidate_id
        LEFT JOIN 
            skills s ON cs.skill_id = s.id
        LEFT JOIN 
            candidate_languages cl ON c.id = cl.candidate_id
        LEFT JOIN 
            languages l ON cl.language_id = l.id
        LEFT JOIN 
            proficiency_levels pl ON cl.proficiency_level_id = pl.id
        GROUP BY 
            c.id, t.title_name
        """

        self.properties = {
            "user": "postgres",
            "password": "qqqqqqqqq",
            "driver": "org.postgresql.Driver"
        }

        # Créer la session Spark
        self.spark = SparkSession.builder \
            .appName("SegmentationCandidats") \
            .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
            .config("spark.local.dir", "temp") \
            .getOrCreate()

    def load_data(self):
        """
        Charge les données depuis PostgreSQL à l'aide de la requête SQL définie.
        :return: DataFrame Spark contenant les données sélectionnées.
        """
        try:
            # Charger les données avec la requête SQL
            df = self.spark.read.jdbc(
                url=self.jdbc_url,
                table=f"({self.query}) AS candidates_data",
                properties=self.properties
            )
            return df
        except Exception as e:
            print(f"Erreur lors du chargement des données : {e}")
            return None


# Exemple d'utilisation
if __name__ == "__main__":
   
    if __name__ == "__main__":
     loader = CandidatDataLoader()
     df = loader.load_data()
    if df is not None:
        df.show()
