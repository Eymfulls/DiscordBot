from datetime import datetime
import json
import constantes as c
from toolbox import identiques, contenuOrdre

def isMaitre(tag):
    with open("hof.json", "r+", encoding="utf-8") as hof:
        data = json.load(hof)
    for guy in data["data"]:
        if guy["id"] == tag and guy["debutMaitre"] != False and guy["finMaitre"] == False:
                return True
    return False

def gestionMaitres(ordre, guy, niv_a, niv_c):
    isMaitre = isMaitre(guy)
    ordre1, elements = contenuOrdre(ordre)  # On casse l'ordre initial pour traiter les fragments
    aujourdhui = datetime.today().strftime('%Y-%m-%d')

    with open("hof.json", "r+", encoding="utf-8") as hof:
        data = json.load(hof)

        if identiques(ordre1, c.O_HOF_VICTOIRE) and isMaitre:
            #Ajout d'un champion, on dépile tous les morceaux
            dtag = elements[0] if elements[0] else False
            id = int(dtag[2:-1]) if dtag else False

            if not id:   # Ces trois champs sont obligatoires
                return "Commande invalide"

            # On vérifie que le champion, son type ou son terrain ne soient pas déjà présents dans le json des champions
            for element in data["data"]:
                if element["id"] == id:
                    element["debutMaitre"] = aujourdhui
                    element["nbMatchsChallenger"] += 1
                    for maitre in data["data"]:
                        if maitre["id"] == guy:
                            maitre["finMaitre"] = aujourdhui
                            maitre["nbMatchsMaitre"] += 1
                            hof.seek(0)
                            json.dump(data, hof, indent=4, ensure_ascii=False)
                            hof.truncate()

                            return f"Gloire à {dtag}, notre nouveau Maître de la Ligue Reborn FR !"
            
            return f"{dtag} n'est pas reconnu comme ayant 18 badges."

        if identiques(ordre1, c.O_HOF_DEFAITE) and isMaitre:
            #Ajout d'un champion, on dépile tous les morceaux
            dtag = elements[0] if elements[0] else False
            id = int(dtag[2:-1]) if dtag else False

            if not id:   # Ces trois champs sont obligatoires
                return "Commande invalide"

            # On vérifie que le champion, son type ou son terrain ne soient pas déjà présents dans le json des champions
            for element in data["data"]:
                if element["id"] == id:
                    element["nbMatchsChallenger"] += 1
                    for maitre in data["data"]:
                        if maitre["id"] == guy:
                            maitre["nbMatchsMaitre"] += 1
                            hof.seek(0)
                            json.dump(data, hof, indent=4, ensure_ascii=False)
                            hof.truncate()

                            return f"{dtag} n'a pas réussi à passer Maître. Bonne chance pour ta prochaine tentative !"
            
            return f"{dtag} n'est pas reconnu comme ayant 18 badges."            

    return False