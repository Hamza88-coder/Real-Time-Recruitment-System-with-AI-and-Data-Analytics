from pyspark.ml.clustering import KMeans

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
