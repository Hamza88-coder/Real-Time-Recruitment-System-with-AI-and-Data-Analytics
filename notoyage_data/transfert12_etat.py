import pandas as pd

# Charger le fichier Excel contenant les données
data = pd.read_excel('fichier_reduit_avec_contrat.xlsx')

# Extraire la colonne "Country" et supprimer les doublons
unique_countries = data['Country'].drop_duplicates().reset_index(drop=True)

# Générer un DataFrame avec id_etat et nom de l'état
unique_countries_df = pd.DataFrame({
    'id_etat': range(1, len(unique_countries) + 1),  # Générer des ID uniques
    'nom_etat': unique_countries
})

# Sauvegarder le DataFrame dans un fichier Excel
unique_countries_df.to_excel('unique_countries.xlsx', index=False)

# Afficher un aperçu des résultats
print(unique_countries_df.head())
