from PyPDF2 import PdfReader
import os

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        # Vérifiez si le chemin du fichier PDF est valide
        if not os.path.exists(pdf):
            print(f"Le fichier {pdf} n'existe pas.")
            continue  # Passez au fichier suivant si celui-ci n'existe pas
        
        try:
            pdf_reader = PdfReader(pdf)
            # Parcourir toutes les pages du PDF et extraire le texte
            for page in pdf_reader.pages:
                text += page.extract_text()  # Extraire le texte de chaque page
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier {pdf}: {e}")
    
    return text

if __name__ == "__main__":
    pdf_docs = [r"C:\Users\HP\OneDrive\Desktop\bigData_project\E-Commerce-Chatbot\data\hamza.pdf"]
    text = get_pdf_text(pdf_docs)
    print(text)
