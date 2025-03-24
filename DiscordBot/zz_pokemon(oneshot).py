import requests
from bs4 import BeautifulSoup
import json

# URL de la page à scraper
url = "https://bulbapedia.bulbagarden.net/wiki/List_of_French_Pok%C3%A9mon_names"

# Effectuer une requête GET pour récupérer la page
response = requests.get(url)
if response.status_code == 200:
    # Parser le contenu HTML
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Trouver tous les nœuds <tr> avec style="background:#FFF"
    tr_nodes = soup.find_all("tr", style="background:#FFF")
    
    # Créer une liste pour stocker les données
    data = []
    
    for tr in tr_nodes:
    # Trouver tous les <td> de ce <tr>
        td_nodes = tr.find_all("td")
        
        # Vérifier qu'il y a bien 4 <td>
        if len(td_nodes) == 4:
            # <td> du numéro avec style spécifique
            td_number = td_nodes[0]
            number = td_number.get_text(strip=True).replace("#", "")
            
            # <td> du nom anglais
            td_english = td_nodes[2]
            en_name = None
            a_tag_en = td_english.find("a")
            if a_tag_en:
                en_name = a_tag_en.get_text(strip=True)
            
            # <td> du nom français
            td_french = td_nodes[3]
            fr_name = None
            a_tag_fr = td_french.find("a")
            if a_tag_fr:
                fr_name = a_tag_fr.get_text(strip=True)
            
            # Ajouter les données à la liste
            data.append({"dexnum": number, "ennom": en_name, "frnom": fr_name, "forme1": "", "forme2": "", "ligue":True})

        

    
    # Générer un JSON avec les données extraites
    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    with open("zzpokedex.json", "w", encoding="utf-8") as file: # zz de sécurité pour ne pas écraser le Pokédex en cas d'erreur
        file.write(json_data)

# N'a servi qu'une fois à prémâcher le contenu de pokedex.json
# Ne plus relancer