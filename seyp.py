from pyspark import SparkContext, SparkConf
import os
os.environ["PYSPARK_PYTHON"] = "python"


from pyspark import SparkConf, SparkContext

# Créer une configuration Spark
conf = SparkConf().setAppName("WordCount").setMaster("spark://localhost:7077")  # Set the correct Spark master URL
sc = SparkContext(conf=conf)

# Vous pouvez maintenant utiliser sc pour exécuter votre travail Spark

# Créer un RDD avec une liste de mots
data = sc.parallelize(["Spark", "Scala","Scala", "Hadoop", "Big Data", "Spark"])

# Compter le nombre d'occurrences de chaque mot
word_counts = data.map(lambda word: (word, 1)).reduceByKey(lambda x, y: x + y)

# Afficher les résultats
for word, count in word_counts.collect():
    print(f"{word}: {count}")

# Arrêter le contexte Spark
sc.stop()
