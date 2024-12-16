from datetime import datetime

from flask import Flask, request, render_template, redirect, url_for
from flask import Flask, render_template, request, redirect, url_for, flash

import os
import pandas as pd
import gensim
import numpy as np
from nltk import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import fitz  # PyMuPDF
from groq import Groq
import re
import csv
import pandas as pd
import csv
import pinecone
import numpy as np
from sentence_transformers import SentenceTransformer
import snowflake.connector
import uuid
import redis

api_key_grouq="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"
api_key_pin = "pcsk_vUaKS_3PK35kGth5rcmSKZkihFFuaS7B44xzMycHCnot1s9Czf1WE8iXSPZg4nDph81Ak"




app = Flask(__name__)

app.config['REDIS_URL'] = "redis://localhost:6379/0"  # Utilisez l'URL de votre instance Redis
# Définir une clé secrète pour la session
app.secret_key = 'said'

# Connexion à Redis
redis_client = redis.StrictRedis.from_url(app.config['REDIS_URL'])
# Charger le modèle Word2Vec
#model = gensim.models.Word2Vec.load("D:/mémoire/resume_word2vec.model")
import json
import uuid

def ats_extractor(resume_data):
    # Prompt for extracting specific information from the resume
    prompt = '''
    You are an AI bot designed to act as a professional for parsing resumes. You are given a resume, and your job is to extract the following information:
    1. skills 
    2. languages
    3. education (field of study such as Computer Science, Management, Medicine, Marketing, Electrical Engineering, etc.)
    4. total number of work experiences
    Provide the extracted information in JSON format only with english translation. Additionally, generate a unique ID for the job .
    If a field does not exist, do "None".

    Expected example:
    {
        "job_id": "Unique ID generated for the candidate.",
        "competences": ["List of skills (e.g., Python, project management) in English."],
        "langues": ["list of Language name (e.g., English, French) without proficiency levels in English."],
        "formation": "field_of_study": "Field of study (e.g., Computer Science, Marketing) in English.",
        "nbr_years_exp": "Total number of work experiences."
    }
    '''

    # Initialize the Groq API client
    groq_client = Groq(api_key=api_key_grouq)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": resume_data}
    ]

    # Generate the response
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.0,
        max_tokens=1500
    )

    data = response.choices[0].message.content
    try:
        json_match = re.search(r"\{.*\}", data, re.DOTALL)  # Extract JSON from curly braces
        if json_match:
            json_data = json.loads(json_match.group(0))  # Load the JSON

            # Add a unique ID for the candidate
            json_data["candidate_id"] = str(uuid.uuid4())

            return json_data
        else:
            return {"error": "JSON not found in the output."}
    except json.JSONDecodeError as e:
        return {"error": f"JSON decoding error: {e}"}

# Fonction de prétraitement
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token.isalpha()]
    return tokens


# Fonction pour extraire du texte des fichiers PDF
import os
import fitz  # PyMuPDF






def json_to_csv(json_data, csv_file_path):
    # Ensure json_data is a dictionary
    if not isinstance(json_data, dict):
        return {"error": "Invalid JSON data."}

    # Define the CSV header
    header = ["candidate_id", "competences", "langues", "formation", "nbr_years_exp"]

    # Convert data into a list of rows
    rows = [
        [
            json_data.get("candidate_id", "None"),
            ", ".join(json_data.get("competences", [])),
            ", ".join(json_data.get("langues", [])),
            json_data.get("formation", "None"),
            json_data.get("nbr_years_exp", "None")
        ]
    ]

    # Write to CSV
    try:
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
    except Exception as e:
        return {"error": f"Error writing CSV: {e}"}

    return {"message": "CSV file created successfully.", "file_path": csv_file_path}
def search_similar_vectors_candidat(query_embedding, top_k=5):
    pc = pinecone.Pinecone(api_key=api_key_pin)
    # Connexion à l'index Pinecone
    index_name = 'candidates'  # Le nom de votre index Pinecone
    index_candidats = pc.Index(index_name)
    print(f"Query embedding: {query_embedding}")
    result = index_candidats.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    print(f"Result: {result}")

    # Vérification de la présence de la clé 'matches'
    if 'matches' in result:
        similar_vectors = []
        for match in result['matches']:
            similar_vectors.append({
                'id': match['id'],  # Extraire l'ID
                'score': match['score']  # Extraire le score
            })
        return similar_vectors
    else:
        print("Aucun résultat trouvé.")
        return []


@app.route('/', methods=['GET', 'POST'])
def job_description():
    global similar_vectors_candidat
    if request.method == 'POST':
        job_description = request.form['job_description']
        # Pass the extracted text to the ats_extractor function
        extracted_info = ats_extractor(job_description)
        resumes_csv = json_to_csv(extracted_info, "resumes.csv")
        data = pd.read_csv("resumes.csv")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        data['competences'] = data['competences'].apply(
            lambda x: ', '.join(sorted(x.split(', '))) if pd.notnull(x) else '')
        data['langues'] = data['langues'].apply(lambda x: ', '.join(sorted(x.split(', '))) if pd.notnull(x) else '')
        data['competences'] = data['competences'].str.lower()
        data['langues'] = data['langues'].str.lower()
        data['formation'] = data['formation'].astype(str).str.lower()
        data.fillna({'COMPETENCES': '', 'LANGUES': '', 'FORMATION': '', 'EXPERIENCE_DUR': 0}, inplace=True)
        data['description'] = data['competences'] + ", " + data['langues'] + ", " + data['formation'] + ", " + data[
            'nbr_years_exp'].astype(str)
        embeddings_data = model.encode(data['description'].tolist(), show_progress_bar=True)
        query = embeddings_data
        query_embedding = query.tolist()
        # Recherche des 5 vecteurs les plus similaires
        similar_vectors_candidat = search_similar_vectors_candidat(query_embedding, top_k=5)
        print(f"Nombre de vecteurs candidats similaires trouvés : {len(similar_vectors_candidat)}")
        for vector in similar_vectors_candidat:
            print(f"ID: {vector['id']}, Score: {vector['score']}")

        return redirect(url_for('ranking2'))

    return render_template('job_description.html')


@app.route('/ranking2')
def ranking2():
    global similar_vectors_candidat
    # Nombre de vecteurs similaires
    nbr_simil = len(similar_vectors_candidat)
    # Générer la liste `resumes` avec les champs id et score arrondi (en pourcentage)
    resumes_candidat = [
        {
            "ID": vector['id'],  # ID du vecteur
            "Score": round(vector['score'] * 100, 2)  # Score en pourcentage
        }
        for vector in similar_vectors_candidat
    ]

    return render_template('ranking2.html', nbr_simil=nbr_simil, resumes=resumes_candidat)





@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    return f"9alib 3liha"
@app.route('/chatbot_key/<key>', methods=['GET', 'POST'])
def chatbot_key(key):
    return f"9alib 3liha"+key
@app.route('/post_cvs/<key>', methods=['GET', 'POST'])
def post_cvs(key):

    return 0



if __name__ == '__main__':
    app.run(debug=True)
