import pandas as pd
import json

# Charger le fichier Excel
data = pd.read_excel('fichier_reduit_avec_entreprises_mises_a_jour.xlsx')

# Fonction pour extraire l'URL du champ 'Company Profile'
def extract_url(company_profile):
    try:
        # Convertir le texte JSON en dictionnaire Python
        profile = json.loads(company_profile)
        # Extraire l'URL si elle existe
        return profile.get("Website", "")  # Retourne la valeur de "Website" ou une chaîne vide si non trouvé
    except (json.JSONDecodeError, TypeError):
        # Retourne une chaîne vide en cas d'erreur de format
        return ""

# Appliquer la fonction à la colonne 'Company Profile' pour créer la nouvelle colonne 'URL'
data['URL'] = data['Company Profile'].apply(extract_url)

# Sauvegarder le fichier modifié dans un nouveau fichier Excel
data.to_excel('fichier_reduit_avec_URL.xlsx', index=False)

print("La colonne URL a été ajoutée et sauvegardée dans le fichier 'fichier_reduit_avec_URL.xlsx'.")
