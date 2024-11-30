import pandas as pd

# Supposons que vous ayez déjà un DataFrame df contenant les colonnes 'Job Id' et 'Skill'
# Si ce n'est pas le cas, chargez votre fichier Excel :
df = pd.read_excel('skills_output.xlsx')

# Extraire les compétences uniques (distinctes) de la colonne 'Skill'
unique_skills = df['Skill'].drop_duplicates().reset_index(drop=True)

# Ajouter un identifiant unique commençant à 1
unique_skills_df = pd.DataFrame({
    'Skill ID': range(1, len(unique_skills) + 1),
    'Skill': unique_skills
})

# Enregistrer les compétences distinctes dans un nouveau fichier Excel
distinct_skills_excel_file = 'distinct_skills.xlsx'
unique_skills_df.to_excel(distinct_skills_excel_file, index=False)

print(f"Les compétences distinctes ont été enregistrées dans le fichier Excel : {distinct_skills_excel_file}")
