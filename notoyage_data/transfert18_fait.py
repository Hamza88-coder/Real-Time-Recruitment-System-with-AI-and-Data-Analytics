import pandas as pd

# Charger le fichier existant
data = pd.read_csv('fichier_valide.csv')

# Sélectionner les colonnes souhaitées et renommer si nécessaire
fields_to_keep = {
    'Job Id': 'Job Id',              # Garder la colonne Job ID
    'id_type_contrat': 'id_type_contrat',  # Garder la colonne id_type_contrat
    'id_company': 'id_company',          # Garder la colonne id_company
    'id_type_trav': 'id_type_trav',      # Garder la colonne id_type_trav
    'salaire': 'salaire',                 # Renommer Salary en salaire
    'Experience': 'Experience',          # Garder la colonne Experience
    'email': 'email_offre'               # Renommer Email en email_offre
}

new_data = data[list(fields_to_keep.keys())].rename(columns=fields_to_keep)

# Convertir la colonne 'salaire' en un nombre décimal
new_data['salaire'] = (
    new_data['salaire']  # Travailler sur la colonne salaire
    .replace({',': ''}, regex=True)  # Supprimer les virgules
    .astype(float)  # Convertir en nombre décimal
)

# Sauvegarder le nouveau fichier Excel
new_data.to_csv('offres_emploi_filtrees2.csv', index=False)

# Afficher un aperçu des premières lignes
print(new_data.head())
