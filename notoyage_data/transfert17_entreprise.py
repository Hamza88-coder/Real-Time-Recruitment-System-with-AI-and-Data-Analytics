import pandas as pd

# Charger le fichier Excel
data = pd.read_csv('salaries_max_convertis.csv')

# Supprimer les doublons par entreprise et conserver les premières occurrences de chaque entreprise
unique_companies = data.drop_duplicates(subset=['Company'])

# Créer un DataFrame avec les informations demandées
company_data = unique_companies[['Company', 'email', 'URL', 'telephone', 'id_secteur', 'id_ville']].copy()

# Renommer les colonnes pour correspondre au format demandé
company_data.rename(columns={
    'Company': 'nom_company',
    'email': 'email',
    'URL': 'URL',
    'telephone': 'telephone'
}, inplace=True)

# Ajouter un identifiant unique pour chaque entreprise
company_data['id_company'] = range(1, len(company_data) + 1)

# Réorganiser les colonnes pour l'ordre souhaité
company_data = company_data[['id_company', 'nom_company', 'email', 'URL', 'telephone', 'id_secteur', 'id_ville']]

# Sauvegarder les informations dans un nouveau fichier Excel
company_data.to_csv('entreprises_avec_id.csv', index=False)

# Afficher un aperçu des 5 premières lignes pour vérifier
print(company_data.head())
