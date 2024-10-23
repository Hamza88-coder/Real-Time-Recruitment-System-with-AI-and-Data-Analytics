import os
import json
import psycopg2
import traceback

# Connexion à la base de données PostgreSQL
try:
    conn = psycopg2.connect(
        dbname='football',
        user='postgres',
        password='papapapa',
        host='localhost',
        port='5432'
    )
    cursor = conn.cursor()
except psycopg2.Error as e:
    print(f"Erreur lors de la connexion à la base de données: {e}")
    exit(1)

# Fonction pour insérer les données dans la base de données
def insert_data(match, folder_name):
    try:
        # Vérifiez si 'away_team' existe dans le match
        if 'away_team' in match:
            
            cursor.execute('''
                INSERT INTO teams (team_id, team_name, team_gender, country_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (team_id) DO NOTHING
            ''', (
                match['away_team']['away_team_id'], 
                match['away_team']['away_team_name'], 
                match['away_team']['away_team_gender'], 
                match['away_team']['country']['id']
            ))
            print("Données de l'équipe à l'extérieur insérées.")

    except psycopg2.Error as e:
        print(f"Erreur lors de l'insertion des données dans le dossier '{folder_name}': {e}")
        print(f"Données de l'équipe à l'extérieur qui ont causé l'erreur: {match['away_team']}")
        print("Trace complète de l'erreur:")
        traceback.print_exc()  # Affiche la trace de l'erreur pour plus de détails
        conn.rollback()  # Annuler la transaction en cours

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
                            insert_data(match, subdir)  # Passer le nom du dossier
                    else:
                        insert_data(data, subdir)  # Passer le nom du dossier
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
