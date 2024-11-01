# Import libraries
from groq import Groq
import yaml
import fitz
import json
import re

# PyMuPDF

# Configuration
CONFIG_PATH = r"config.yaml"
api_key = None

# Load the API key from YAML configuration file
with open(CONFIG_PATH) as file:
    data = yaml.load(file, Loader=yaml.FullLoader)
    api_key = data['GROQ_API_KEY']


def ats_extractor(resume_data):
    # Prompt for extracting resume information
    prompt = '''
    You are an AI bot designed to act as a professional for parsing resumes. You are given a resume, and your job is to extract the following information:
    1. first name
    2. last name
    1. full name
    4. title
    5. address
    6. objective
    7. date_of_birth
    8. place_of_birth
    9. phones
    10. urls
    11. gender
    12. nationality
    13. education details
    14. total years education
    15. experience details
    16. total years experience
    17. skills
    18. projects
    19. languages
    20. certifications 
    Provide the extracted information in JSON format only,If a field does not exist, do "None".
    Expected example:
    {
  "first_name": "Le prénom du candidat.",
  "last_name": "Le nom de famille du candidat.",
  "full_name": "Le nom complet du candidat (prénom et nom).",
  "title": "Titre professionnel du candidat (ex: Stagiare, Ingénieur, Développeur).",
  "address": {
       "formatted_location": "Adresse complète du candidat au format texte.",
       "city": "Ville de résidence du candidat.",
       "region": "Région de résidence du candidat.",
       "country": "Pays de résidence du candidat.",
       "postal_code": "Code postal de l’adresse du candidat."
  },
  "objective": "Objectif de carrière ou déclaration personnelle du candidat.",
  "date_of_birth": "Date de naissance du candidat (format AAAA-MM-JJ).",
  "place_of_birth": "Lieu de naissance du candidat (ville, région, pays).",
  "phones": "Liste des numéros de téléphone du candidat.",
  "email": "Adresse email principale du candidat.",
  "urls": {
       "GitHub": "Lien vers le profil GitHub du candidat.",
       "portfolio": "Lien vers le portfolio en ligne du candidat.",
       "LinkedIn": "Lien vers le profil LinkedIn du candidat.",
       "site_web": "Lien vers le site web personnel ou professionnel du candidat."
  },
  "gender": "Genre du candidat (ex: masculin, féminin).",
  "nationality": "Nationalité ou citoyenneté du candidat.",
  "education_details": [ (liste des etude de condidat)
    {
      "etude_title": "Titre ou diplôme obtenu (ex: Licence, Master, Doctorat).",
      "etablissement_name": "Nom de l’établissement d’enseignement.",
      "start_date": "Date de début des études (format AAAA-MM-JJ).",
      "end_date": "Date de fin des études ou date prévue de fin (format AAAA-MM-JJ).",
      "etude_city": "Ville où les études ont été effectuées.",
      "etude_region": "Région où les études ont été effectuées.",
      "etude_contry": "Pays où les études ont été effectuées."
    }
  ],
  "total_years_education": "Nombre total d'années de formation du candidat (ex 2.5 ce signifiee 2 annees et demi annee).",
  "work_experience_details": [(liste des experience de condidat)
    {
      "job_title": "Intitulé du poste occupé.",
      "company_name": "Nom de l’entreprise ou de l’organisation.",
      "city": "Ville où l’emploi a été exercé.",
      "region": "Région où l’emploi a été exercé.",
      "sector_of_activity": "Secteur d’activité de l’entreprise.",
      "start_date": "Date de début du poste (format AAAA-MM-JJ).",
      "end_date": "Date de fin du poste ou « actuel » pour les postes en cours."
    }
  ],
  "total_years_work_experience": "Nombre total d'années d’expérience professionnelle.",
  "skills": [
    "Liste des compétences et technologies maitrisées par le candidat (ex: Java, gestion de projet)."
  ],
  "projects":[(liste de projetcs){
      "name":
      "outils":[liste de outils utilisee dans ce projet]
}]
  "language": [
    {
      "name": "Nom de la langue parlée (ex: anglais, français).",
      "level": "Niveau de maîtrise de la langue (ex: débutant, intermédiaire, avancé, bilingue)."
    }
  ],
  "certifications": [
    {
      "name": "Nom de la certification obtenue.",
      "etablissement_certification": "Nom de l’organisme délivrant la certification.",
      "date": "Date d’obtention de la certification (format AAAA-MM-JJ)."
    }
  ]
}

    '''

    # Initialize the Groq API client
    groq_client = Groq(api_key=api_key)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": resume_data}
    ]

    # Generate the response
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.0,
        max_tokens=1500)

    data = response.choices[0].message.content
    try:
        json_match = re.search(r"\{.*\}", data, re.DOTALL)  # Trouver le JSON entre accolades
        if json_match:
            json_data = json.loads(json_match.group(0))  # Charger le JSON
            return json_data
        else:
            return {"error": "JSON non trouvé dans la sortie."}
    except json.JSONDecodeError as e:
        return {"error": f"Erreur de décodage JSON : {e}"}

    # Return the extracted information


def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    text = ""

    # Extract text from each page
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")

    return text


# Path to your resume PDF
pdf_path = "10674770.pdf"

# Extract text from the PDF
resume_text = extract_text_from_pdf(pdf_path)

# Pass the extracted text to the ats_extractor function
extracted_info = ats_extractor(resume_text)

# Display the extracted information
print(extracted_info)
