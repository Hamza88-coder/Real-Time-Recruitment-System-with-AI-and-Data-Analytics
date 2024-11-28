import pandas as pd
import ast

# Charger le dataset depuis le fichier Excel
data = pd.read_excel('fichier_reduit_avec_maroc.xlsx')

# Fonction pour extraire la valeur du secteur depuis la colonne "Company Profile"
def extract_sector(company_profile):
    try:
        # Convertir la chaîne de caractères en dictionnaire
        profile_dict = ast.literal_eval(company_profile)
        # Retourner la valeur du secteur
        return profile_dict.get('Sector', None)  # Renvoie None si 'Sector' n'existe pas
    except:
        return None

# Appliquer la fonction à la colonne 'Company Profile' et créer la nouvelle colonne 'Secteur'
data['Secteur'] = data['Company Profile'].apply(extract_sector)

# Sauvegarder le dataset modifié dans un nouveau fichier Excel
data.to_excel('fichier_reduit_avec_secteur.xlsx', index=False)

print("Modification terminée et les données sont sauvegardées dans 'fichier_reduit_avec_secteur.xlsx'.")
