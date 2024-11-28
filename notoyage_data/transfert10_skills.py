import pandas as pd
import yaml
import json
from groq import Groq  # Assurez-vous que l'API Groq est correctement installée et accessible.

# Configuration
CONFIG_PATH = r"config.yaml"
api_key = None

# Load the API key from YAML configuration file
with open(CONFIG_PATH) as file:
    data = yaml.load(file, Loader=yaml.FullLoader)
    api_key = data['GROQ_API_KEY']

# Initialize the Groq API client
groq_client = Groq(api_key=api_key)


def ats_extractor(text):
    # Prompt for extracting skills information
    prompt = """
    You are an AI assistant. Your task is to extract a list of skills mentioned in the text provided by the user. 
    Please list the skills you can identify, separating them with commas.
    """

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text}
    ]

    # Generate the response
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.0,
        max_tokens=1500
    )

    # Extract skills from the response
    skills = response.choices[0].message.content.strip()
    return [skill.strip() for skill in skills.split(',')]


# Read the Excel file
excel_file_path = 'fichier_reduit_avec_contrat.xlsx'  # Remplacez par le chemin de votre fichier Excel
data = pd.read_excel(excel_file_path)

# Create a list to store JSON data
json_data = []

# Iterate over the rows in the Excel file
for index, row in data.iterrows():
    job_id = row['Job Id']
    skills_text = row['skills']

    # Extract skills using the ats_extractor function
    skills_list = ats_extractor(skills_text)

    # Append data to JSON structure
    json_data.append({
        "Job Id": job_id,
        "Skills": skills_list
    })

# Write the JSON data to a file
output_json_file = 'extracted_skills.json'
with open(output_json_file, 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

print(f"Les compétences extraites ont été sauvegardées dans {output_json_file}")
