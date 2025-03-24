###########################################################################
######                                                               ######
######     FLOBOT : BOT DISCORD POUR LE SERVEUR POKÉMON REBORN FR    ######
######                                                               ######
###########################################################################

# Imports du Main (flobot.py)
import discord
from discord import DMChannel
import constantes as c
import champions as ch
import dresseurs as dr
import hof
import pointsjeux as pj
import divers as di
import infos as i
from habilitations import hab, mute
from toolbox import identiques

# Variables globales
intents = discord.Intents.default()
intents.message_content = True
modeChut = False
missingId = di.getMissingDtag()
client = discord.Client(intents=intents)

# Debug pour login réussi
@client.event
async def on_ready():
    print(f'Login réussi en tant que {client.user}')

###########################################################################
# Corps du bot : gestion des messages reçus
@client.event
async def on_message(message):
    if message.author == client.user:           # On ignore les messages de Flobot
        return
    
    missingId = di.getMissingDtag()
    if missingId != False:
        if message.author.id in missingId:
            missingId = di.fixChamp(message.author.id, message.author.global_name)

    msg = message.content                       # On récupère le message
    if not msg.startswith('$'):                 # On ignore les messages n'étant pas préfixés par $
        return
    msg = msg[1:]

    auteur = message.author.id                  # On récupère l'auteur et le serveur
    auteurlettres = message.author.global_name  
    if isinstance(message.channel, DMChannel):
        serveur = False
    else:
        serveur = message.guild.name

    # Niveau d'habilitation pour traitement du message
    # niv_a = admin
    # niv_c = champion (gym leader)
    # niv_s = standard (infos pour le public)
    # niv_z = minimum (infos pour soi)
    niv_a, niv_c, niv_s, niv_z = hab(auteur=auteur, serveur=serveur)

    # On filtre déjà s'il n'y a aucune habilitation :
    if not (niv_a or niv_c or niv_s or niv_z):
        return

    # Séparation du message entre ordre et précisions 
    sujet = msg.split()[0]                # Le premier mot de la commande définit vers où on va
    if len(msg.split()) > 1:                # La suite donne les précisions sur la commande
        ordre = msg.split(maxsplit=1)[1]
    else:
        ordre = False

    # Vincent Debug
    if auteur == 141195266555379712 and identiques(sujet, c.S_VEBUG):
        print(ordre)
        print(message)
        return

    # Mute ou unmute une personne
    if niv_a and identiques(sujet, c.S_MUTE):
        retour = mute(ordre)
        if retour:
            await message.channel.send(retour)
            return
        return

    #  Gestion du mode "Chut" : Flobot se taira pour toute autre demande
    global modeChut
    if niv_a and identiques(sujet, c.S_CHUT):
        modeChut, retour = di.ModeChut(ordre, modeChut)
        if retour:
            await message.channel.send(retour)
            return
        return
    if modeChut and not niv_z:
        return

    # Gestion des infos
    # Nécessite le niveau minimal d'habilitation : soit dans une pièce privée (MP), soit un utilisateur avec droit de diffusion
    if identiques(sujet, c.S_INFOS):
        if niv_z:
            retour = i.gestionInfos(ordre)
            if retour:
                await message.channel.send(retour)
        return
    elif identiques(sujet, c.S_LIGUE):
        if niv_z:
            retour = i.gestionLigue(ordre)
            if retour:
                await message.channel.send(retour)
        return

    # Gestion des champions : on transmet les habilitations admin (ajout suppression de champion) ou minimum pour informations
    if identiques(sujet, c.S_CHAMPION):
        retour = ch.gestionChampions(ordre, niv_a, niv_c, niv_z)
        if retour:
            await message.channel.send(retour)
        return
    
    # Gestion des participants : possible en MP ou en public
    if identiques(sujet, c.S_DRESSEUR) and (niv_s or niv_z):
        retour = dr.gestionDresseurs(ordre, auteur, auteurlettres)
        if retour:
            await message.channel.send(retour)
        return

    # Gestion victoire ou defaite : uniquement pour les champions
    if identiques(sujet, c.S_VICTOIRE) and niv_c:
        retour = di.remettreBadge(auteur, ordre)
        if retour:
            await message.channel.send(retour)
        return
    elif identiques(sujet, c.S_DEFAITE) and niv_c:
        retour = di.archiverDefaite(auteur, ordre)
        if retour:
            await message.channel.send(retour)
        return
    
    # Gestion jeux du serveur
    if identiques(sujet, c.S_POINTS) and (niv_a or auteur in c.animateurs):
        retour, missingId = pj.jeuxapoints(ordre, missingId)
        if retour:
            await message.channel.send(retour)
        return
    
    if identiques(sujet, c.S_HOF):
        retour = hof.gestionMaitres(ordre, auteur, niv_a, niv_c)
        if retour:
            await message.channel.send(retour)

client.run(c.token)