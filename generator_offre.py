import re

def generer_offre_emploi(api_key, prompt, resume_data):
    try:
        from groq import Groq  # Import du client Groq

        groq_client = Groq(api_key=api_key)

        # Messages pour le modèle
        messages = [
            {
                "role": "system",
                "content": "Tu es un assistant chargé de générer des offres d'emploi basées sur un modèle structuré."
            },
            {
                "role": "user",
                "content": f"""Voici les informations de base d'un candidat :
                {resume_data}
                Génère une offre d'emploi sous un format texte suivant ce modèle :
                Titre du poste : Stagiaire Data Engineer (PFE)
                Société : DataTech Solutions
                Compétences requises : Python, SQL, Apache Airflow, Talend, MongoDB, Cassandra, AWS, Google Cloud
                Lieu : Lyon, France
                Type d'offre : stage
                Type de contrat : Stage PFE
                Durée : 6 mois
                Email : contact@datatechsolutions.fr
                Téléphone : +33 1 23 45 67 89
                Type : Hybride
                Langues requises : Anglais, Français
                Salaire : 1 200 EUR par mois
                Date de début : 15 janvier 2025
                Secteur d'activité : Technologie de l'information
                Expérience demandée : None
                Formation requise : Étudiant en informatique ou domaine connexe
                Avantages : Assurance santé, Opportunités de formation continue
                Site web : www.datatechsolutions.fr
                """
            }
        ]

        # Appel au modèle
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.0,
            max_tokens=1500
        )

        # Extraction du contenu généré
        data = response.choices[0].message.content
        
        # Vérifier si un texte bien formé est retourné
        if data:
            return data.strip()
        else:
            return "Erreur : Aucune donnée générée."

    except Exception as e:
        return f"Erreur lors de l'analyse : {str(e)}"

# Exemple d'utilisation
api_key = "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"
resume_data = "Candidat expert en Python et SQL, avec expérience dans le cloud AWS."
prompt = "Générer une offre d'emploi sous format texte structuré."

offre = generer_offre_emploi(api_key, prompt, resume_data)
print(offre)
