import pandas as pd

# Charger le fichier Excel
data = pd.read_excel('fichier_reduit_avec_URL_mis_a_jour.xlsx')

# Fonction pour générer l'email
def generate_email(row):
    # Extraire le prénom et le nom de la colonne 'Contact Person'
    contact_person = row['Contact Person']
    if contact_person:  # Si la personne de contact n'est pas vide
        name_parts = contact_person.split()  # Séparer le prénom et le nom
        first_name = name_parts[0].lower()  # Prénom en minuscules
        last_name = name_parts[-1].lower()  # Nom en minuscules
        # Extraire le nom de l'entreprise
        company_name = row['Company'].replace(" ", "_").lower()  # Remplacer les espaces par des underscores et mettre en minuscules
        # Créer l'email
        email = f"{first_name}.{last_name}@{company_name}.com"
        return email
    return ""  # Retourner une chaîne vide si le champ Contact Person est vide

# Appliquer la fonction à chaque ligne du DataFrame pour créer la colonne 'email'
data['email'] = data.apply(generate_email, axis=1)

# Sauvegarder le fichier modifié dans un nouveau fichier Excel
data.to_excel('fichier_reduit_avec_email.xlsx', index=False)

print("La colonne email a été ajoutée et sauvegardée dans le fichier 'fichier_reduit_avec_email.xlsx'.")
