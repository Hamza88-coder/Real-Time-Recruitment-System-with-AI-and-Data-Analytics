import pandas as pd
import random

# Dictionnaire des entreprises marocaines par secteur
companies_by_sector = {
    'Energy': ['Nareva Holding', 'OCP Group', 'LafargeHolcim Maroc', 'Managem'],
    'Consumer Goods': ['Cosumar', 'Sidi Ali', 'Danone Maroc', 'Unilever Maroc'],
    'Healthcare Services': ['Clinique Internationale de Marrakech', 'Clinique Al Azhar', 'Réseau de santé Al Amal'],
    'Insurance': ['Attijariwafa Assurance', 'RMA Watanya', 'Saham Assurance'],
    'Lab Equipment': ['Biopharma', 'Medtech Maroc', 'Pharmatex'],
    'Financial Services': ['Bank of Africa', 'Attijariwafa Bank', 'BMCE Bank of Africa', 'CIH Bank'],
    'Healthcare Technology': ['Medisys', 'HemoTech', 'InnovHealth'],
    'Industrial': ['LafargeHolcim Maroc', 'Maroc Chimie', 'Managem'],
    'Logistics': ['CTM', 'Groupe BDP International', 'Transports Océan'],
    'Retail': ['Marjane Holding', 'Carrefour Maroc', 'Aswat Assalam'],
    'Healthcare': ['Clinique International de Marrakech', 'Polyclinique de la Santé', 'Réseau de santé Akdital'],
    'Financial Technology': ['PayLogic', 'S2M', 'Flouci'],
    'Energy/Infrastructure': ['ACWA Power', 'OCP Group', 'Nareva Holding'],
    'Real Estate': ['Addoha Group', 'Immobilier Al Omrane', 'Sogecom'],
    'Technology and Entertainment': ['Inwi', 'Orange Maroc', 'Maroc Telecom'],
    'Food & Beverage': ['Les Eaux Minérales d\'Oulmes', 'Coca-Cola Maroc', 'Domaine des Ouled Thaleb'],
    'Automotive': ['Renault Maroc', 'Peugeot Maroc', 'Stellantis'],
    'Engineering': ['Alstom Maroc', 'Société Générale des Travaux du Maroc'],
    'Consumer Goods/Homecare': ['Henkel Maroc', 'Procter & Gamble Maroc'],
    'Diversified': ['SNI', 'OCP Group'],
    'Beverage': ['Coca-Cola Maroc', 'Amazigh Beverages'],
    'Aerospace and Defense': ['AeroPro', 'Royal Air Maroc'],
    'Telecommunications': ['Maroc Telecom', 'Inwi', 'Orange Maroc'],
    'Medical Devices': ['Medtech', 'Biopharma', 'Système Médical et Informatique'],
    'Utilities': ['ONEE', 'LafargeHolcim Maroc'],
    'Food and Beverage/Confectionery': ['Coca-Cola Maroc', 'Saidal', 'Danone Maroc']
}

# Charger le fichier Excel
data = pd.read_excel('fichier_reduit_avec_secteur.xlsx')

# Fonction pour mettre à jour la colonne 'Company' en fonction du secteur et du pays
def update_company(row):
    country = row['Country']
    secteur = row['Secteur']  # Récupérer le secteur
    if country == 'Morocco' and secteur in companies_by_sector:
        # Sélectionner une entreprise au hasard dans le secteur correspondant
        company = random.choice(companies_by_sector[secteur])
        row['Company'] = company  # Mettre à jour la colonne 'Company'
    return row

# Appliquer la fonction à chaque ligne du dataframe
data = data.apply(update_company, axis=1)

# Sauvegarder le fichier modifié dans un nouveau fichier Excel
data.to_excel('fichier_reduit_avec_entreprises_mises_a_jour.xlsx', index=False)

print("Les entreprises ont été mises à jour dans le fichier 'fichier_reduit_avec_entreprises_mises_a_jour.xlsx'.")
