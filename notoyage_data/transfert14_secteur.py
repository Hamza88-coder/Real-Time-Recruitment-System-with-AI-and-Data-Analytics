import pandas as pd

# Charger le fichier contenant les données avec id_ville
data = pd.read_excel('fichier_reduit_avec_id_ville.xlsx')

# Extraire les secteurs uniques
secteurs_uniques = data['Secteur'].dropna().unique()

# Créer un DataFrame avec un id pour chaque secteur unique
secteurs_df = pd.DataFrame({
    'id_secteur': range(1, len(secteurs_uniques) + 1),
    'nom_secteur': secteurs_uniques
})

# Sauvegarder le fichier avec les secteurs et leurs identifiants
secteurs_df.to_excel('secteurs_avec_id.xlsx', index=False)

# Afficher un aperçu des secteurs générés pour vérification
print(secteurs_df.head())
