import pandas as pd

# Charger les fichiers nécessaires
data = pd.read_csv('salaries_max_convertis.csv')  # Le fichier principal
companies = pd.read_csv('entreprises_avec_id.csv')  # Le fichier avec id_company

# Fusionner les deux fichiers pour ajouter la colonne id_company
# Fusionner sur la colonne "Company" (nom_company dans le fichier entreprises)
data_with_company_id = pd.merge(data, companies[['id_company', 'nom_company']],
                                left_on='Company', right_on='nom_company',
                                how='left')

# Supprimer la colonne "nom_company" ajoutée par la fusion pour éviter la redondance
data_with_company_id.drop(columns=['nom_company'], inplace=True)

# Sauvegarder le résultat dans un nouveau fichier Excel
data_with_company_id.to_csv('fichier_valide.csv', index=False)

# Afficher un aperçu des 5 premières lignes pour vérifier
print(data_with_company_id.head())
