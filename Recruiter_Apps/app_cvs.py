from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pandas as pd
from utils.similar_vectors import search_similar_vectors_candidat,search_similar_vectors_job
from utils.prepare_data import extract_text_from_pdf,ats_extractor,json_to_csv,generee_offres
from sentence_transformers import SentenceTransformer
import snowflake.connector
import uuid
import redis


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


if __name__ == '__main__':
    app.run(debug=True)
