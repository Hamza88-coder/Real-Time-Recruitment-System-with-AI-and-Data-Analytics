import pandas as pd

# Charger le fichier contenant les données avec id_etat
data = pd.read_excel('fichier_reduit_avec_id_etat.xlsx')

# Charger le fichier des villes avec id_ville et id_etat
cities = pd.read_excel('villes_avec_id.xlsx')

# Fusionner les données pour ajouter la colonne id_ville
# en utilisant 'Location' et 'id_etat' comme clé de correspondance
merged_data = pd.merge(data, cities, how='left', left_on=['location', 'id_etat'], right_on=['nom_ville', 'id_etat'])

# Supprimer la colonne 'nom_ville' utilisée uniquement pour la correspondance
merged_data.drop(columns=['nom_ville'], inplace=True)

# Sauvegarder le fichier final avec la nouvelle colonne 'id_ville'
merged_data.to_excel('fichier_reduit_avec_id_ville.xlsx', index=False)

# Afficher un aperçu des 5 premières lignes pour vérification
print(merged_data.head())
