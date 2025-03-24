###########################################################################
# Divers : actions spécifiques non classables
###########################################################################
from datetime import datetime
import json
from toolbox import identiques
import constantes as c

# Le dresseur a gagné, le champion lui remet son badge
def remettreBadge(auteur, ordre):
    badgeRemis = getType(auteur)            # Récupérer le type du badge en fonction du champion
    if not badgeRemis:
        return

    id = int(ordre[2:-1])

    with open("dresseurs.json", "r+", encoding="utf-8") as dresseurs:
        data = json.load(dresseurs)
        for element in data["data"]:
            # Recherche du dresseur
            if element["id"] == id:
                badgeTrouve = False
                aujourdhui = datetime.today().strftime('%Y-%m-%d')
                for badge in element["badges"]:
                    # Recherche du badge, s'il existe, c'est que le challenger a déjà affronté au moins une fois le champion
                    if identiques(badge["type"], badgeRemis):
                        if badge["Victoire"]:
                            return f"{ordre} possède déjà le badge {badgeRemis}"
                        badge["Victoire"] = True
                        badge["nbDefis"] += 1
                        badge["dateVictoire"] = aujourdhui
                        badgeTrouve = True
                if not badgeTrouve: # Le challenger gagne du premier coup
                    newBadge = {
                        "type": badgeRemis,
                        "Victoire": True,
                        "nbDefis": 1,
                        "dateVictoire": aujourdhui
                    }
                    element["badges"].append(newBadge)
                
                # MÀJ du json des challengers
                dresseurs.seek(0)
                json.dump(data, dresseurs, indent=4, ensure_ascii=False)
                dresseurs.truncate()
                return f"Félicitations {ordre}, voici le badge {badgeRemis} !"
   
        # Dresseur non trouvé
        return f"Le dresseur {ordre} n'est pas inscrit au tournoi (peut-être est-il mal orthographié ?)"

# Le dresseur a perdu, on enregistre le résultat
def archiverDefaite(auteur, ordre):
    badgeEnQuestion = getType(auteur)       # Récupérer le type du badge en fonction du champion
    if not badgeEnQuestion:
        return
    id = int(ordre[2:-1])

    with open("dresseurs.json", "r+", encoding="utf-8") as dresseurs:
        data = json.load(dresseurs)
        for element in data["data"]:
            # Rechercher le dresseur
            if element["id"] == id:
                badgeTrouve = False
                for badge in element["badges"]:
                    # Rechercher le badge, s'il existe, c'est que le challenger n'en est pas à sa première défaite
                    if identiques(badge["type"], badgeEnQuestion):
                        if not badge["Victoire"]:
                            badge["nbDefis"] += 1
                            badgeTrouve = True
                        else:
                            return f"{ordre} possède déjà le badge {badgeEnQuestion}"
                if not badgeTrouve: # Première défaite du challenger
                    newBadge = {
                        "type": badgeEnQuestion,
                        "Victoire": False,
                        "nbDefis": 1,
                        "dateVictoire": ""
                    }
                    element["badges"].append(newBadge)
                
                # Mise à jour du json des challengers
                dresseurs.seek(0)
                json.dump(data, dresseurs, indent=4, ensure_ascii=False)
                dresseurs.truncate()
                return f"{ordre} a perdu dans sa tentative pour le badge {badgeEnQuestion}."
   
        # Dresseur non trouvé
        return f"Le dresseur {ordre} n'est pas inscrit au tournoi (peut-être est-il mal orthographié ?)"

# Petite fonction pour récupérer le type du champion postant le résultat
def getType(champion):
    with open("champions.json", "r", encoding="utf-8") as champ:
        data = json.load(champ)
        badge = False
        for element in data["data"]:
            if element["id"] == champion:
                badge = element["type"]
                break
    return badge

# Mode Chut : FLOBOT se tait jusqu'au contre-ordre
def ModeChut(suffixe, modeChut):
    if identiques(suffixe, c.O_CHUT_ACTIV):
        modeChut = True
        retour = "Mode 'Chut' activé. Ce sujet se taira jusqu'au contre-ordre."
    elif identiques(suffixe, c.O_CHUT_DESACT):
        modeChut = False
        retour = "Mode 'Chut' désactivé. Ce sujet reprend ses activités."
    else:
        if modeChut:
            retour = "Mode 'Chut' actuellement actif. La commande '$Chut -' permet à ce sujet de reprendre son activité."
        else:
            retour = "Mode 'Chut' actuellement inactif. Si vous en voyez le besoin, la commande '$Chut +' ordonnera à ce sujet de se taire."
    return modeChut, retour

def getMissingDtag():
    with open("champions.json", "r", encoding="utf-8") as champ:
        data = json.load(champ)
        idlist = []
        for champion in data["data"]:
            if champion["dtag"][2:-1].isdigit() and champion["id"] == int(champion["dtag"][2:-1]):
                idlist.append(champion["id"])
    with open("pointsjeux.json", "r", encoding="utf-8") as leaderboard:
        data = json.load(leaderboard)
        for joueur in data:
            if joueur["dtag"][2:-1].isdigit() and joueur["id"] == int(joueur["dtag"][2:-1]):
                idlist.append(joueur["id"])
    if len(idlist) == 0:
        return False
    else:
        return idlist

def fixChamp(id, name):
    with open("champions.json", "r+", encoding="utf-8") as champ:
        data = json.load(champ)
        idlist = []
        for champion in data["data"]:
            if champion["id"] == id:
                champion["dtag"] = name
            if champion["dtag"][2:-1].isdigit() and champion["id"] == int(champion["dtag"][2:-1]):
                idlist.append(champion["id"])
        
        champ.seek(0)
        json.dump(data, champ, indent=4, ensure_ascii=False)
        champ.truncate()

    with open("pointsjeux.json", "r+", encoding="utf-8") as leaderboard:
        data = json.load(leaderboard)
        idlist = []
        for joueur in data:
            if joueur["id"] == id:
                joueur["dtag"] = name
            if joueur["dtag"][2:-1].isdigit() and joueur["id"] == int(joueur["dtag"][2:-1]):
                idlist.append(joueur["id"])
        
        leaderboard.seek(0)
        json.dump(data, leaderboard, indent=4, ensure_ascii=False)
        leaderboard.truncate()  

    if len(idlist) == 0:
        return False
    else:
        return idlist