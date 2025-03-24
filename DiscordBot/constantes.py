###########################################################################
# Constantes du programme
###########################################################################

# ATTENTION TOKEN DOIT ÊTRE MASQUÉ AVANT LE PARTAGE
token = "REDACTED"
arclight = "REDACTED"

# Pour l'instant gestion manuelle de ces cas-là. À voir si on fait ça dynamiquement dans le futur, probablement inutile
serveursAutorises = ["Serveur de Vinc2612", "Pokémon Reborn FR"]
# Vinc2612, Blatha, Prag, Teto
superutilisateurs = [141195266555379712, 792098954342957096, 305775114954473474, 451369556020035584]
animateurs = [1198625640610529290]

# Liste des fonctions du bot
# S_ : sujet, correspond à l'information entre $ et la première espace
# O_ : ordre, correspond à ce qui est obtenu après la première espace
S_INFOS = "Infos"
O_INFOS_DIVERS = "Divers"

S_LIGUE = "Li"
O_LIGUE_GENERAL = "Général"
O_LIGUE_REGLES = "Règles"

S_CHAMPION = "Ch"
O_CHAMPION_AJOUT = "+"
O_CHAMPION_RETRAIT = "-"
O_CHAMPION_RECHERCHE = "?"
O_CHAMPION_TOUS = "Tous"

S_DRESSEUR = "Dr"
O_DRESSEUR_INSCRIP = "Inscription"
O_DRESSEUR_MOI = "Moi"
O_DRESSEUR_LUI = "Lui"
O_DRESSEUR_ELLE = "Elle"
O_DRESSEUR_AJOUT = "+"
O_DRESSEUR_RETRAIT = "-"

S_VICTOIRE = "Victoire"
S_DEFAITE = "Défaite"

S_CHUT = "Chut"
O_CHUT_ACTIV = "+"
O_CHUT_DESACT = "-"

S_MUTE = "Mute"
O_MUTE_AJOUT = "+"
O_MUTE_RETRAIT = "-"

S_POINTS = "Points"
O_POINTS_AJOUT = "+"
O_POINTS_RECTIF = "-"
O_POINTS_SCORE = "?"
O_POINTS_CLASSEMENT = "Top"

S_HOF = "HOF"
O_HOF_VICTOIRE = "+"
O_HOF_DEFAITE = "-"
O_HOF_ACTUEL = "Maître"
O_HOF_HISTO = "Historique"

S_VEBUG = "Vebug"

# Liste des types dans leur graphie officielle, pour éviter les doublons
TYPES = ["Normal", "Fée", "Eau", "Glace", "Feu", "Combat", "Roche", "Sol", "Acier", "Électrik", "Vol", "Dragon", "Psy", "Insecte", "Spectre", "Ténèbres", "Plante", "Poison"]