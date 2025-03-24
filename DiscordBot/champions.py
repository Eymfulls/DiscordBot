import json
import constantes as c
from toolbox import identiques, contenuOrdre

def gestionChampions(ordre, niv_a, niv_c, niv_z):

    ordre1, elements = contenuOrdre(ordre)  # On casse l'ordre initial pour traiter les fragments

    with open("champions.json", "r+", encoding="utf-8") as champ:
        data = json.load(champ)

        if identiques(ordre1, c.O_CHAMPION_AJOUT) and niv_a:
            #Ajout d'un champion, on dépile tous les morceaux
            dtag = elements[0] if elements[0] else False
            id = int(dtag[2:-1]) if dtag else False
            type = elements[1] if elements[1] else False
            terrain = elements[2] if elements[2] else False
            style = elements[3] if elements[3] else False
            titre = elements[4] if elements[4] else ""

            if not (id and type and style and terrain):   # Ces trois champs sont obligatoires
                return "Commande invalide"
            if type not in c.TYPES:                         # Le type doit être connu
                return f"Le type {type} n'existe pas."

            # On vérifie que le champion, son type ou son terrain ne soient pas déjà présents dans le json des champions
            for element in data["data"]:
                if element["id"] == id:
                    return f"{element['dtag']} est déjà un champion."
                if element["type"] == type:
                    return f"Le type {type} est déjà assigné à un champion."
                if element["terrain"] == terrain:
                    return f"Le terrain {terrain} est déjà assigné à un champion."
            
            # Si on est là, c'est qu'on est prêt à ajouter le champion!
            nouveauChamp = {
                "id": id,
                "dtag": dtag,
                "type": type,
                "terrain": terrain,
                "style": style,
                "titre": titre
            }
            data["data"].append(nouveauChamp)

            # Mise à jour des données
            champ.seek(0)
            json.dump(data, champ, indent=4, ensure_ascii=False)
            champ.truncate()
            
            return f"{dtag} est notre nouveau champion de type {type}. Son terrain est {terrain}, où il combat en {style}.".strip()
            
        elif identiques(ordre1, c.O_CHAMPION_RETRAIT) and niv_a:
            #retrait d'un champion
            if elements[0]:
                id = elements[0][2:-1]
            else:
                return

            avant = len(data["data"])
            data["data"] = [item for item in data["data"] if not identiques(item["dtag"], dtag)]

            if len(data["data"])<avant:
                # Mise à jour des données uniquement si la taille a changé (champion correctement retiré)
                champ.seek(0)
                json.dump(data, champ, indent=4, ensure_ascii=False)
                champ.truncate()
                return f"{dtag} nous a quittés."

            # Si on arrive là, le champion n'a pas été retiré
            return f"{dtag} n'était pas un champion (peut-être est-il mal orthographié ?)"
        
        elif identiques(ordre1, c.O_CHAMPION_RECHERCHE) and (niv_c or niv_z):
            #Informations sur l'un des badges
            recherche = elements[0] if elements[0] else ""
            correspondance = False
            for element in data["data"]:
                if recherche[2:-1].isdigit() and int(recherche[2:-1]) == element["id"]:
                    if element["id"] in (792098954342957096, 1198625640610529290):
                        retour = f"Championne trouvée\n"
                    else:
                        retour = f"Champion trouvé\n"
                    correspondance = True
                elif identiques(element["dtag"], recherche):      # Recherche possible par TAG de champion
                    if element["id"] in (792098954342957096, 1198625640610529290):
                        retour = f"Championne {recherche} trouvée\n"
                    else:
                        retour = f"Champion {recherche} trouvé\n"
                    correspondance = True
                elif identiques(element["type"], recherche):      # Recherche possible par type du badge
                    retour = f"Type {recherche} trouvé\n"
                    correspondance = True
                elif identiques(element["terrain"], recherche):   # Recherche possible par terrain
                    retour = f"Terrain {recherche} trouvé\n"
                    correspondance = True
                if correspondance:                              # On est au bon endroit !
                    titre = element["titre"]
                    type = element["type"]
                    dtag = element["dtag"]
                    style = element["style"]
                    terrain = element["terrain"]
                    if element["id"] in (792098954342957096, 1198625640610529290):
                        retour += f"{titre} {dtag} est la championne de type {type}. Elle combat en {style} sur le terrain {terrain}."
                    else:  
                        retour += f"{titre} {dtag} est le champion de type {type}. Il combat en {style} sur le terrain {terrain}."
                    return retour
            
            # Si on est là, on n'a rien trouvé
            return f"Aucune correspondance pour {recherche} (peut-être que l'objet de la recherche est mal orthographié)"

        elif identiques(ordre1, c.O_CHAMPION_TOUS) and (niv_c or niv_z):
            # On récupère tous les champions (True = on veut les détails)
            listeChampions = getChampions(True)
            retour = ""
            for champion in listeChampions:
                retour += champion
                retour += "\n"
            return retour.strip()
    return False

# Ce script récupère tous les champions
# etendu : on veut juste les nom, ou bien une phrase présentant le champion ?
def getChampions(etendu):
    with open("champions.json", "r", encoding="utf-8") as champ:
        data = json.load(champ)
        listeChampions = []
        for champion in data["data"]:   
            dtag = champion["dtag"]
            id = champion["id"]     
            if etendu:
                titre = champion["titre"]
                type = champion["type"]
                style = champion["style"]
                terrain = champion["terrain"]
                if id in (792098954342957096, 1198625640610529290):
                    listeChampions.append(f"{titre} {dtag} est la championne de type {type}. Elle combat en {style} sur le terrain {terrain}.")
                else:  
                    listeChampions.append(f"{titre} {dtag} est le champion de type {type}. Il combat en {style} sur le terrain {terrain}.")
            else:
                listeChampions.append(id)
        
    return listeChampions
