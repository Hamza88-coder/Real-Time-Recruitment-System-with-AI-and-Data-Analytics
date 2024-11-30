import pandas as pd

# Charger le fichier contenant les données d'origine
data = pd.read_excel('fichier_reduit_avec_contrat.xlsx')

# Charger le fichier contenant la correspondance des pays avec les ID
unique_countries = pd.read_excel('unique_countries.xlsx')

# Fusionner les deux fichiers pour ajouter la colonne id_etat à data
data_with_ids = data.merge(unique_countries, how='left', left_on='Country', right_on='nom_etat')

# Supprimer la colonne "nom_etat" si elle est inutile
data_with_ids = data_with_ids.drop(columns=['nom_etat'])

# Sauvegarder le nouveau fichier avec la colonne id_etat ajoutée
data_with_ids.to_excel('fichier_reduit_avec_id_etat.xlsx', index=False)

# Afficher un aperçu des résultats
print(data_with_ids.head())
