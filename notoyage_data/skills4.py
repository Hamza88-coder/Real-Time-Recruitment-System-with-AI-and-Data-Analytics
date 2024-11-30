import pandas as pd

# Charger les fichiers Excel existants
skills_df = pd.read_excel('skills_output.xlsx')  # Contient 'Job Id' et 'Skill'
distinct_skills_df = pd.read_excel('distinct_skills.xlsx')  # Contient 'Skill ID' et 'Skill'

# Fusionner les deux DataFrames pour obtenir 'Skill ID' à partir du 'Skill'
merged_df = pd.merge(skills_df, distinct_skills_df, on='Skill', how='inner')

# Garder uniquement les colonnes 'Job Id' et 'Skill ID'
job_skill_df = merged_df[['Job Id', 'Skill ID']]

# Enregistrer le résultat dans un nouveau fichier Excel
output_job_skill_excel = 'job_skill_mapping.xlsx'
job_skill_df.to_excel(output_job_skill_excel, index=False)

print(f"Les données Job Id et Skill ID ont été enregistrées dans le fichier Excel : {output_job_skill_excel}")
