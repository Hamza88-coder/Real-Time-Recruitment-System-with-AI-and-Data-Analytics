import pandas as pd

# Charger le fichier contenant les données avec id_etat
data = pd.read_excel('fichier_reduit_avec_id_etat.xlsx')

# Extraire les colonnes 'Location' et 'id_etat'
cities = data[['location', 'id_etat']].drop_duplicates()

# Supprimer les lignes où 'Location' est vide ou NaN
cities = cities.dropna(subset=['location'])

# Générer un id_ville unique pour chaque ville
cities['id_ville'] = range(1, len(cities) + 1)

# Réorganiser les colonnes
cities = cities[['id_ville', 'id_etat', 'location']]

# Renommer les colonnes pour plus de clarté
cities.rename(columns={'location': 'nom_ville'}, inplace=True)

# Sauvegarder le nouveau fichier contenant les villes
cities.to_excel('villes_avec_id.xlsx', index=False)

# Afficher un aperçu du résultat
print(cities.head())
