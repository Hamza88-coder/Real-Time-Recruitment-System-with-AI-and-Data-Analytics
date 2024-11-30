import pandas as pd
import random

# Charger le fichier contenant les données
data = pd.read_excel('fichier_reduit_avec_contrat.xlsx')

# Charger les langues depuis un autre fichier Excel ou définir manuellement
languages = [
    {"id_lang": 1, "name": "Arabe"},
    {"id_lang": 2, "name": "Français"},
    {"id_lang": 3, "name": "Amazigh"},
    {"id_lang": 4, "name": "Anglais"},
    {"id_lang": 13, "name": "Espagnol"},

    # Ajoutez d'autres langues si nécessaire
]

# Convertir les langues en DataFrame
languages_df = pd.DataFrame(languages)

# Fonction pour assigner une langue en fonction du pays
def assign_language(country):
    if country == "Morocco":
        # 90 % Français, 10 % Anglais
        if random.random() < 0.9:
            return 2  # ID de Français
        else:
            return 4  # ID d'Anglais
    else:
        # Si le pays n'est pas spécifié, retourner une langue par défaut
        return 4  # Par exemple, ID de Arabe

# Appliquer la fonction pour créer une colonne 'id_lang'
data['id_lang'] = data['Country'].apply(assign_language)

# Créer un DataFrame pour "Job Id" et "id_lang"
output_df = data[['Job Id', 'id_lang']]

# Sauvegarder les résultats dans un fichier Excel
output_df.to_excel('job_id_languages.xlsx', index=False)

# Afficher un aperçu des données sauvegardées
print(output_df.head())
