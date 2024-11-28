from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.classification import LogisticRegression

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
        region_indexer = StringIndexer(inputCol="region", outputCol="region_indexed")

        # Étape 2 : Assemblage des caractéristiques
        feature_assembler = VectorAssembler(
            inputCols=["age", "experience", "region_indexed"],
            outputCol="features"
        )

        # Créer un pipeline avec les étapes nécessaires
        pipeline = Pipeline(stages=[
            region_indexer,   # Indexer la colonne 'region'
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
    from pyspark.sql import SparkSession

    # Créer une session Spark
    spark = SparkSession.builder \
        .appName("TransformationsCandidats") \
        .getOrCreate()

    # Exemple de DataFrame
    data = [
        (25, 3, "Europe"),
        (40, 15, "Asie"),
        (30, 8, "Afrique"),
    ]
    columns = ["age", "experience", "region"]

    df_candidats = spark.createDataFrame(data, columns)

    # Instancier la classe avec le DataFrame
    transformer = CandidatTransformer(df_candidats)

    # Appliquer les transformations
    result_df = transformer.transform()

    # Afficher les colonnes transformées
    result_df.select("features").show()
