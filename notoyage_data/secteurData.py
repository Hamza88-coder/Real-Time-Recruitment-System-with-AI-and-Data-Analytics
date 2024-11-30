import pandas as pd

# Charger les fichiers Excel
data = pd.read_excel('fichier_reduit_avec_id_ville.xlsx')
secteurs_df = pd.read_excel('secteurs_avec_id.xlsx')

# Associer chaque secteur à son id_secteur
# Nous effectuons un merge (jointure) entre les deux DataFrames sur le nom du secteur
data = data.merge(secteurs_df, left_on='Secteur', right_on='nom_secteur', how='left')

# Supprimer la colonne nom_secteur puisqu'on a déjà la colonne Secteur
data.drop(columns=['nom_secteur'], inplace=True)

# Sauvegarder le DataFrame mis à jour dans un nouveau fichier Excel
data.to_excel('fichier_reduit_avec_id_secteur.xlsx', index=False)

# Afficher un aperçu des 5 premières lignes pour vérifier
print(data.head())
