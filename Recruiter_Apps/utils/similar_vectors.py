import pinecone
def search_similar_vectors_candidat(query_embedding, top_k=5):
    api_key_pin = "pcsk_vUaKS_3PK35kGth5rcmSKZkihFFuaS7B44xzMycHCnot1s9Czf1WE8iXSPZg4nDph81Ak"
    pc = pinecone.Pinecone(api_key=api_key_pin)
    # Connexion à l'index Pinecone
    index_name = 'candidates'  # Le nom de votre index Pinecone
    index_candidats = pc.Index(index_name)
    print(f"Query embedding: {query_embedding}")
    result = index_candidats.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    print(f"Result: {result}")

    # Vérification de la présence de la clé 'matches'
    if 'matches' in result:
        similar_vectors = []
        for match in result['matches']:
            similar_vectors.append({
                'id': match['id'],  # Extraire l'ID
                'score': match['score']  # Extraire le score
            })
        return similar_vectors
    else:
        print("Aucun résultat trouvé.")
        return []

def search_similar_vectors_job(query_embedding, top_k=5):
    api_key_pin = "pcsk_vUaKS_3PK35kGth5rcmSKZkihFFuaS7B44xzMycHCnot1s9Czf1WE8iXSPZg4nDph81Ak"
    pc = pinecone.Pinecone(api_key=api_key_pin)
    # Connexion à l'index Pinecone
    index_name = 'job'  # Le nom de votre index Pinecone
    index_job= pc.Index(index_name)
    print(f"Query embedding: {query_embedding}")
    result = index_job.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    print(f"Result: {result}")

    # Vérification de la présence de la clé 'matches'
    if 'matches' in result:
        similar_vectors = []
        for match in result['matches']:
            similar_vectors.append({
                'id': match['id'],  # Extraire l'ID
                'score': match['score']  # Extraire le score
            })
        return similar_vectors
    else:
        print("Aucun résultat trouvé.")
        return []