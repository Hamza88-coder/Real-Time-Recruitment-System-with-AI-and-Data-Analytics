import os
import json
import psycopg2
import traceback

# Connexion à la base de données PostgreSQL
conn = psycopg2.connect(
    dbname='football',
    user='postgres',
    password='papapapa',
    host='localhost',
    port='5432'
)
cursor = conn.cursor()

# Fonction pour insérer les données dans la base de données
def insert_data(match):
    try:
        # Insérer les données du pays
        cursor.execute('''
            INSERT INTO countries (country_id, name)
            VALUES (%s, %s)
            ON CONFLICT (country_id) DO NOTHING
        ''', (match['home_team']['country']['id'], match['home_team']['country']['name']))
        
        # Insérer les données de la saison
        cursor.execute('''
            INSERT INTO seasons (season_id, season_name)
            VALUES (%s, %s)
            ON CONFLICT (season_id) DO NOTHING
        ''', (match['season']['season_id'], match['season']['season_name']))
    
    except Exception as e:
        # Afficher l'erreur et la trace complète pour comprendre le problème
        print(f"Erreur lors de l'insertion des données pour le match {match['match_id']}:")
        print(f"Type d'erreur: {type(e).__name__}")
        print(f"Message d'erreur: {e}")
        print("Trace complète de l'erreur:")
        traceback.print_exc()  # Affiche la trace complète de l'erreur

# Chemin vers le dossier contenant les sous-dossiers
main_folder = r'C:\Users\HP\OneDrive\Desktop\bigData_project\matches'

# Parcours des sous-dossiers et des fichiers JSON
for subdir, dirs, files in os.walk(main_folder):
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(subdir, file)
            with open(file_path, 'r', encoding='utf-8') as json_file:
                try:
                    data = json.load(json_file)
                    # Vérifiez si les données sont dans une liste, sinon créez une liste avec un seul élément
                    if isinstance(data, list):
                        for match in data:
                            insert_data(match)
                    else:
                        insert_data(data)
                except json.JSONDecodeError as e:
                    print(f"Erreur lors de la lecture du fichier {file_path}: {e}")

# Validation des changements et fermeture de la connexion
conn.commit()
cursor.close()
conn.close()
