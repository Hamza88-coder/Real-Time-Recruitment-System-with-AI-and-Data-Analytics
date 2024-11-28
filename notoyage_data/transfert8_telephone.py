import pandas as pd

# Charger le fichier Excel
data = pd.read_excel('fichier_reduit_avec_email.xlsx')

# Fonction pour créer un téléphone à partir du Contact
def generate_telephone(row):
    contact_value = row['Contact']  # Récupérer la valeur de la colonne Contact
    if contact_value:
        # Limiter à 20 caractères
        telephone_value = contact_value[:20]  # Prendre uniquement les 20 premiers caractères
        return telephone_value
    return ""  # Retourner une chaîne vide si le champ Contact est vide

# Appliquer la fonction à chaque ligne du DataFrame pour créer la colonne 'telephone'
data['telephone'] = data.apply(generate_telephone, axis=1)

# Sauvegarder le fichier modifié dans un nouveau fichier Excel
data.to_excel('fichier_reduit_avec_telephone.xlsx', index=False)

print("La colonne telephone a été ajoutée et sauvegardée dans le fichier 'fichier_reduit_avec_telephone.xlsx'.")
