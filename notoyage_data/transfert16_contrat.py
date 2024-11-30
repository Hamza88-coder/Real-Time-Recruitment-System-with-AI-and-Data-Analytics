import pandas as pd
import random

# Charger le fichier Excel
data = pd.read_excel('fichier_reduit_avec_telephone_mise_a_jour.xlsx')


# Fonction pour assigner les valeurs du contrat selon le type de travail
def assign_contrat(row, cdi_ratio=0.4):
    work_type = row['Work Type']

    # Si le type de travail est "Contract", il y a une chance de 40% d'être CDI
    if work_type == 'Contract':
        if random.random() < cdi_ratio:  # 40% chance de CDI
            return 'CDI'
        else:
            return 'CDD'

    # Affecter les autres types directement
    elif work_type == 'Full-Time':
        return 'CDI'
    elif work_type == 'Intern':
        return 'Stage'
    elif work_type == 'Part-Time':
        return 'CDD'
    elif work_type == 'Temporary':
        return 'Intérim'
    else:
        return 'Non défini'  # Si le type de travail n'est pas reconnu


# Appliquer la fonction à chaque ligne du DataFrame pour créer la colonne 'contrat'
data['contrat'] = data.apply(assign_contrat, axis=1)

# Sauvegarder le DataFrame mis à jour dans un nouveau fichier Excel
data.to_excel('fichier_reduit_avec_contrat.xlsx', index=False)

# Afficher un aperçu des 5 premières lignes pour vérifier
print(data.head())
