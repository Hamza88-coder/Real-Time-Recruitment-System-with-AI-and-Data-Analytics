# Extraire les données de Snowflake
import snowflake.connector
import pandas as pd

# Détails de connexion à Snowflake
account = "phztxrc-go36107"
user = "SAID"
password = "SaidKHALID2002!"
role = "dev_role"
warehouse = "projet_warehouse"
database = "my_project_database"
schema = "my_project_schema"

# Connexion à Snowflake
conn = snowflake.connector.connect(
    account=account,
    user=user,
    password=password,
    role=role,
    warehouse=warehouse,
    database=database,
    schema=schema
)

# Requête pour les offres
query_offres = """
 SELECT o.offre_id,
        LISTAGG(DISTINCT cmp.nom, ', ') AS competences,
        LISTAGG(DISTINCT lng.nom, ', ') AS langues,
        f.nom AS formation,
        o.experience_dur
 FROM my_project_database.my_project_schema.offre_fait o
 JOIN my_project_database.my_project_schema.offre_comp oc ON o.offre_id = oc.offre_id
 JOIN my_project_database.my_project_schema.competence cmp ON oc.competence_id = cmp.competence_id
 LEFT JOIN my_project_database.my_project_schema.langue_offr lo ON o.offre_id = lo.offre_id
 LEFT JOIN my_project_database.my_project_schema.langue lng ON lo.langue_id = lng.langue_id
 LEFT JOIN my_project_database.my_project_schema.formation f ON o.formation_id = f.formation_id
 GROUP BY o.offre_id, f.nom, o.experience_dur
"""

# Requête pour les candidats
query_candidats = """
 SELECT c.candidat_id,
        LISTAGG(DISTINCT cmp.nom, ', ') AS competences,
        LISTAGG(DISTINCT lng.nom, ', ') AS langues,
        f.nom AS formation,
        c.nbr_years_exp
 FROM my_project_database.my_project_schema.candidat_fait c
 LEFT JOIN my_project_database.my_project_schema.candidat_comp cc ON c.candidat_id = cc.candidat_id
 LEFT JOIN my_project_database.my_project_schema.competence cmp ON cc.competence_id = cmp.competence_id
 LEFT JOIN my_project_database.my_project_schema.langue_cand lc ON c.candidat_id = lc.candidat_id
 LEFT JOIN my_project_database.my_project_schema.langue lng ON lc.langue_id = lng.langue_id
 LEFT JOIN my_project_database.my_project_schema.formation f ON c.formation_id = f.formation_id
 GROUP BY c.candidat_id, f.nom, c.nbr_years_exp
"""

# Exécution des requêtes et transfert des résultats dans des DataFrames
try:
    df_offres = pd.read_sql(query_offres, conn)
    print("Données des offres chargées avec succès.")
    print(df_offres.head())  # Affiche un aperçu des premières lignes
    print(df_offres.columns)

    df_candidats = pd.read_sql(query_candidats, conn)
    print("Données des candidats chargées avec succès.")
    print(df_candidats.head())  # Affiche un aperçu des premières lignes
    df_candidats = df_candidats.sample(frac=0.5, random_state=42)
    print('2',df_candidats.head())
    print(df_candidats.columns)

except Exception as e:
    print("Erreur lors de l'exécution des requêtes :", e)
finally:
    # Fermeture de la connexion
    conn.close()
    print("Connexion à Snowflake fermée.")

# from sqlalchemy import create_engine
# import pandas as pd
#
# # Chaîne de connexion SQLAlchemy
# engine = create_engine(
#     'snowflake://SAID:SaidKHALID2002!@phztxrc-go36107.snowflakecomputing.com/my_project_database/my_project_schema?role=dev_role&warehouse=projet_warehouse'
# )
#
# # Établir une connexion explicite à partir de l'objet engine
# with engine.connect() as connection:
#     # Charger les données des offres
#     query_offres = """
#     SELECT o.offre_id,
#            LISTAGG(DISTINCT cmp.nom, ', ') AS competences,
#            LISTAGG(DISTINCT lng.nom, ', ') AS langues,
#            f.nom AS formation,
#            o.experience_dur
#     FROM my_project_database.my_project_schema.offre_fait o
#     JOIN my_project_database.my_project_schema.offre_comp oc ON o.offre_id = oc.offre_id
#     JOIN my_project_database.my_project_schema.competence cmp ON oc.competence_id = cmp.competence_id
#     LEFT JOIN my_project_database.my_project_schema.langue_offr lo ON o.offre_id = lo.offre_id
#     LEFT JOIN my_project_database.my_project_schema.langue lng ON lo.langue_id = lng.langue_id
#     LEFT JOIN my_project_database.my_project_schema.formation f ON o.formation_id = f.formation_id
#     GROUP BY o.offre_id, f.nom, o.experience_dur
#     """
#     df_offres = pd.read_sql(query_offres, connection)
#
#     # Charger les données des candidats
#     query_candidats = """
#     SELECT c.candidat_id,
#            LISTAGG(DISTINCT cmp.nom, ', ') AS competences,
#            LISTAGG(DISTINCT lng.nom, ', ') AS langues,
#            f.nom AS formation,
#            c.nbr_years_exp
#     FROM my_project_database.my_project_schema.candidat_fait c
#     LEFT JOIN my_project_database.my_project_schema.candidat_comp cc ON c.candidat_id = cc.candidat_id
#     LEFT JOIN my_project_database.my_project_schema.competence cmp ON cc.competence_id = cmp.competence_id
#     LEFT JOIN my_project_database.my_project_schema.langue_cand lc ON c.candidat_id = lc.candidat_id
#     LEFT JOIN my_project_database.my_project_schema.langue lng ON lc.langue_id = lng.langue_id
#     LEFT JOIN my_project_database.my_project_schema.formation f ON c.formation_id = f.formation_id
#     GROUP BY c.candidat_id, f.nom, c.nbr_years_exp
#     """
#     df_candidats = pd.read_sql(query_candidats, connection)
#
# # Afficher les DataFrames pour vérification
# print("Offres :")
# print(df_offres.head())
# print("\nCandidats :")
# print(df_candidats.head())

# Étape 2 : Générer des embeddings pour les offres et les candidats
from sentence_transformers import SentenceTransformer


# Charger le modèle avec support GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
# Trier les compétences et les langues pour chaque offre
df_offres['COMPETENCES'] = df_offres['COMPETENCES'].apply(lambda x: ', '.join(sorted(x.split(', '))) if pd.notnull(x) else '')
df_offres['LANGUES'] = df_offres['LANGUES'].apply(lambda x: ', '.join(sorted(x.split(', '))) if pd.notnull(x) else '')

# Trier les compétences et les langues pour chaque candidat
df_candidats['COMPETENCES'] = df_candidats['COMPETENCES'].apply(lambda x: ', '.join(sorted(x.split(', '))) if pd.notnull(x) else '')
df_candidats['LANGUES'] = df_candidats['LANGUES'].apply(lambda x: ', '.join(sorted(x.split(', '))) if pd.notnull(x) else '')
# Uniformiser la casse pour les compétences, langues, formation, etc.
df_offres['COMPETENCES'] = df_offres['COMPETENCES'].str.lower()
df_offres['LANGUES'] = df_offres['LANGUES'].str.lower()
df_offres['FORMATION'] = df_offres['FORMATION'].str.lower()

df_candidats['COMPETENCES'] = df_candidats['COMPETENCES'].str.lower()
df_candidats['LANGUES'] = df_candidats['LANGUES'].str.lower()
df_candidats['FORMATION'] = df_candidats['FORMATION'].str.lower()


# Supprimer les doublons dans les compétences et langues
df_offres['COMPETENCES'] = df_offres['COMPETENCES'].apply(lambda x: ', '.join(sorted(set(x.split(', ')))) if x else '')
df_offres['LANGUES'] = df_offres['LANGUES'].apply(lambda x: ', '.join(sorted(set(x.split(', ')))) if x else '')

df_candidats['COMPETENCES'] = df_candidats['COMPETENCES'].apply(lambda x: ', '.join(sorted(set(x.split(', ')))) if x else '')
df_candidats['LANGUES'] = df_candidats['LANGUES'].apply(lambda x: ', '.join(sorted(set(x.split(', ')))) if x else '')


# Remplacer les valeurs manquantes
df_offres.fillna({'COMPETENCES': '', 'LANGUES': '', 'FORMATION': '', 'EXPERIENCE_DUR': 0}, inplace=True)
df_candidats.fillna({'COMPETENCES': '', 'LANGUES': '', 'FORMATION': '', 'NBR_YEARS_EXP': 0}, inplace=True)

# Générer des embeddings pour les offres
df_offres['description'] = df_offres['COMPETENCES'] + ", " + df_offres['LANGUES'] + ", " + df_offres['FORMATION'] + ", " + df_offres['EXPERIENCE_DUR'].astype(str)
embeddings_offres = model.encode(df_offres['description'].tolist(), show_progress_bar=True)

# Assurez-vous que les embeddings sont bien sous forme de liste de tableaux 1D
df_offres['embedding'] = [embedding.tolist() for embedding in embeddings_offres]

#df_offres['embedding'] = model.encode(df_offres['description'].tolist(), show_progress_bar=True)

# Générer des embeddings pour les candidats
df_candidats['description'] = df_candidats['COMPETENCES'] + ", " + df_candidats['LANGUES'] + ", " + df_candidats['FORMATION'] + ", " + df_candidats['NBR_YEARS_EXP'].astype(str)
embeddings_candidats = model.encode(df_candidats['description'].tolist(), show_progress_bar=True)

# Assurez-vous que les embeddings sont bien sous forme de liste de tableaux 1D
df_candidats['embedding'] = [embedding.tolist() for embedding in embeddings_candidats]
# Vérifier le résultat
print(df_offres.head())
print(df_candidats.head())

#df_candidats['embedding'] = model.encode(df_candidats['description'].tolist(), show_progress_bar=True)
# Étape 3 : Charger les embeddings dans Pinecone
from pinecone import Pinecone, ServerlessSpec, PineconeApiException
import pinecone
# Créez une instance de Pinecone avec votre clé API
api_key = "pcsk_Bek39_GoSxAyBEKDYpgNTADG9gjATrshAMneRiTtY9cEET1LvmsH4mCqyYoYxazS1cPp2"

pc = pinecone.Pinecone(api_key=api_key)
# Vérifiez si l'index existe déjà
if 'jobcandidates' not in pc.list_indexes().names():
    try:
        # Créez l'index si nécessaire
        pc.create_index(
            name='jobcandidates',
            dimension=384,  # Adaptez la dimension selon le modèle utilisé
            metric='cosine',  # Vous pouvez choisir la métrique appropriée
            spec=ServerlessSpec(
                cloud='aws',  # Spécifiez le fournisseur de cloud
                region='us-east-1'  # Essayez une autre région AWS
            )
        )
        print("Index 'job_candidates' créé avec succès.")
    except PineconeApiException as e:
        print(f"Erreur lors de la création de l'index : {e}")
else:
    print("L'index 'job_candidates' existe déjà.")


# Accédez à l'index
index = pc.Index("jobcandidates")


def batch_vectors(vectors, batch_size):
    """
    Divise une liste de vecteurs en lots plus petits.
    """
    for i in range(0, len(vectors), batch_size):
        yield vectors[i:i + batch_size]

# Taille maximale des lots (ajustez si nécessaire)
batch_size = 100  # Taille de lot initiale, adaptée à vos besoins et à vos tests.

# --- Insérer les offres ---
offre_vectors = [(str(row.OFFRE_ID), row.embedding) for _, row in df_offres.iterrows()]

# Vérifiez la dimension des vecteurs
for vector_id, vector_values in offre_vectors:
    if len(vector_values) != 384:
        print(f"Erreur : le vecteur avec l'ID {vector_id} a une dimension incorrecte ({len(vector_values)})")
        break

# Insérer les vecteurs en lots
for batch in batch_vectors(offre_vectors, batch_size):
    try:
        index.upsert(vectors=batch)
    except pinecone.PineconeApiException as e:
        print(f"Erreur lors de l'insertion d'un lot d'offres : {e}")

# --- Insérer les candidats ---
candidat_vectors = [(str(row.CANDIDAT_ID), row.embedding) for _, row in df_candidats.iterrows()]

# Vérifiez la dimension des vecteurs
for vector_id, vector_values in candidat_vectors:
    if len(vector_values) != 384:
        print(f"Erreur : le vecteur avec l'ID {vector_id} a une dimension incorrecte ({len(vector_values)})")
        break

# Insérer les vecteurs en lots
for batch in batch_vectors(candidat_vectors, batch_size):
    try:
        index.upsert(vectors=batch)
    except pinecone.PineconeApiException as e:
        print(f"Erreur lors de l'insertion d'un lot de candidats : {e}")

print("Tous les embeddings ont été insérés dans Pinecone.")
