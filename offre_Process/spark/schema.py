# Définir le schéma pour le JSON
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
from pyspark.sql.types import StructType, StructField, StringType, ArrayType

OFFRE_SCHEMA= StructType([
    StructField("titre_du_poste", StringType(), True),
    StructField("societe", StringType(), True),
    StructField("competences", ArrayType(StringType()), True),
    StructField("lieu", StringType(), True),
    StructField("type_offre", StringType(), True),
    StructField("durée", StringType(), True),
    StructField("type_de_contrat", StringType(), True),
    StructField("email", StringType(), True),
    StructField("telephone", StringType(), True),
    StructField("type", StringType(), True),
    StructField("langues", ArrayType(StringType()), True),
    StructField("salaire", StringType(), True),
    StructField("date_de_debut", StringType(), True),
    StructField("secteur_dactivite", StringType(), True),
    StructField("experience_demande", StringType(), True),
    StructField("formation_requise", StringType(), True),
    StructField("avantages", ArrayType(StringType()), True),
    StructField("site_web", StringType(), True)
])
