"""Définition des decks"""

from enum import Enum, unique
from LeJeu import *
from time import sleep
from random import *

""" Définition des fonctions des cartes """

def decorate_play(function):
    """Cette fonction génère le décorateur:
    """
    def wrapper(game):
        """Le décorateur qui introduit la carte jouée"""
        print(f"Vous jouez la carte {game.card_played}")
        result = function(game)
        return result
    return wrapper

def decorate_type(function):
    """Cette fonction génère le décorateur: 
    """
    def wrapper(game):
        """décorateur: si la carte spe est en jeu, l'itère de 1
        dans la limite de 3 (se transforme en argument)"""
        #Si la carte spe a été jouée -> On augmente le compteur de 1
        
        CARD_SPE = [game.current.princesse_des_coeurs, game.current.roi_de_la_bouffe]
        for card_spe in CARD_SPE:
            if card_spe[1] is not None and card_spe[2] in game.card_played.type:
                card_spe[0] += 1
                #Si 3 cartes du bon type ont été jouées, la carte est un argument en jeu, on ajoute 1 au nombre d'arguments joués.
                print(card_spe[0])
                if card_spe[0] == 3:
                    game.current.ingame_arg.append(card_spe[1])      
        result = function(game)
        return result
    return wrapper

@decorate_play
def play1(game):
    """Pirouette: Vous pouvez jouer deux arguments de plus pendant ce tour"""
    game.arg_played -=2

@decorate_play
def play2(game):
    """Faux Travail: Vous choisissez une carte dans la main de votre adversaire, elle retourne dans son deck"""
    print("Voici les cartes de votre adversaire: \n")
    print(game.other.hand)
    cardnum = int(input("Quelle carte choisissez vous ?"))
    game.other.deck.append(game.other.cards.pop(cardnum-1))
    game.other.deck.shuffle()

@decorate_play
@decorate_type
def play3(game):
    """Salade: Ne sert à rien"""
    sleep(1)
    print("\n ...\n")
    sleep(1)
    print("il ne se passe rien")

@decorate_play
def play4(game):
    """Kiffeur: Vous choisissez une carte dans la main de votre adversaire"""
    print(game.other.hand)
    cardnum = int(input("Quelle carte choisissez vous ?"))
    game.current.cards.append(game.other.cards.pop(cardnum-1))

@decorate_play
def play5(game):
    """Pinte de Spritz: L'adversaire se défausse d'un argument"""
    l = [c for c in game.other.ingame_arg if c.discardable]
    L = Deck(l)

    #Si l'adversaire a pas d'argument
    if len(game.other.ingame_arg)<=0:
        "Votre adversaire n'a pas d'arguments votre action est inutile"

    #Si l'adversaire a des arguments défaussables
    elif len(game.other.ingame_arg)>0 and len(l)!=0:
        print("Voici les arguments de votre adversaire: ")
        print(L)
        try :
            card = L.cards[int(input("Quelle carte choisissez vous de supprimer?"))-1]
            game.other.ingame_arg.remove(card)
        except IndexError as e:
            print("Un numéro de carte qui existe plutôt...")

@decorate_play
@decorate_type
def play6(game):
    """Un argument"""
    game.arg_played += 1
    game.current.ingame_arg.append(game.card_played)


@decorate_play
def play8(game):
    """Un argument pour l'autre camp mais qui fait piocher 3 cartes"""
    game.other.ingame_arg.append(game.card_played)
    for k in range(3):
        try:
            game.current.cards.append(game.current.deck.draw())
        except IndexError:
            pass  # deck vide
        
@decorate_play
def play9(game):
    """Si le joueur courant n'a pas d'argument en main, en joue un depuis son deck"""
    l_hand = [c.arg for c in game.current.cards]
    if not True in l_hand:
        try:
            card_drawn = game.current.deck.draw_argument()
            card_drawn.play(game)
        except AttributeError:
            print("Il n'y plus d'argument dans votre deck cette carte n'a pas d'effet.")
            pass
    else:
        print("Vous avez un argument en main, cette carte n'a pas d'effet")
        
@decorate_play
def play10(game):
    """Pioche deux actions du deck"""
    for i in range(2):
        card_drawn= game.current.deck.draw_action()
        if card_drawn is not None:
            game.current.cards.append(card_drawn)
    
@decorate_play
def play11(game):
    """Remplace toutes ses cartes par des cartes du deck"""
    nbcards = len(game.current.cards)
    newHand = Hand(game.current.deck, nbcards)
    game.current.deck.cards= game.current.deck.cards + game.current.cards
    game.current.hand = newHand
    game.current.deck.shuffle()

@decorate_play
def play12(game):
    """Bien équipé: Réorganise les trois premières cartes de votre deck"""
    l = game.view_n_fist_cards_of_deck(3)
    indice1 = int(input("Quelle carte voulez vous piocher un premier?"))
    indice2 = int(input("En deuxième?"))
    indice3 = int(input("En dernier?"))
    game.current.deck.cards = game.current.deck.cards + [l[indice3-1], l[indice2-1], l[indice1-1]]
        
@decorate_play
def play13(game):
    """Baillement: Vous défaussez une carte. votre adversaire en défausse deux"""
    game.current.nb_of_card_to_discard=1
    game.other.nb_of_card_to_discard=2
    for player in [game.current, game.other]:
        for k in range(player.nb_of_card_to_discard):
            print(f"Voici les cartes de {player.name}: ")
            sleep(1)
            print(player.hand)
            card_chosen = player.cards[int(input("Quelle carte voulez vous défausser? "))-1]
            game.discard_card(card_chosen,player)

#TODO: gérer si jouée deux fois
@decorate_play
def play14(game):
    """Roi de la Bouffe: Cette action reste en jeu. Jouez 3 cartes BOUFFE pour la transformer en argument."""
    game.current.roi_de_la_bouffe[1] = game.card_played

@decorate_type
@decorate_play
def play16(game):
    """Princesse des coeurs: Cette action reste en jeu. Jouez 3 cartes BOUFFE pour la transformer en argument."""
    game.current.princesse_des_coeurs[1] = game.card_played

@decorate_play
def play17(game):
    """Sieste inopinée: l'adversaire passe son prochain tour"""
    game.other.allowed_to_play[0] = False

@decorate_play
def play18(game):
    """Rire mignon: L'adversaire se défausse d'une carte aléatoire"""
    #Choisit une carte alétoire du deck de l'adversaire
    card = choice(game.other.cards)
    game.discard_card(card,game.other)

@decorate_play
def play19(game):
    """Posé: Votre adversaire ne peut pas jouer plus de deux cartes au prochain tour."""
    game.other.allowed_to_play[1] = 2

@decorate_play
def play21(game):
    """Courageuse?: Vous échangez une carte de votre main avec une carte au choix parmi les trois premières de votre deck"""
    l = game.view_n_fist_cards_of_deck(3)
    indice = int(input("Quelle carte voulez vous prendre?"))
    game.current.cards.append(l[indice-1])
    print(game.current.hand)
    indice = int(input("Contre quelle carte?"))
    game.discard_card(game.current.cards[indice-1],game.current)
    game.current.deck.cards = game.current.deck.cards.append(l[indice-1])




""" Création des cartes """

card1 = Card(HADRI,play1,"Pirouette: Vous pouvez jouer deux arguments de plus pendant ce tour",0)
card2 = Card(NEUTRE, play2, "Faux Travail: Vous choisissez une carte dans la main de votre adversaire, elle retourne dans son deck",0)
card3 = Card(NEUTRE,play3,"Salade: Ne sert à rien",0,type=[BOUFFE])
card4 = Card(HADRI, play4, "Kiffeur: Vous choisissez une carte dans la main de votre adversaire",0)
card5 = Card(NEUTRE, play5, "Pinte de Spritz: L'adversaire se défausse d'un argument",0)
card6 = Card(HADRI, play6, "Jam: Je dois aider pour installer en plus",1)
card7 = Card(HADRI, play6, "Style incontestable: Une fois cet argument joué il ne peut être défaussé",1,discardable=False)
card8 = Card(HADRI, play8, "Pari stupide: cet argument est pour votre adversaire. Vous piochez 3 cartes",0)
card9 = Card(HADRI, play9, "Gros Canon: Si vous n'avez pas d'argument en main, en joue un depuis votre deck",0)
card10 = Card(HADRI, play10, "Jeune investisseur: Vous piochez deux actions",0)
card11 = Card(HADRI, play11, "Courageux: Echangez toutes vos cartes avec des cartes de votre deck",0)
card12 = Card(HADRI, play12, "Bien équipé: Vous réorganisez les trois premières cartes de votre deck",0)
card13 = Card(NEUTRE, play13, "Baillement: Vous défausser une carte. Votre adversaire en défausse deux",0)
card14 = Card(HADRI, play14, "Roi de la Bouffe: Cette action reste en jeu. Jouez 3 cartes Bouffe pour la transformer en Argument",0,type=[BOUFFE])
card15 = Card(CLAROU, play6, "Style incontestable: Une fois cet argument joué il ne peut être défaussé",1,type=[BEAUF],discardable=False)
card16 = Card(CLAROU, play16, "Princesse des coeurs: Cette action reste en jeu. Jouez 3 cartes Amour pour la transformeren Argument.",0, type = [AMOUR])
card17 = Card(CLAROU, play17, "Sieste inopinée: L'adversaire passe son prochain tour",0)
card18 = Card(CLAROU, play18, "Rire mignon: l'adversaire se défausse d'une carte aléatoire",0)
card19 = Card(HADRI, play19, "Posé: Votre adversaire ne peut pas jouer plus de deux cartes au prochain tour", 0, type = [BEAUF])
card20 = Card(CLAROU, play6, "(Argument) Journée de la femme: J'y peux rien c'est aujourd'hui",1)
card21 = Card(CLAROU, play21, "Courageuse?: Vous échangez une carte de votre main avec une carte au choix parmi les trois premières de votre deck",0)
#card21 = Card(CLAROU, play21, "Courageuse?: Vous échangez une carte de votre main avec une carte au choix parmi les trois premières de votre deck",0)


l1 = [card21,card21,card21,card21,card21,card18,card18,card18,card9,card10,card14]
l2 = [card12,card12,card12,card12,card5,card6,card7,card8,card9,card10,card14]

"""Création des deux decks de départ"""

deck1 = Deck(l1)
deck2 = Deck(l2)
deck1.shuffle()
deck2.shuffle()