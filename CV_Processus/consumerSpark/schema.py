from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType, StructType, StructField
import fitz
import yaml
from groq import Groq
import json
import re
from pyspark.sql.types import StructType, StructField, StringType, ArrayType
from io import BytesIO
from datetime import datetime
import os
PERSON_SCHEMA = StructType([
   
    StructField("last_name", StringType(), True),
    StructField("full_name", StringType(), True),
    StructField("title", StringType(), True),
    StructField("address", StructType([
        StructField("formatted_location", StringType(), True),
        StructField("city", StringType(), True),
        StructField("region", StringType(), True),
        StructField("country", StringType(), True),
        StructField("postal_code", StringType(), True)
    ]), True),
    StructField("objective", StringType(), True),
    StructField("date_of_birth", StringType(), True),
    StructField("place_of_birth", StringType(), True),
    StructField("phones", StringType(), True),
    StructField("urls", StructType([
        StructField("GitHub", StringType(), True),
        StructField("portfolio", StringType(), True),
        StructField("LinkedIn", StringType(), True),
        StructField("site_web", StringType(), True)
    ]), True),
    StructField("gender", StringType(), True),
    StructField("nationality", StringType(), True),
    StructField("education_details", ArrayType(StructType([
        StructField("etude_title", StringType(), True),
        StructField("etablissement_name", StringType(), True),
        StructField("start_date", StringType(), True),
        StructField("end_date", StringType(), True),
        StructField("etude_city", StringType(), True),
        StructField("etude_region", StringType(), True),
        StructField("end_country", StringType(), True)
    ])), True),
    StructField("work_experience_details", ArrayType(StructType([
        StructField("job_title", StringType(), True),
        StructField("company_name", StringType(), True),
        StructField("city", StringType(), True),
        StructField("region", StringType(), True),
        StructField("sector_of_activity", StringType(), True),
        StructField("start_date", StringType(), True),
        StructField("end_date", StringType(), True)
    ])), True),
    StructField("skills", ArrayType(StringType()), True),
    StructField("language", ArrayType(StructType([
        StructField("name", StringType(), True),
        StructField("level", StringType(), True)
    ])), True),
    StructField("certifications", ArrayType(StructType([
        StructField("name", StringType(), True),
        StructField("etablissement_certification", StringType(), True),
        StructField("date", StringType(), True)
    ])), True)
])