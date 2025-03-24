import json
import constantes as c
from toolbox import identiques, contenuOrdre

def gestionDresseurs(ordre, auteur, auteurlettres):

    ordre1, elements = contenuOrdre(ordre)  # On casse l'ordre initial pour traiter les fragments
    if len(elements) == 0:
        elements = False

    with open("dresseurs.json", "r+", encoding="utf-8") as dresseurs:
        data = json.load(dresseurs)

        if identiques(ordre1, c.O_DRESSEUR_INSCRIP):
            #Inscription du dresseur
            for dresseur in data["data"]:       # On cherche s'il n'existe pas déjà
                if auteur == dresseur["id"]:
                    return f"{auteur} est déjà inscrit au tournoi."
            
            # Dresseur non trouvé, on l'inscrit
            nouveauDresseur = {
                "id": auteur,
                "dtag": auteurlettres,
                "pokemon": [],
                "badges": []
            }
            data["data"].append(nouveauDresseur)

            # Mise à jour du JSON des dresseurs
            dresseurs.seek(0)
            json.dump(data, dresseurs, indent=4, ensure_ascii=False)
            dresseurs.truncate()
            return f"{auteurlettres} a correctement rejoint la Ligue Pokémon Reborn FR."
            
        elif identiques(ordre1, c.O_DRESSEUR_MOI):
            #Informations sur le dresseur
            retour = ""
            for dresseur in data["data"]:
                if dresseur["id"] == auteur:    # Dresseur trouvé
                    pokemonList = ""
                    nbPoke = 0
                    for poke in dresseur["pokemon"]:        # Génération de la liste des dresseurs
                        pokemonList += poke
                        pokemonList += ", "
                        nbPoke += 1
                    pokemonList = pokemonList[:-2] if len(pokemonList) > 2 else "à définir"
                    combats = 0
                    badgesList = ""
                    badgesNumber = 0
                    for badge in dresseur["badges"]:        # Récupération des badges et nombre de combats réalisés
                        if badge["Victoire"] == True:
                            badgesList += badge["type"]
                            badgesList += ", "
                            if badge["nbDefis"] > 0:
                                badgesNumber += 1
                        combats += badge["nbDefis"]
                    badgesList = badgesList[:-2] if len(badgesList) > 2 else "aucun"

                    # Cas de la demande "technique", on veut juste la liste actuel et le statut "modifications autorisées"
                    if elements and identiques(elements[0], "tech"):
                        if combats > 0:
                            return 400
                        else:
                            return pokemonList

                    # Création du retour littéral
                    retour = f"{auteurlettres} combat avec les {nbPoke} Pokémon suivants : {pokemonList}\n"
                    retour += f"{auteurlettres} a remporté les badges suivants : {badgesList}\n"
                    winrate = int(100 * float(badgesNumber) / float(combats)) if combats>0 else 0
                    retour += f"{auteurlettres} a remporté {badgesNumber} combat(s) en combattant {combats} fois, pour un taux de victoire de {winrate} %."
                    return retour

            # On n'a pas trouvé le dresseur en question        
            if elements and elements[0] == "tech":
                return 0
            else:
                return f"{auteurlettres} ne participe pas au tournoi."
        
        elif (identiques(ordre1, c.O_DRESSEUR_LUI) or identiques(ordre1, c.O_DRESSEUR_ELLE)) and elements:
            #Moi mais en donnant un ID
            id = elements[0]
            resultat = gestionDresseurs("MOI", int(id[2:-1]), id)
            return resultat

        elif identiques(ordre1, c.O_DRESSEUR_AJOUT) and elements:
            # Ajout d'un ou plusieurs Pokémon dans la liste du dresseur
            if len(elements) == 0:
                return "Merci de préciser les Pokémon à inscrire."
            infosParticipant = gestionDresseurs(f"{c.O_DRESSEUR_MOI}, tech", auteur, auteurlettres)    # On récupère la liste des Pokémon ou le statut d'erreur   
            if infosParticipant == 0:
                return f"{auteurlettres} ne participe pas au tournoi."     
            elif infosParticipant == 400:
                return f"{auteurlettres} a déjà participé à un combat et ne peut plus modifier ses Pokémon."

            # Liste initiale : les Pokémon déjà présents OU une liste vide
            pokemonList = [e.strip() for e in infosParticipant.split(",")]
            if pokemonList[0] == "à définir":
                pokemonList = []
            
            # On récupère le Pokédex pour savoir ce qu'on peut utiliser
            with open("pokedex.json", "r", encoding="utf-8") as pokedexfile:
                pokedex = json.load(pokedexfile)

            # Initialisation des cinq cas possibles : ajout réussi, Pokémon déjà présent, Pokémon illégal, Pokémon inconnu, Forme à préciser
            okajout = ""
            dejala = ""
            illegal = ""
            inconnu = ""
            precision = ""

            for pokemon in elements:        # On parcourt la liste donnée par l'utilisateur
                trouve = False
                pokid = pokemon.split()[0]  # S'il y a une espace, c'est qu'une forme est précisée derrière
                if len(pokemon.split()) > 1:
                    pokforme = pokemon.split(maxsplit=1)[1]
                else:
                    pokforme = False

                if pokid.isdigit():         # Si l'entrée est numérique, on cherche par ID, il faut rajouter les 0 non significatifs
                    pokid = f"0000{pokid}"[-4:]

                # Ça y est, on peut parcourir le Pokédex pour rechercher notre match
                for entry in pokedex:
                    if identiques(pokid, entry['dexnum']) or identiques(pokid, entry['ennom']) or identiques(pokid, entry['frnom']):
                        # Match possible par numéro, nom français ou nom anglais
                        trouve = True
                        aAjouter = entry['frnom']         # On prendra le nom français pour la suite

                        # On récupère les formes si elles existent
                        formeMat = False
                        attendu = False
                        if entry['forme1'] != "":
                            f1 = entry['forme1']
                            f2 = entry['forme2']
                            f3 = entry['forme3'] if 'forme3' in entry else ""
                            f4 = entry['forme4'] if 'forme4' in entry else ""
                            attendu = f"('{aAjouter} {f1}' ou '{aAjouter} {f2}'"
                            if f3 != "":
                                attendu += f" ou '{aAjouter} {f3}'"
                            if f4 != "":
                                attendu += f" ou '{aAjouter} {f4}'"
                            attendu += "),"
                        
                            if not pokforme:
                                pass
                            elif identiques(pokforme, f1):
                                aAjouter += f" {f1}"
                                formeMat = True
                            elif identiques(pokforme, f2):
                                aAjouter += f" {f2}"
                                formeMat = True
                            elif identiques(pokforme, f3):
                                aAjouter += f" {f3}"
                                formeMat = True
                            elif identiques(pokforme, f4):
                                aAjouter += f" {f4}"
                                formeMat = True
                            else:
                                aAjouter += f" {pokforme}"
                        
                        if not entry['ligue']:      # Pokémon interdit (probablement légendaire ou UC)
                            illegal += aAjouter
                            illegal += "," 

                        elif aAjouter in pokemonList: # Pokémon déjà inscrit
                            dejala += aAjouter
                            dejala += ","      

                        elif attendu and not formeMat: # Forme absente ou invalide
                            precision += f" {aAjouter} : {attendu}"

                        else:                           # Ajout OK
                            okajout += aAjouter
                            okajout += ","
                        break
                if not trouve:                          # Pokémon non trouvé
                    inconnu += pokemon
                    inconnu += ","
            
            # On vire les virgules de la fin
            okajout = okajout[:-1] if len(okajout)>1 else False
            dejala = dejala[:-1] if len(dejala)>1 else False
            illegal = illegal[:-1] if len(illegal)>1 else False
            inconnu = inconnu[:-1] if len(inconnu)>1 else False
            precision = precision[:-1] if len(precision)>1 else False

            # Boucle pour les ajouts réels (dans la limite des 18 Pokémon), d'abord les Pokémon déjà présents, puis les ajouts
            max = False
            ajoutreels = ""
            initial = len(pokemonList)
            if okajout:
                ajouter = list(set(okajout.split(",")))
                for ajout in ajouter:
                    if len(pokemonList)<18:
                        pokemonList.append(ajout)
                        ajoutreels += ajout
                        ajoutreels += ","
                    else:
                        max = True
                        break
            
            # Si la taille de la liste est supérieure à la taille initiale, on met le JSON à jour
            if len(pokemonList)>initial:
                for dresseur in data["data"]:
                    if dresseur["id"] == auteur:
                        dresseur["pokemon"] = pokemonList
                        dresseurs.seek(0)
                        json.dump(data, dresseurs, indent=4, ensure_ascii=False)
                        dresseurs.truncate()
                        break

            # C'est fini, on donne le retour complet de ce qui a été traité (ou non)
            retour = ""
            if len(ajoutreels)>1:
                ajoutreels = ajoutreels[:-1]
                retour += f"Ces Pokémon ont été ajoutés à l'équipe de {auteurlettres} : {ajoutreels}\n"
            if max:
                retour += f"Certains Pokémon n'ont pas pu être ajoutés car l'équipe est pleine.\n"
            if dejala:
                retour += f"Ces Pokémon sont déjà dans l'équipe et n'ont donc pas été rajoutés : {dejala}\n"
            if illegal:
                retour += f"Ces Pokémon ne sont pas autorisés dans le tournoi : {illegal}\n"
            if inconnu:
                retour += f"Ces Pokémon n'ont pas été reconnus : {inconnu}\n"
            if precision:
                retour += f"Ces Pokémon doivent être enregistrés en précisant leur forme : {precision}"
            return retour

        elif identiques(ordre1, c.O_DRESSEUR_RETRAIT) and elements:
            # Retrait d'un Pokémon dans la liste du dresseur
            if len(elements) == 0:
                return "Merci de préciser les Pokémon à retirer."
            infosParticipant = gestionDresseurs(f"{c.O_DRESSEUR_MOI}, tech", auteur, auteurlettres)    # On récupère la liste des Pokémon ou le statut d'erreur     
            if infosParticipant == 0:
                return f"{auteurlettres} ne participe pas au tournoi."     
            elif infosParticipant == 400:
                return f"{auteurlettres} a déjà participé à un combat et ne peut plus modifier ses Pokémon."

            # On éclate la liste des Pokémon avant de jouer aux matchs
            pokemonList = [e.strip() for e in infosParticipant.split(",")]
            if pokemonList[0] == "à définir":
                return f"{auteurlettres} n'a aucun Pokémon dans son équipe actuelle."      

            listeAJour = []
            for pokemon in pokemonList:
                aSupprimer = False
                for element in elements:
                    if identiques(pokemon, element):
                        aSupprimer = True
                if not aSupprimer:
                    listeAJour.append(pokemon)

            if len(listeAJour) < len(pokemonList):      # La taille des listes avant/après montre s'il y a eu une suppression
                for dresseur in data["data"]:
                    if dresseur["id"] == auteur:
                        dresseur["pokemon"] = listeAJour
                        # Mise à jour des données
                        dresseurs.seek(0)
                        json.dump(data, dresseurs, indent=4, ensure_ascii=False)
                        dresseurs.truncate()
                        break
                return f"La liste de Pokémon de {auteurlettres} a été mise à jour. Nouveaux Pokémon : {listeAJour}"
            else:
                return f"Aucun changement dans la liste de Pokémon de {auteurlettres}."

    return False