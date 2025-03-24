###########################################################################
# Toolbox : fonctions utilisées un peu partout
###########################################################################

import unicodedata

# Retire les accents, passe tout en majuscule, puis compare les deux entrées
def identiques(entree1, entree2):
    if not entree1 or not entree2:
        return False
    entree1 = unicodedata.normalize('NFKD', entree1)
    entree1 = ''.join([c_ for c_ in entree1 if not unicodedata.combining(c_)]).upper()

    entree2 = unicodedata.normalize('NFKD', entree2)
    entree2 = ''.join([c_ for c_ in entree2 if not unicodedata.combining(c_)]).upper()

    if entree1 == entree2:
        return True
    return False

# Sépare le contenu de l'ordre en principal et éléments secondaires
def contenuOrdre(ordre):
    if ordre:
        ordres = ordre.split(",")
        ordre1 = ordres[0].strip()
        elements = []
        if len(ordre.split(",")) > 1:
            elements = [e.strip() for e in ordres[1:]]
        
        return ordre1, elements
    else:
        return False, False
    