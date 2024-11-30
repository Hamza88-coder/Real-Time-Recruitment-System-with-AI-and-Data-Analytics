import pandas as pd

# Charger le fichier Excel
data = pd.read_excel('fichier_reduit_avec_id_type_trav.xlsx')

# Extraire les types de contrat uniques
unique_contrats = data['contrat'].dropna().unique()

# Créer un DataFrame avec l'id et le nom des types de contrat
contrat_df = pd.DataFrame({
    'id_type_contrat': range(1, len(unique_contrats) + 1),
    'nom_type_contrat': unique_contrats
})

# Sauvegarder le DataFrame dans un fichier Excel
contrat_df.to_excel('type_contrat_avec_id.xlsx', index=False)

# Afficher un aperçu des 5 premières lignes pour vérifier
print(contrat_df.head())
