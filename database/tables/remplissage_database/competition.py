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
        # Insérer les données de la compétition
        cursor.execute('''
            INSERT INTO competitions (competition_id, country_name, competition_name)
            VALUES (%s, %s, %s)
            ON CONFLICT (competition_id) DO NOTHING
        ''', (match['competition']['competition_id'], match['competition']['country_name'], match['competition']['competition_name']))
        print("Données de la compétition insérées.")

        

    except Exception as e:
        print(f"Erreur lors de l'insertion des données: {e}")
        print("Trace complète de l'erreur:")
        traceback.print_exc()  # Affiche la trace de l'erreur pour plus de détails

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
try:
    conn.commit()
except Exception as e:
    print(f"Erreur lors de la validation des changements: {e}")
    conn.rollback()  # Annuler les modifications en cas d'erreur
finally:
    cursor.close()
    conn.close()
