from datetime import datetime
import threading
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import HuggingFaceHub
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from recruitboot.ingest import get_text_chunks, get_vectorstore
from utils.similar_vectors import search_similar_vectors_candidat
from utils.prepare_data import ats_extractor,json_to_csv
from recruitboot.retrieval_generation import create_conversation_chain
from recruitboot.converteur import get_pdf_text
from flask import Flask, render_template, request, redirect, url_for, flash


import pandas as pd
from sentence_transformers import SentenceTransformer
import redis





# Traitement du PDF
pdf_docs = [r"data\hamza.pdf"]
text = get_pdf_text(pdf_docs)
chunks = get_text_chunks(text)
vectorstore = get_vectorstore(chunks)

# Création de la chaîne de conversation
conversation_chain = create_conversation_chain(vectorstore)
app = Flask(__name__)

app.config['REDIS_URL'] = "redis://localhost:6379/0"  # Utilisez l'URL de votre instance Redis
# Définir une clé secrète pour la session
app.secret_key = 'said'

# Connexion à Redis
redis_client = redis.StrictRedis.from_url(app.config['REDIS_URL'])

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
def index():
    return render_template('chat.html')

@app.route('/chatbot_key/<key>', methods=['GET', 'POST'])
def chatbot_key(key):
    return f"9alib 3liha"+key


@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    input = msg  # Le message utilisateur
    try:
        # Appel à invoke() pour obtenir la réponse
        result = conversation_chain.invoke({"question": input})
        print("Response: ", result)

        # Retourner uniquement la réponse textuelle sans l'objet complet
        answer = result["answer"] if "answer" in result else "Désolé, je n'ai pas pu trouver une réponse."

        return jsonify({"response": answer})  # Retourner la réponse du chatbot
    except Exception as e:
        print("Error: ", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
