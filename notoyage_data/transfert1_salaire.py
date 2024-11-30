import pandas as pd

# Charger le dataset depuis le fichier Excel
data = pd.read_excel('fichier_reduit.xlsx')

# Fonction pour convertir la valeur maximale de la plage en décimal
def extract_max_salary(salary_range):
    # Diviser les valeurs en deux parties
    _, max_salary = salary_range.split('-')
    # Enlever le symbole $ et le K, puis multiplier par 100 pour obtenir le format décimal
    max_decimal = float(max_salary.replace('$', '').replace('K', '')) * 100
    # Retourner la valeur maximale en format décimal avec deux chiffres après la virgule
    return f"{max_decimal:,.2f}"

# Appliquer la conversion pour extraire la valeur maximale et créer la colonne 'salaire'
data['salaire'] = data['Salary Range'].apply(extract_max_salary)

# Sauvegarder le résultat dans un nouveau fichier Excel
data.to_excel('salaries_max_convertis.xlsx', index=False)

print("La conversion est terminée et les données sont sauvegardées dans 'salaries_max_convertis.xlsx'.")
