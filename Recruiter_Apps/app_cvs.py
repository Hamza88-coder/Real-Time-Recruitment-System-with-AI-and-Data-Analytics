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
# Détails de connexion à Snowflake
account = "phztxrc-go36107"
user = "SAID"
password = "SaidKHALID2002!"
role = "dev_role"
warehouse = "projet_warehouse"
database = "my_project_database"
schema = "my_project_schema"

# Connexion à Snowflake
conn = snowflake.connector.connect(
    account=account,
    user=user,
    password=password,
    role=role,
    warehouse=warehouse,
    database=database,
    schema=schema
)

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
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
    Provide the extracted information in JSON format only with english translation. Additionally, generate a unique ID for the candidate .
    If a field does not exist, do "None".

    Expected example:
    {
        "candidate_id": "Unique ID generated for the candidate.",
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

# Fonction pour obtenir les embeddings moyennés
def get_average_word_vector(tokens, model):
    word_vectors = [model.wv[token] for token in tokens if token in model.wv]
    if not word_vectors:
        return np.zeros(model.vector_size)
    return np.mean(word_vectors, axis=0)



def extract_text_from_pdf(upload_folder):
    """
    Extrait le texte de tous les fichiers PDF dans un dossier.

    Args:
        upload_folder (str): Chemin du dossier contenant les fichiers PDF.

    Returns:
        dict: Dictionnaire avec les noms de fichiers comme clés et les textes extraits comme valeurs.
    """
    #extracted_text = {}

    try:
        # Parcourir tous les fichiers du dossier
        for filename in os.listdir(upload_folder):
            if filename.endswith('.pdf'):
                filepath = os.path.join(upload_folder, filename)
                doc = fitz.open(filepath)
                text = ""

                # Extraire le texte de chaque page du PDF
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text += page.get_text("text")
                    return text



    except Exception as e:
        # Gérer les erreurs et retourner un message
        return {"error": f"Erreur lors de l'extraction des textes : {e}"}


def generee_offres(descriptions):
    description_prompt = '''
        You are an AI bot designed to generate detailed job descriptions. Based on the following candidate information, create a professional job description in English. The format should include:
        - Industry: Mention the industry (e.g., "Computer and Technology").
        - Job Title: Suggest a title based on skills and education (e.g., "Data Scientist").
        - Date: Use the current date in the format YYYY-MM-DD.
        - Description: Provide a paragraph summarizing the skills, languages, education, and years of experience. Make the description engaging and professional.

        Example:
        Industry: Computer And Technology
        Data Scientist
        Date: 2021-08-18 00:00:00
        Description du poste :

        Nous sommes à la recherche d'un Développeur Python passionné par le Machine Learning pour rejoindre notre équipe dynamique. Avec 5 ans d'expérience dans le domaine, vous serez responsable de la conception, du développement et de l'optimisation de solutions innovantes basées sur l'intelligence artificielle.

        Compétences requises :

        Maîtrise de Python et des bibliothèques de Machine Learning (comme TensorFlow, scikit-learn, etc.)
        Solides compétences en analyse de données et en modélisation
        Capacité à travailler en équipe et à communiquer efficacement en anglais et en français
        Formation :

        Diplôme en informatique ou domaine connexe
        Expérience :

        Minimum de 5 ans d'expérience en développement de logiciels, avec un accent particulier sur le Machine Learning
        Ce que nous offrons :

        Un environnement de travail collaboratif et stimulant
        Des opportunités de développement professionnel
        Un package salarial compétitif
        '''

    # Initialize the Groq API client
    groq_client = Groq(api_key=api_key_grouq)

    # Dictionary to store the generated descriptions
    generated_offers = {}

    # Loop through the input dictionary (descriptions)
    for key, value in descriptions.items():
        # Extract information from the dictionary (e.g., competences, formation, experience, entreprise)
        competences = value['competences']
        langues = value['langues']
        formation = value['formation']
        experience_dur = value['experience_dur']
        entreprise = value['entreprise']

        # Format the input for the AI bot
        job_description_input = f'''
            Industry: {formation}
            Job Title: Based on your skills and experience, we recommend a title such as Data Scientist, Data Engineer, or similar roles.
            Date: une date
            Description du poste :

            We are looking for a dynamic and skilled professional to join our team. With {experience_dur} of experience in the field, you will be responsible for leveraging your expertise in {competences} to drive business outcomes. You will be working with state-of-the-art technologies and collaborating with a team of experts.

            Required Skills:
            {competences}

            Languages:
            {langues}

            Education:
            {formation}

            Experience:
            {experience_dur} of experience in the field

            Company:
            {entreprise}

            What we offer:
            A collaborative and challenging work environment
            Opportunities for professional growth and development
            A competitive salary and benefits package
        '''

        # Create the input message for Llama
        description_messages = [
            {"role": "system", "content": description_prompt},
            {"role": "user", "content": job_description_input}
        ]

        # Generate the response
        description_response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=description_messages,
            temperature=0.7,
            max_tokens=1000
        )

        # Extract the generated text
        description_text = description_response.choices[0].message.content.strip()

        # Add the generated description to the dictionary
        generated_offers[key] = description_text

    return generated_offers


def save_picture(form_picture):
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f_name + f_ext
    picture_path = os.path.join(app.root_path, 'static', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

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
def search_similar_vectors_job(query_embedding, top_k=5):
    pc = pinecone.Pinecone(api_key=api_key_pin)
    # Connexion à l'index Pinecone
    index_name = 'job'  # Le nom de votre index Pinecone
    index_job= pc.Index(index_name)
    print(f"Query embedding: {query_embedding}")
    result = index_job.query(vector=query_embedding, top_k=top_k, include_metadata=True)
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
def index():
    global similar_vectors_candidat
    global similar_vectors_job
    global nom_cv
    if request.method == 'POST':
        if 'resume_folder' in request.files:
            # Traiter le téléchargement des fichiers PDF
            resume_folder = request.files.getlist('resume_folder')
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            for file in resume_folder:
                # Générer une clé unique pour chaque fichier
                unique_key = str(uuid.uuid4())  # Utiliser uuid pour générer une clé unique

                # Ajouter la clé unique dans Redis avec le nom du fichier
                redis_client.set(unique_key, file.filename)  # Enregistrer le nom du fichier sous la clé unique

                # Obtenir la date et l'heure actuelles
                current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format YYYYMMDD_HHMMSS

                # Créer le chemin du fichier avec la date et l'heure
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_key}_{current_time}_{file.filename}")

                # Sauvegarder le fichier avec la clé unique et la date/heure comme nom de fichier
                file.save(file_path)
                nom_cv=file.filename


            # Extraire les textes des PDF
            resumes = extract_text_from_pdf(app.config['UPLOAD_FOLDER'])
            # Pass the extracted text to the ats_extractor function
            extracted_info = ats_extractor(resumes)
            resumes_csv = json_to_csv(extracted_info, "resumes.csv")
            data = pd.read_csv("resumes.csv")
            model = SentenceTransformer('all-MiniLM-L6-v2')
            data['competences'] = data['competences'].apply(
                lambda x: ', '.join(sorted(x.split(', '))) if pd.notnull(x) else '')
            data['langues'] = data['langues'].apply(lambda x: ', '.join(sorted(x.split(', '))) if pd.notnull(x) else '')
            data['competences'] = data['competences'].str.lower()
            data['langues'] = data['langues'].str.lower()
            data['formation'] = data['formation'].str.lower()
            data.fillna({'COMPETENCES': '', 'LANGUES': '', 'FORMATION': '', 'EXPERIENCE_DUR': 0}, inplace=True)
            data['description'] = data['competences'] + ", " + data['langues'] + ", " + data['formation'] + ", " + data[
                'nbr_years_exp'].astype(str)
            embeddings_data = model.encode(data['description'].tolist(), show_progress_bar=True)
            query = embeddings_data
            query_embedding = query.tolist()  # Convertir en une liste de vecteurs

            # query_embedding = np.array(query, dtype=np.float32)
            # Recherche de tous les vecteurs similaires


            # Recherche des 5 vecteurs les plus similaires
            similar_vectors_candidat = search_similar_vectors_candidat(query_embedding, top_k=5)
            print(f"Nombre de vecteurs candidats similaires trouvés : {len(similar_vectors_candidat)}")
            for vector in similar_vectors_candidat:
                print(f"ID: {vector['id']}, Score: {vector['score']}")

            # Recherche des 5 vecteurs les plus similaires
            similar_vectors_job = search_similar_vectors_job(query_embedding, top_k=6)
            print(f"Nombre de vecteurs jobs similaires trouvés : {len(similar_vectors_job)}")
            for vector in similar_vectors_job:
                print(f"ID: {vector['id']}, Score: {vector['score']}")



            # # Créer un DataFrame et sauvegarder en CSV
            # df = pd.DataFrame(resumes, columns=['ID', 'Resume_str'])
            # df.to_csv('resumes.csv', index=False)

            return redirect(url_for('ranking'))
    return render_template('index.html')
@app.route('/ranking')
def ranking():
    global similar_vectors_candidat
    #global similar_vectors_job
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

    return render_template('ranking.html', nbr_simil=nbr_simil, resumes=resumes_candidat)
@app.route('/jobs')
def jobs():
    global similar_vectors_candidat
    global similar_vectors_job
    global resumes_job
    # Nombre de vecteurs similaires
    nbr_simil = len(similar_vectors_job)
    # Générer la liste `resumes` avec les champs id et score arrondi (en pourcentage)
    resumes_job = [
        {
            "ID": vector['id'],  # ID du vecteur
            "Score": round(vector['score'] * 100, 2)  # Score en pourcentage
        }
        for vector in similar_vectors_job
    ]

    return render_template('jobs.html', nbr_simil=nbr_simil, resumes=resumes_job)
@app.route('/show_jobs')
def show_jobs():
    global resumes_job
    global descriptions
    print(resumes_job)
    # Récupération des IDs (avec protection pour éviter l'erreur d'indexation)
    id_job1 = resumes_job[0]['ID'] if len(resumes_job) > 0 else None
    id_job2 = resumes_job[1]['ID'] if len(resumes_job) > 1 else None
    id_job3 = resumes_job[2]['ID'] if len(resumes_job) > 2 else None
    id_job4 = resumes_job[3]['ID'] if len(resumes_job) > 3 else None
    id_job5 = resumes_job[4]['ID'] if len(resumes_job) > 4 else None
    id_job6=resumes_job[5]['ID'] if len(resumes_job) > 5 else None
    # Liste des IDs pour lesquels vous souhaitez générer les descriptions
    id_jobs = [id_job1, id_job2, id_job3, id_job4, id_job5, id_job6]

    # Dictionnaire pour stocker les descriptions
    descriptions = {}

    # Requête SQL de base
    query_offres = """
        SELECT o.offre_id,
               LISTAGG(DISTINCT cmp.nom, ', ') AS competences,
               LISTAGG(DISTINCT lng.nom, ', ') AS langues,
               f.nom AS formation,
               o.experience_dur,
               e.nom as nom_entreprise
        FROM my_project_database.my_project_schema.offre_fait o
        JOIN my_project_database.my_project_schema.offre_comp oc ON o.offre_id = oc.offre_id
        JOIN my_project_database.my_project_schema.competence cmp ON oc.competence_id = cmp.competence_id
        LEFT JOIN my_project_database.my_project_schema.langue_offr lo ON o.offre_id = lo.offre_id
        LEFT JOIN my_project_database.my_project_schema.langue lng ON lo.langue_id = lng.langue_id
        LEFT JOIN my_project_database.my_project_schema.formation f ON o.formation_id = f.formation_id
        LEFT JOIN my_project_database.my_project_schema.entreprise e ON o.entreprise_id = e.entreprise_id
        WHERE o.offre_id = %s
        GROUP BY o.offre_id, f.nom, o.experience_dur, e.nom
    """
    try:
        # Créer un curseur pour exécuter des requêtes
        cursor = conn.cursor()

        # Exécuter la requête pour chaque ID
        for i, id_job in enumerate(id_jobs, start=1):
            if id_job:  # Vérifier que l'ID n'est pas None
                cursor.execute(query_offres, (id_job,))
                result = cursor.fetchone()

                # Stocker le résultat dans une variable nommée dynamiquement
                descriptions[result[0]] = {
                    "offre_id": result[0],
                    "competences": result[1],
                    "langues": result[2],
                    "formation": result[3],
                    "experience_dur": result[4],
                    "entreprise":result[5],
                } if result else None

        # Afficher les descriptions
        for key, value in descriptions.items():
            print(f"{key}: {value}")

    finally:
        # Fermer la connexion à Snowflake
        pass
    generated_offers=generee_offres(descriptions)
    return render_template('show_jobs.html', generated_offers=generated_offers)





@app.route('/post_cvs/<key>', methods=['GET', 'POST'])
def post_cvs(key):
    global descriptions
    global nom_cv
    # Exemple de nom de CV (ceci peut être dynamique si récupéré de l'utilisateur ou d'une base de données)
      # Exemple de nom, à remplacer par une logique dynamique si nécessaire.
    # Ajouter les informations dans Redis sous la forme (key: offer_id) -> CV name
    redis_client.set(key, nom_cv)  # Stocke le nom du CV pour l'ID de l'offre

    # Ajouter un message de notification avec flash
    flash(f"Submit your CV: {nom_cv} for Offer ID: {key}", "info")

    # Rediriger vers la page des offres après l'application
    return redirect(url_for('show_jobs'))

# @app.route("/post_cvs/<jobid>", methods=['GET', 'POST'])
# def post_cvs(jobid):
#     form = ApplicationForm()
#     #job = Jobs.query.filter_by(id=jobid).first()
#
#     # Récupération des données du formulaire sans les enregistrer dans la base de données
#     application_data = {
#         'gender': form.gender.data,
#         'degree': form.degree.data,
#         'industry': form.industry.data,
#         'experience': form.experience.data,
#         'cover_letter': form.cover_letter.data,
#         'cv_filename': form.cv.data.filename
#     }
#
#     # Traitement du CV (sauvegarde ou autre traitement sans utiliser la base de données)
#     picture_file = save_picture(form.cv.data)
#
#     # Vous pouvez ici ajouter des traitements supplémentaires ou des affichages
#     # Par exemple, afficher les données reçues ou effectuer une action sans sauvegarder
#
#     # Redirection après le traitement
#     return redirect(url_for('show_jobs'))
#
#     # Vous pouvez aussi utiliser un render_template si vous voulez afficher quelque chose à l'utilisateur
#     # return render_template('post_cvs.html', form=form, Random_Review=Random_Review)

# @app.route('/job_description', methods=['GET', 'POST'])
# def job_description():
#     if request.method == 'POST':
#         job_description = request.form['job_description']
#
#         # Charger les CV à partir du fichier CSV
#         df = pd.read_csv('resumes.csv')
#
#         job_tokens = preprocess_text(job_description)
#         job_vector = get_average_word_vector(job_tokens, model)
#
#         similarity_list = []
#         for index, row in df.iterrows():
#             resume_tokens = preprocess_text(row['Resume_str'])
#             resume_vector = get_average_word_vector(resume_tokens, model)
#             similarity_score = cosine_similarity([job_vector], [resume_vector])[0][0]
#              # Tronquer le texte du CV
#             truncated_resume_text = row['Resume_str'][:10] + '...' if len(row['Resume_str']) > 10 else row['Resume_str']
#             similarity_list.append((row['ID'], truncated_resume_text, similarity_score))
#
#         similarity_list.sort(key=lambda x: x[2], reverse=True)
#         top_resumes = similarity_list[:10]  # Garde les 10 meilleurs
#         return render_template('ranking.html', job_description=job_description, resumes=top_resumes)
#
#     return render_template('job_description.html')

if __name__ == '__main__':
    app.run(debug=True)
