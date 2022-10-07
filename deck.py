"""Définition des decks"""

from enum import Enum, unique
from LeJeu import *
from time import sleep

""" Définition des fonctions des cartes """

def decorate_play(function):
    """Cette fonction génère le décorateur"""
    
    def wrapper(game):
        """Le décorateur qui introduit la carte jouée"""
        print(f"Vous jouez la carte {game.cardplayed}")
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
    if game.other.arg<=0:
        "Votre adversaire n'a pas d'arguments votre action est inutile"

    #Si l'adversaire a des arguments défaussables
    elif game.other.arg>0 and len(l)!=0:
        game.other.arg -= 1
        print("Voici les arguments de votre adversaire: ")
        print(L)
        try :
            card = L.cards[int(input("Quelle carte choisissez vous de supprimer?"))-1]
            game.other.ingame_arg.remove(card)
        except IndexError as e:
            print("Un numéro de carte qui existe plutôt...")

@decorate_play
def play6(game):
    """Un argument basique"""
    game.current.arg +=1
    game.arg_played += 1
    game.current.ingame_arg.append(game.cardplayed)

@decorate_play
def play7(game):
    """Un argument non défaussabl"""
    game.current.arg +=1
    game.arg_played += 1
    game.current.ingame_arg.append(game.cardplayed)

@decorate_play
def play8(game):
    """Un argument pour l'autre camp mais qui fait piocher 3 cartes"""
    game.other.arg +=1
    game.other.ingame_arg.append(game.cardplayed)
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
        except IndexError:
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
    """Réorganise les trois premières cartes de votre deck"""
    print("Voici les trois premières cartes de votre deck: ")
    l = []
    for k in range(3):
        l.append(game.current.deck.draw())
        print(k+1,". ", l[k], '\n')
    indice1 = int(input("Quelle carte voulez vous piocher un premier?"))
    indice2 = int(input("En deuxième?"))
    indice3 = int(input("En dernier?"))
    game.current.deck.cards = game.current.deck.cards + [l[indice3-1], l[indice2-1], l[indice1-1]]
        

""" Création des cartes """

BOUFFE = 11
PICOLE = 12
BEAUF = 13

card1 = Card(1,play1,"Pirouette: Vous pouvez jouer deux arguments de plus pendant ce tour",0)
card2 = Card(0, play2, "Faux Travail: Vous choisissez une carte dans la main de votre adversaire, elle retourne dans son deck",0)
card3 = Card(0,play3,"Salade: Ne sert à rien",0,type=[BOUFFE])
card4 = Card(1, play4, "Kiffeur: Vous choisissez une carte dans la main de votre adversaire",0)
card5 = Card(0, play5, "Pinte de Spritz: L'adversaire se défausse d'un argument",0)
card6 = Card(1, play6, "Jam: Je dois aider pour installer en plus",1)
card7 = Card(1, play7, "Style incontestable: Une fois cet argument joué il ne peut être défaussé",1,discardable=False)
card8 = Card(1, play8, "Pari stupide: cet argument est pour votre adversaire. Vous piochez 3 cartes",0)
card9 = Card(1, play9, "Gros Canon: Si vous n'avez pas d'argument en main, en joue un depuis votre deck",0)
card10 = Card(1, play10, "Jeune investisseur: Vous piochez deux actions",0)
card11 = Card(1, play11, "Courageux: Echangez toutes vos cartes avec des cartes de votre deck",0)
card12 = Card(1, play12, "Bien équipé: Vous réorganisez les trois premières cartes de votre deck",0)


l1 = [card1,card2,card3,card4,card5,card6,card7,card8,card9,card10,card12]
l2 = [card1,card2,card3,card4,card5,card6,card7,card8,card9,card10,card12]

"""Création des deux decks de départ"""

deck1 = Deck(l1)
deck2 = Deck(l2)
deck1.shuffle()
deck2.shuffle()