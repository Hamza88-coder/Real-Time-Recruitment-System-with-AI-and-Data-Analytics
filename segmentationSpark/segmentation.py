from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans
from reader_data import CandidatDataLoader
from transformer import CandidatTransformer
import matplotlib.pyplot as plt
import pandas as pd
from pyspark.ml.feature import PCA

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

    # Afficher les résultats de la segmentation
    print("Résultats après segmentation :")
    clustered_df.select("pca_features", "cluster").show(10)

    # Pour visualiser les résultats, convertir en Pandas
    clustered_pandas = clustered_df.select("pca_features", "cluster").toPandas()

    # Extraire les features réduites par PCA pour les visualiser
    features = clustered_pandas["pca_features"].apply(lambda x: list(x)).tolist()
    clusters = clustered_pandas["cluster"].tolist()

    # Convertir les features en DataFrame pour visualisation
    features_df = pd.DataFrame(features, columns=["Feature1", "Feature2"])
    features_df["Cluster"] = clusters

    # Visualisation des clusters
    plt.figure(figsize=(8, 6))
    for cluster in features_df["Cluster"].unique():
        cluster_data = features_df[features_df["Cluster"] == cluster]
        plt.scatter(cluster_data["Feature1"], cluster_data["Feature2"], label=f"Cluster {cluster}")
    
    plt.title("Clusters des candidats")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.legend()
    plt.show()
