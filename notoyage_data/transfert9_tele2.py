import pandas as pd
import random

# Charger le fichier Excel
data = pd.read_excel('fichier_reduit_avec_telephone.xlsx')


# Fonction pour générer un numéro marocain fictif
def generate_moroccan_phone_number():
    # Générer un numéro marocain au format +212 6XX XXX XXX
    first_part = "+212 6"
    second_part = str(random.randint(100, 999))  # Trois chiffres pour la seconde partie
    third_part = str(random.randint(100, 999))  # Trois chiffres pour la troisième partie
    fourth_part = str(random.randint(100, 999))  # Trois chiffres pour la quatrième partie
    return f"{first_part}{second_part} {third_part} {fourth_part}"


# Fonction pour mettre à jour la colonne telephone
def update_telephone(row):
    contact_value = row['Contact']  # Récupérer la valeur de la colonne Contact
    country_value = row['Country']  # Récupérer la valeur de la colonne Country

    if country_value == "Morocco":
        # Si le pays est le Maroc, remplacer le téléphone par un numéro marocain
        return generate_moroccan_phone_number()
    else:
        # Si le pays n'est pas le Maroc, limiter la valeur à 20 caractères
        if contact_value:
            return contact_value[:20]  # Prendre uniquement les 20 premiers caractères
        return ""  # Retourner une chaîne vide si le champ Contact est vide


# Appliquer la fonction à chaque ligne du DataFrame pour créer la colonne 'telephone'
data['telephone'] = data.apply(update_telephone, axis=1)

# Sauvegarder le fichier modifié dans un nouveau fichier Excel
data.to_excel('fichier_reduit_avec_telephone_mise_a_jour.xlsx', index=False)

print(
    "La colonne 'telephone' a été mise à jour et sauvegardée dans le fichier 'fichier_reduit_avec_telephone_mise_a_jour.xlsx'.")
