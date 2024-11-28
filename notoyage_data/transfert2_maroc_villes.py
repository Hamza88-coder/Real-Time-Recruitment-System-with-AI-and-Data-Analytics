import pandas as pd
import random

# Charger le dataset depuis le fichier Excel
data = pd.read_excel('salaries_max_convertis.xlsx')

# Liste des villes marocaines
moroccan_cities = [
    'Casablanca', 'Rabat', 'Salé', 'Agadir', 'Tanger', 'Fès',
    'Marrakech', 'Meknès', 'Oujda', 'Kenitra', 'Tétouan', 'Safi',
    'Mohammedia', 'El Jadida', 'Khouribga', 'Beni Mellal',
    'Nador', 'Khemisset', 'Settat', 'Larache', 'Guelmim',
    'Taza', 'Tan-Tan', 'Errachidia', 'Azrou', 'Ouarzazate',
    'Laâyoune', 'Al Hoceima', 'Ifrane', 'Asilah'
]

# Sélectionner aléatoirement 700 indices de lignes dans le dataset
indices_to_change = random.sample(range(len(data)), 700)

# Modifier les lignes sélectionnées avec le pays 'Morocco' et des villes marocaines aléatoires
for idx in indices_to_change:
    data.at[idx, 'Country'] = 'Morocco'
    data.at[idx, 'location'] = random.choice(moroccan_cities)

# Sauvegarder le dataset modifié dans un nouveau fichier Excel
data.to_excel('fichier_reduit_avec_maroc.xlsx', index=False)

print("Modification terminée et les données sont sauvegardées dans 'fichier_reduit_avec_maroc.xlsx'.")
