import csv

from groq import Groq
import re
import uuid
import os
import json
import fitz  # PyMuPDF
def ats_extractor(resume_data):
    api_key_grouq = "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"
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
    api_key_grouq = "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"
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
