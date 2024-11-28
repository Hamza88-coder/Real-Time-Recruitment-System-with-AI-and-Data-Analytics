import pandas as pd

# Charger le fichier Excel
data = pd.read_excel('fichier_reduit_avec_URL.xlsx')

# Dictionnaire des entreprises et de leurs URLs
company_urls = {
    "Nareva Holding": "http://www.nareva.ma",
    "Unilever Maroc": "https://www.unilever.com",
    "Clinique Internationale de Marrakech": "http://www.cim.ma",
    "Attijariwafa Assurance": "https://www.attijariwafassurance.ma",
    "Pharmatex": "https://www.pharmatex.ma",
    "BMCE Bank of Africa": "https://www.bmcebank.ma",
    "HemoTech": "http://www.hemotech.com",
    "Maroc Chimie": "http://www.marocchimie.ma",
    "Groupe BDP International": "http://www.bdp-group.com",
    "Marjane Holding": "https://www.marjane.ma",
    "PayLogic": "https://www.paylogic.com",
    "Immobilier Al Omrane": "http://www.alomrane.ma",
    "Managem": "https://www.managemgroup.com",
    "Orange Maroc": "https://www.orange.ma",
    "Coca-Cola Maroc": "https://www.cokecolamiddleeast.com",
    "Renault Maroc": "https://www.renault.ma",
    "Danone Maroc": "https://www.danone.com",
    "Alstom Maroc": "https://www.alstom.com",
    "Procter & Gamble Maroc": "https://www.pg.com",
    "OCP Group": "https://www.ocpgroup.ma",
    "Saham Assurance": "https://www.sahamassurance.ma",
    "CIH Bank": "https://www.cihbank.ma",
    "KLA": "https://www.kla.com",
    "LafargeHolcim Maroc": "https://www.lafarge.ma",
    "Leidos Holdings": "https://www.leidos.com",
    "State Bank of India (SBI)": "https://www.sbi.co.in",
    "SpartanNash": "https://www.spartannash.com",
    "Bank of Africa": "https://www.bkam.ma",
    "Rockwell Automation": "https://www.rockwellautomation.com",
    "Aswat Assalam": "https://www.aswatassalam.com",
    "Ramsay Health Care": "https://www.ramsayhealth.com",
    "Polyclinique de la Santé": "http://www.polyclinique-sante.ma",
    "Domaine des Ouled Thaleb": "https://www.ouledthaleb.ma"
}

# Fonction pour mettre à jour la colonne 'URL' en fonction de 'Company'
def update_url(row):
    company_name = row['Company']
    # Si l'entreprise existe dans le dictionnaire, on met à jour l'URL, sinon on garde l'ancienne valeur
    return company_urls.get(company_name, row['URL'])  # Renvoyer l'ancienne URL si l'entreprise n'est pas trouvée

# Appliquer la fonction à la colonne 'Company' pour mettre à jour la colonne 'URL'
data['URL'] = data.apply(update_url, axis=1)

# Sauvegarder le fichier modifié dans un nouveau fichier Excel
data.to_excel('fichier_reduit_avec_URL_mis_a_jour.xlsx', index=False)

print("La colonne URL a été mise à jour et sauvegardée dans le fichier 'fichier_reduit_avec_URL_mis_a_jour.xlsx'.")
