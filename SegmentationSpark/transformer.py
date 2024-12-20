from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.classification import LogisticRegression

from reader_data import CandidatDataLoader


class CandidatTransformer:
    def __init__(self, df):
        """
        Initialise la classe avec un DataFrame Spark.
        :param df: DataFrame Spark contenant les données.
        """
        self.df = df

    def build_pipeline(self):
        """
        Construit un pipeline pour transformer les données.
        :return: Un objet Pipeline.
        """
        # Étape 1 : Indexation des colonnes catégoriques
        title_indexer = StringIndexer(inputCol="title", outputCol="title_indexed",handleInvalid="skip")
        langue_indexer = StringIndexer(inputCol="language", outputCol="language_indexed",handleInvalid="skip")
        sector_indexer = StringIndexer(inputCol="sector_of_activity", outputCol="sector_indexed",handleInvalid="skip")

        # Étape 2 : Assemblage des caractéristiques
        feature_assembler = VectorAssembler(
            inputCols=["total_years_work_experience", "total_years_education", "title_indexed","language_indexed","sector_indexed"],
            outputCol="features"
        )

        # Créer un pipeline avec les étapes nécessaires
        pipeline = Pipeline(stages=[
            title_indexer,
              langue_indexer,
                  sector_indexer,
                       
            feature_assembler # Assembler les colonnes en une seule colonne 'features'
        ])

        return pipeline

    def transform(self):
        """
        Applique les transformations sur le DataFrame Spark.
        :return: DataFrame transformé.
        """
        # Construire et ajuster le pipeline
        pipeline = self.build_pipeline()
        model = pipeline.fit(self.df)

        # Appliquer les transformations
        transformed_df = model.transform(self.df)
        return transformed_df

# Exemple d'utilisation
if __name__ == "__main__":
    
    loader = CandidatDataLoader()
    df_candidats = loader.load_data()
    
   

    # Instancier la classe avec le DataFrame
    transformer = CandidatTransformer(df_candidats)

    # Appliquer les transformations
    result_df = transformer.transform()

    # Afficher les colonnes transformées
    result_df.select("features").show()
