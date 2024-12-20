import threading
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import HuggingFaceHub
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from ecommbot.ingest import get_text_chunks, get_vectorstore

from ecommbot.retrieval_generation import create_conversation_chain
from ecommbot.converteur import get_pdf_text

app = Flask(__name__)

load_dotenv()

# Fonction de génération de la chaîne conversationnelle (pour intégrer LangChain)


# Traitement du PDF
pdf_docs = [r"C:\Users\HP\OneDrive\Desktop\bigData_project\E-Commerce-Chatbot\data\hamza.pdf"]
text = get_pdf_text(pdf_docs)
chunks = get_text_chunks(text)
vectorstore = get_vectorstore(chunks)

# Création de la chaîne de conversation
conversation_chain = create_conversation_chain(vectorstore)

@app.route("/")
def index():
    return render_template('chat.html')

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
    # Lancer l'application Flask en mode débogage
    app.run(debug=True)
