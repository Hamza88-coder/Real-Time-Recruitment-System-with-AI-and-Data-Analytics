import json
import pandas as pd

# Charger les données JSON à partir du fichier
input_json_file = 'extracted_skills.json'  # Remplacez par le nom de votre fichier JSON
with open(input_json_file, 'r') as file:
    json_data = json.load(file)

# Créer une liste pour stocker les données structurées
data = []

# Parcourir chaque entrée dans le fichier JSON
for entry in json_data:
    job_id = entry["Job Id"]
    skills = entry["Skills"]

    # Omettre les deux premiers skills et le dernier
    filtered_skills = skills[2:-1]  # Exclut les deux premiers et le dernier

    # Ajouter chaque skill avec l'ID correspondant à la liste de données
    for skill in filtered_skills:
        data.append({"Job Id": job_id, "Skill": skill})

# Créer un DataFrame pandas à partir des données
df = pd.DataFrame(data)

# Enregistrer les données dans un fichier Excel
output_excel_file = 'skills_output.xlsx'
df.to_excel(output_excel_file, index=False)

print(f"Les données ont été transférées dans le fichier Excel : {output_excel_file}")
