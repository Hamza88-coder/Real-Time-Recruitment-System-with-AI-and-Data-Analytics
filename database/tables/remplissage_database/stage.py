import os
import json
import psycopg2

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
def insert_data(match, folder_name):
    try:# Insérer les données du match
        cursor.execute('''
            INSERT INTO competition_stage (id, name)
            VALUES (%s, %s)
            ON CONFLICT (id) DO NOTHING
        ''', (match['competition_stage']['id'], match['competition_stage']["name"]))

  

    except KeyError as e:
        print(f"Erreur lors de l'insertion des données pour le match {match['match_id']} dans le dossier {folder_name}: clé manquante {e}")
        conn.rollback()  # Annuler la transaction
    except psycopg2.Error as e:
        print(f"Erreur SQL lors de l'insertion des données pour le match {match['match_id']} dans le dossier {folder_name}: {e}")
        conn.rollback()  # Annuler la transaction
    else:
        conn.commit()  # Valider la transaction

# Chemin vers le dossier contenant les sous-dossiers
main_folder = r'C:\Users\HP\OneDrive\Desktop\bigData_project\matches'

# Parcours des sous-dossiers et des fichiers JSON
for subdir, dirs, files in os.walk(main_folder):
    folder_name = os.path.basename(subdir)  # Récupérer le nom du dossier actuel
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(subdir, file)
            with open(file_path, 'r', encoding='utf-8') as json_file:
                try:
                    data = json.load(json_file)
                    # Vérifiez si les données sont dans une liste, sinon créez une liste avec un seul élément
                    if isinstance(data, list):
                        for match in data:
                            insert_data(match, folder_name)
                    else:
                        insert_data(data, folder_name)
                except json.JSONDecodeError as e:
                    print(f"Erreur lors de la lecture du fichier {file_path} dans le dossier {folder_name}: {e}")

# Fermeture de la connexion
cursor.close()
conn.close()
