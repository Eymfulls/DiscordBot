import requests
from bs4 import BeautifulSoup
import json

# URL de la page à scraper
urlmoves = "https://bulbapedia.bulbagarden.net/wiki/List_of_moves_in_other_languages"
urltalents = "https://bulbapedia.bulbagarden.net/wiki/List_of_Abilities_in_other_languages"
url = urltalents

# Effectuer une requête GET pour récupérer la page
response = requests.get(url)
if response.status_code == 200:
    # Parser le contenu HTML
    soup = BeautifulSoup(response.text, "html.parser")
    
    tableau = soup.find("table", {"class": ["roundy", "sortable", "jquery-tablesorter"]}).find("tbody")

    moves_list = []

    # Parcourir les lignes du tableau
    for ligne in tableau.find_all("tr")[1:]:  # [1:] pour sauter l'en-tête
        colonnes = ligne.find_all("td")

        if len(colonnes) >= 5:
            if not colonnes[0].text.strip().isdigit():
                continue
            move_id = int(colonnes[0].text.strip())  # ID en entier
            move_name = colonnes[1].text.strip()  # Nom anglais
            move_fr = colonnes[4].text.split("*")[0].strip()  # Nom français sans ancienne traduction

            moves_list.append({"id": move_id, "en": move_name, "fr": move_fr})

    # Sauvegarde en JSON
    with open("talentdex.json", "w", encoding="utf-8") as f:
        json.dump(moves_list, f, ensure_ascii=False, indent=4)

    print("Fichier movedex.json généré avec succès ! ✅")