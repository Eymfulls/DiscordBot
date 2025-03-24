###########################################################################
# Habilitations : prend en compte (ou non) la demande
###########################################################################

import constantes as c
import champions as ch
from toolbox import contenuOrdre, identiques
import json

# Renvoie trois niveaux d'habilitation :
    # admin si l'utilisateur peut tout faire
    # gymle si l'utilisateur a les autorisations liées à la Ligue Pokémon Reborn FR
    # user si l'utilisateur est en public
    # limit si l'utilisateur est en MP ou en public

def hab(auteur, serveur):
    # Les superusers le sont partout
    if auteur in c.superutilisateurs:
        admin = True
        gymle = True if auteur in ch.getChampions(False) else False
        user = True
        limit = True
        return admin, gymle, user, limit
    admin = False
    
    # Si on est en MP, les infos sont toujours accessibles
    limit = True if not serveur else False

    # Les utilisateurs sous silence n'ont accès qu'aux MP
    with open("muted.json", "r", encoding="utf-8") as muted:
        data = json.load(muted)
        mutedList = []
        for utilisateurs in data:
            mutedList.append(utilisateurs["dtag"])
    if auteur in mutedList:
        admin = False
        gymle = False
        user = False
        return admin, gymle, user, limit
    
    # Si on n'est ni admin ni sous silence, on vérifie que le serveur est autorisé
    if limit or (serveur in c.serveursAutorises):
        user = True
    else:
        user = False

    # Les champions ne le sont que dans les salles autorisées
    gymle = False
    if user:
        if auteur in ch.getChampions(False):
            gymle = True
    
    return admin, gymle, user, limit

def mute(ordre):
    ordre1, elements = contenuOrdre(ordre)  # On casse l'ordre initial pour traiter les fragments
    if not ordre1:
        return False
    if len(elements) != 1:
        return False
    personne = int(elements[0][2:-1])

    if personne == 141195266555379712:
        return "On touche pas à Vinc sale bâtard"
    
    with open("muted.json", "r+", encoding="utf-8") as muted:
        data = json.load(muted)
        if identiques(ordre1, c.O_MUTE_AJOUT):
            
            for utilisateur in data:
                if utilisateur["id"] == personne:
                    return f"{personne} est déjà muted."
            new_mute = {
                "id": personne
            }
            data.append(new_mute)
            muted.seek(0)
            json.dump(data, muted, indent=4, ensure_ascii=False)
            muted.truncate()
            return f"{personne} est maintenant muted."
        
        if identiques(ordre1, c.O_MUTE_RETRAIT):
            for utilisateur in data:
                if utilisateur["id"] == personne:
                    data = [item for item in data if item["id"] != personne]
                    muted.seek(0)
                    json.dump(data, muted, indent=4, ensure_ascii=False)
                    muted.truncate()
                    return f"{personne} n'est plus muted."
            return f"{personne} n'était pas muted."
        
        return False