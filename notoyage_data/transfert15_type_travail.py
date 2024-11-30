import pandas as pd

# Charger le fichier Excel contenant les données
data = pd.read_excel('fichier_reduit_avec_id_secteur.xlsx')

# Extraire les types de travail uniques
unique_work_types = data['Work Type'].dropna().unique()

# Créer un DataFrame avec les types de travail et leur identifiant
work_type_df = pd.DataFrame(unique_work_types, columns=['nom_type_trav'])

# Ajouter un identifiant pour chaque type de travail
work_type_df['id_type_trav'] = range(1, len(work_type_df) + 1)

# Sauvegarder le DataFrame dans un nouveau fichier Excel
work_type_df.to_excel('type_trav_avec_id.xlsx', index=False)

# Afficher un aperçu des 5 premières lignes pour vérifier
print(work_type_df.head())
