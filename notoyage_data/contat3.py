import pandas as pd

# Charger le fichier contenant les données avec les types de contrat
data = pd.read_excel('fichier_reduit_avec_id_type_trav.xlsx')

# Charger le fichier contenant les types de contrat avec leurs identifiants
contrat_df = pd.read_excel('type_contrat_avec_id.xlsx')

# Effectuer la jointure entre les deux DataFrames sur la colonne 'contrat'
data_with_id = data.merge(contrat_df, how='left', left_on='contrat', right_on='nom_type_contrat')

# Sauvegarder le DataFrame mis à jour dans un nouveau fichier Excel
data_with_id.to_excel('fichier_reduit_avec_id_type_contrat.xlsx', index=False)

# Afficher un aperçu des 5 premières lignes pour vérifier
print(data_with_id.head())
