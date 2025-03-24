###########################################################################
# Infos : recrache le savoir de Flobot en fonction de la demande
###########################################################################

import constantes as c
from toolbox import contenuOrdre, identiques

def gestionInfos(ordre):

    retour = False
    if not ordre:
        retour = "Ce sujet se nomme Flobot, assistant de la Ligue Pokémon Reborn FR.\n"
        retour += "Ce sujet peut vous renseigner à propos de :\n"
        retour += f" • {c.S_LIGUE} : Règles de la Ligue Pokémon Reborn FR.\n"
        retour += f" • {c.S_CHAMPION} : Gestion des champions de la ligue Pokémon Reborn FR. \n"
        retour += f" • {c.S_DRESSEUR} : Gestion des dresseurs défiant la ligue Pokémon Reborn FR. \n"
        retour += f" • Certaines actions sont réservées aux champions, pour le suivi de la ligue Pokémon Reborn FR. Plus d'informations sur le sujet '{c.O_INFOS_DIVERS}'\n"
        retour += f"Pour plus d'informations, vous pouvez utiliser la commande '${c.S_INFOS} [Sujet]'."
    
    if identiques(ordre, c.S_LIGUE):
        retour = "Ce sujet peut vous renseigner sur de nombreux aspects de la Ligue Pokémon Reborn FR.\n"
        retour += "Voici les différentes questions auxquelles ce sujet peut vous répondre :\n"
        retour += f" • '${c.S_LIGUE} {c.O_LIGUE_GENERAL}' : Informations sur le fonctionnement général du tournoi telles que les dates ou le format\n"
        retour += f" • '${c.S_LIGUE} {c.S_DRESSEUR}' : Informations nécessaires aux participants sur l'inscription et la composition de l'équipe\n"
        retour += f" • '${c.S_LIGUE} {c.S_CHAMPION}' : Informations sur les champions et leurs restrictions\n"
        retour += f" • '${c.S_LIGUE} {c.O_LIGUE_REGLES}' : Informations sur les règles et clauses applicables dans chaque combat."
    
    if identiques(ordre, c.S_CHAMPION):
        retour = "Ce sujet peut informer sur la liste des champions de la Ligue Pokémon Reborn FR et peut également la mettre à jour.\n"
        retour += "Voici les différentes informations et actions auxquelles ce sujet a accès :\n"
        retour += f" • '${c.S_CHAMPION} {c.O_CHAMPION_AJOUT}, Tag, Type, Terrain, Style, Titre' : Utilisateurs autorisés. Ajoute le champion à la liste des champions actifs\n"
        retour += f" • '${c.S_CHAMPION} {c.O_CHAMPION_RETRAIT}, Tag' : Utilisateurs autorisés. Retire le champion de la liste des champions actifs\n"
        retour += f" • '${c.S_CHAMPION} {c.O_CHAMPION_RECHERCHE}, Élément' : Recherche les informations du champion concerné par l'élément. Éléments reconnus : Tag, type, terrain\n"
        retour += f" • '${c.S_CHAMPION} {c.O_CHAMPION_TOUS}' : Liste l'ensemble des champions actifs."
    
    if identiques(ordre, c.S_DRESSEUR):
        retour = "Ce sujet peut informer sur la liste des participants de la Ligue Pokémon Reborn FR. Il vous assiste également à l'inscription.\n"
        retour += "Voici les différentes informations et actions auxquelles ce sujet a accès :\n"
        retour += f" • '${c.S_DRESSEUR} {c.O_DRESSEUR_INSCRIP}' : Inscrit le dresseur à la Ligue Pokémon Reborn FR\n"
        retour += f" • '${c.S_DRESSEUR} {c.O_DRESSEUR_MOI}' : Résume le statut du dresseur au sein de la Ligue Pokémon Reborn FR\n"
        retour += f" • '${c.S_DRESSEUR} Tag' : Résume le statut du dresseur considéré au sein de la Ligue Pokémon Reborn FR\n"
        retour += f" • '${c.S_DRESSEUR} {c.O_DRESSEUR_AJOUT}, Pokémon, Pokémon, Pokémon...' : Ajoute un Pokémon à l'équipe du dresseur dans la limite des 18 disponibles\n"
        retour += f" • '${c.S_DRESSEUR} {c.O_DRESSEUR_RETRAIT}, Pokémon, Pokémon, Pokémon...' : Retire un Pokémon de l'équipe du dresseur\n"
        retour += "Les Pokémon à rajouter ou supprimer peuvent être référencés par leur numéro de Pokédex, leur nom français ou leur nom anglais. Des précisions sur les formes peuvent être demandées.\n"
        retour += "Attention : l'équipe du dresseur sera verrouillée au moment de son premier combat officiel."

    if identiques(ordre, c.O_INFOS_DIVERS):
        retour = "En tant que champion, vous pouvez mettre à jour le résultat des matchs avec les commandes suivantes :\n"
        retour += f" • '${c.S_VICTOIRE} Tag' : Remets le badge au dresseur Tag\n"
        retour += f" • '${c.S_DEFAITE} Tag' : Archive la défaite du dresseur Tag"

    return retour

def gestionLigue(ordre):
    retour = False

    if not ordre:
        retour = gestionInfos(c.S_LIGUE)
        return retour

    if identiques(ordre, c.O_LIGUE_GENERAL):
        retour = "Ce sujet vous souhaite la bienvenue sur la Ligue Pokémon Reborn FR.\n"
        retour += "Voici les informations générales que ce sujet peut partager :\n"
        retour += " • Les combats se déroulent sur Pokémon Reborn, en version 19.5+. Cette version n'est pas compatible avec la traduction française. Cette version doit être téléchargée sur le site officiel de Pokémon Reborn.\n"
        retour += " • Dix-huit champions d'arène, un par type, doivent être affrontés et vaincus dans l'ordre de votre choix\n"
        retour += " • Une victoire contre l'un des champions vous remportera son badge\n"
        retour += " • Les défaites ne sont pas éliminatoires. Le champion peut être défié autant de fois que le souhaite le dresseur\n"
        retour += " • Les champions peuvent être trouvés sur le serveur Discord de Pokémon Reborn FR. En cas de difficulté, le combat peut être organisé à une date précise.\n"
        retour += f"Plus d'informations sur les champions sont disponibles via la commande '${c.S_CHAMPION} {c.O_CHAMPION_TOUS}'."
    
    if identiques(ordre, c.S_DRESSEUR):
        retour = "Les dresseurs inscrits au tournoi peuvent participer à la Ligue Pokémon Reborn FR.\n"
        retour += "Voici les informations nécessaires au bon déroulement du tournoi :\n"
        retour += " • Votre équipe est composée de 18 Pokémon. Pour chaque combat, vous pouvez emmener les six Pokémon de votre choix\n"
        retour += " • En dehors de Vémini et Mandrillon, tous les Pokémon disponibles avant la Ligue Pokémon (en jeu) sont autorisés, à savoir tous les Pokémon non légendaires, non mythiques et non Ultra-Chimère, ainsi que Phione, Type:0 et Silvallié\n"
        retour += " • Les sets des Pokémon peuvent être modifiés entre chaque combat, en dehors des formes innées (forme impossible à changer en jeu)\n"
        retour += " • Le mode DEBUG est autorisé pour la création de l'équipe. Pokémon Reborn intègre un contrôle de légalité et bloque donc naturellement les Pokémon illégaux.\n"
        retour += "Note sur les formes : les formes innées correspondent aux formes fixées à la naissance ou à l'évolution, telles que les formes d'Alola, la taille de Banshitrouye, le sexe de Mystigrix. Les changements de forme purement esthétiques sont tolérés (tel que Tritosor)"
    
    if identiques(ordre, c.S_CHAMPION):
        retour = "Les champions de la Ligue Pokémon Reborn FR sont soumis à des limitations différentes des dresseurs :\n"
        retour += " • L'équipe du champion possède un type en commun. Les types du Pokémon ou de sa méga-évolution sont considérés\n"
        retour += " • Comme pour les dresseurs, seuls les Pokémon disponibles avant la Ligue Pokémon (en jeu) sont autorisés, à savoir tous les Pokémon non légendaires, non mythiques, Phione, Type:0 et Silvallié\n"
        retour += " • Les six Pokémon, leurs sets, leur ordre, le terrain et le format sont fixés pour l'intégralité du tournoi \n"
        retour += f"Découvrez les différents champions de la Ligue Pokémon Reborn FR via la commande '${c.S_CHAMPION} {c.O_CHAMPION_TOUS}'."
    
    if identiques(ordre, c.O_LIGUE_REGLES):
        retour = "Lors des combats, ces différentes règles doivent être respectées :\n"
        retour += " • Species Clause : un dresseur ne peut pas jouer deux Pokémon partageant le même numéro de Pokédex\n"
        retour += " • OHKO Clause : les capacités Abîme, Glaciation, Empal'Korne et Guillotine sont interdites\n"
        retour += " • Evasion Clause : les capacités Reflet et Lilliput sont interdites, ainsi que les objets Poudreclaire et Encens Doux\n"
        retour += " • Baton Pass Clause : la capacité Relais est limitée à un seul Pokémon sur les six\n"
        retour += " • Z Clause : les capacités Z sont interdites (cette clause est nécessaire car les attaques Z provoquent des anomalies lors du jeu en ligne)\n"
        retour += " • Moody Clause : le talent Lunatique est interdit\n"
        retour += " • Sleep Clause : si un Pokémon adverse est endormi par un effet différent de Repos, il est interdit d'utiliser une capacité qui, lorsqu'elle touche, garantie l'endormissement."
    
    return retour


        