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
    try:
        # Insérer les données du match, en utilisant .get() pour fournir 'None' si la clé n'existe pas
        cursor.execute('''
            INSERT INTO matches (match_id, match_date, kick_off, competition_id, season_id, home_team_id, away_team_id, home_score, away_score, match_status, match_status_360, match_week, stadium_id, competition_stage_id, referee_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (match_id) DO NOTHING
        ''', (
            match.get('match_id', None),
            match.get('match_date', None),
            match.get('kick_off', None),
            match.get("competition", {}).get("competition_id", None),
            match.get('season', {}).get('season_id', None),
            match.get('home_team', {}).get('home_team_id', None),
            match.get('away_team', {}).get('away_team_id', None),
            match.get('home_score', None),
            match.get('away_score', None),
            match.get('match_status', None),
            match.get('match_status_360', None),
            match.get('match_week', None),
            match.get('stadium', {}).get('id', None),
            match.get('competition_stage', {}).get('id', None),
            match.get('referee', {}).get('id', None)
        ))

    except KeyError as e:
        print(f"Erreur lors de l'insertion des données pour le match {match.get('match_id', 'ID non disponible')} dans le dossier {folder_name}: clé manquante {e}")
        conn.rollback()  # Annuler la transaction
    except psycopg2.Error as e:
        print(f"Erreur SQL lors de l'insertion des données pour le match {match.get('match_id', 'ID non disponible')} dans le dossier {folder_name}: {e}")
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
