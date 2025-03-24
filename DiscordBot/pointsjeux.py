from cmath import inf
from toolbox import contenuOrdre, identiques
from datetime import datetime
import json
import constantes as c
import divers as di

def jeuxapoints(ordre, missingId):
    ordre1, elements = contenuOrdre(ordre)  # On casse l'ordre initial pour traiter les fragments
    if not ordre1:
        return False, missingId
    personne = elements[0] if len(elements) > 0 else ""
    if len(personne)>1:
        id = int(personne[2:-1]) if personne[2:-1].isdigit() else 0
    points = elements[1] if len(elements) > 1 else ""
    jeu = elements[2] if len(elements) > 2 else ""
    aujourdhui = datetime.today().strftime('%Y-%m-%d')
    new_score = {
        "jeu": jeu,
        "points": points,
        "date": aujourdhui
    }
    with open("pointsjeux.json", "r+", encoding="utf-8") as leaderboard:
        data = json.load(leaderboard)

        if identiques(ordre1, c.O_POINTS_AJOUT) and len(elements) > 1:
            trouve = False
            for utilisateur in data:
                if utilisateur["id"] == id:
                    utilisateur["points"].append(new_score)
                    trouve = True
                    break
            if not trouve:
                new_joueur = {
                    "id": id,
                    "dtag": personne,
                    "points": [new_score]
                    }
                data.append(new_joueur)
            leaderboard.seek(0)
            json.dump(data, leaderboard, indent=4, ensure_ascii=False)
            leaderboard.truncate()
            if not trouve:
                missingId = di.getMissingDtag()
            return f"{personne} remporte {points} points ({jeu}).", missingId
        
        if identiques(ordre1, c.O_POINTS_RECTIF) and len(elements) > 0:
            for utilisateur in data:
                if utilisateur["id"] == personne and len(utilisateur["points"])>0:
                    if utilisateur["points"][-1]["date"] == aujourdhui:
                        saveslot = utilisateur["points"][-1]
                        utilisateur["points"].pop()
                        leaderboard.seek(0)
                        json.dump(data, leaderboard, indent=4, ensure_ascii=False)
                        leaderboard.truncate()
                        return f"Les derniers points de {personne} ont été annulés : {saveslot['points']} points ({saveslot['jeu']})", missingId
                    else:
                        return f"Impossible d'annuler le dernier résultat de {personne} car le jeu ne date pas d'aujourd'hui.", missingId
            return f"{personne} n'a aucun résultat à rectifier (peut-être une faute de frappe dans son tag ?)", missingId

        if identiques(ordre1, c.O_POINTS_SCORE) and len(elements) > 0:
            for utilisateur in data:
                if utilisateur["id"] == id:
                    score = 0
                    if len(utilisateur["points"]) > 0:
                        for point in utilisateur["points"]:
                            score += int(point["points"])
                    return f"{personne} a actuellement {score} points.", missingId
            return f"{personne} n'a jamais participé à un jeu (peut-être une faute de frappe dans son tag ?)", missingId

        if identiques(ordre1, c.O_POINTS_CLASSEMENT) and len(elements) > 0:
            if not elements[0].isdigit():
                return f"Merci de renseigner le nombre maximum de résultats.", missingId
            else:
                maxretours = int(elements[0])
            tableau = []
            for utilisateur in data:
                if len(utilisateur["points"]) > 0:
                    score = 0
                    for point in utilisateur["points"]:
                        score += int(point["points"])
                    participant = {utilisateur["dtag"]: score}
                    tableau.append(participant)
            tableau = sorted(tableau, key=lambda x: list(x.values())[0], reverse=True)
            if len(tableau) > maxretours:
                seuil = list(tableau[maxretours - 1].values())[0]
                tableau = [p for p in tableau if list(p.values())[0] >= seuil]
            
            retour = ""
            compteur = 0
            compteursav = 0
            scorep = float(inf)
            for element in tableau:
                for cle, valeur in element.items():
                    if valeur < scorep:
                        compteur += 1
                        compteursav = compteur
                        scorep = valeur
                    else:
                        compteur += 1
                    retour += f"{compteursav} : {cle} avec {valeur} points.\n"
            return retour, missingId
        
    return False, missingId