import pandas as pd

# Charger les fichiers Excel
data = pd.read_excel('fichier_reduit_avec_id_secteur.xlsx')
work_type_df = pd.read_excel('type_trav_avec_id.xlsx')

# Fusionner les deux DataFrames sur la colonne 'Work Type' pour ajouter 'id_type_trav'
merged_data = pd.merge(data, work_type_df, how='left', left_on='Work Type', right_on='nom_type_trav')

# Sauvegarder le fichier mis à jour dans un nouveau fichier Excel
merged_data.to_excel('fichier_reduit_avec_id_type_trav.xlsx', index=False)

# Afficher un aperçu des 5 premières lignes pour vérifier
print(merged_data.head())
