from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans
from reader_data import CandidatDataLoader
from transformer import CandidatTransformer
from pyspark.ml.feature import PCA
from pyspark.sql.functions import col

class CandidatSegmentation:
    def __init__(self, df, k=3, seed=42):
        """
        Initialise la classe pour la segmentation des candidats.
        :param df: DataFrame Spark contenant les données transformées.
        :param k: Nombre de clusters pour KMeans.
        :param seed: Seed pour la reproductibilité.
        """
        self.df = df
        self.k = k
        self.seed = seed

    def segment(self):
        """
        Applique la segmentation KMeans sur le DataFrame.
        :return: DataFrame avec une colonne supplémentaire "cluster" représentant les clusters.
        """
        # Configurer le modèle KMeans
        kmeans = KMeans(k=self.k, seed=self.seed, featuresCol="features", predictionCol="cluster")

        # Ajuster le modèle
        model = kmeans.fit(self.df)

        # Appliquer la segmentation et ajouter les prédictions au DataFrame
        df_clustered = model.transform(self.df)

        return df_clustered


# Exemple d'utilisation
if __name__ == "__main__":
   
    # Charger les données
    loader = CandidatDataLoader()
    df_candidats = loader.load_data()
    
    # Appliquer les transformations
    transformer = CandidatTransformer(df_candidats)
    result_df = transformer.transform()

    # Appliquer PCA pour réduire les dimensions à 2
    pca = PCA(k=2, inputCol="features", outputCol="pca_features")
    pca_model = pca.fit(result_df)
    result_df_pca = pca_model.transform(result_df)

    # Appliquer la segmentation KMeans
    segmenter = CandidatSegmentation(result_df_pca, k=3)
    clustered_df = segmenter.segment()

    # Aplatir la colonne `pca_features` en deux colonnes distinctes pour l'exportation
    export_df = clustered_df.select(
        col("pca_features").getItem(0).alias("Feature1"),
        col("pca_features").getItem(1).alias("Feature2"),
        col("cluster").alias("Cluster")
    )

    # Spécifier le chemin d'exportation
    export_path = "./segmentation_results.csv"

    # Enregistrer les résultats en CSV
    export_df.write.csv(export_path, header=True, mode="overwrite")

    print(f"Résultats de segmentation enregistrés dans : {export_path}")
