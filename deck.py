"""Définition des decks"""

from LeJeu import *
""" Définition des fonctions des cartes """

def play1(game):
    print("On applique l'action Pirouette: Vous pouvez jouer deux arguments de plus pendant ce tour")
    game.arg_played -=2

def play2(game):
    print("On applique l'action Faux travail: Voici les cartes de votre adversaire: \n")
    print(game.other.hand)
    cardnum = int(input("Quelle carte choisissez vous ?"))
    game.other.deck.append(game.other.cards.pop(cardnum-1))
    game.other.deck.shuffle()


def play3(game):
    print("Vous jouez salade: \n ...\n il ne se passe rien")

def play4(game):
    print("Appliquer le play de la carte 4")
            

""" Création des cartes """

a = Card(1,play1,"Pirouette: Vous pouvez jouer deux arguments de plus pendant ce tour (Action)",0)
b = Card(0, play2, "Faux Travail: Vous choisissez une carte dans la main de votre adversaire, elle retourne dans son deck (Action)",0)
c = Card(1,play3,"Salade: Ne sert à rien (Action)",0)
d = Card(1, play4, "Je suis la carte 4",0)
l1 = [a,b,c,d]

a = Card(2,play1,"Je suis la carte 5",1)
b = Card(2, play2, "Je suis la carte 6",0)
c = Card(2,play3,"Je suis la carte 7",1)
d = Card(2, play4, "Je suis la carte 8",0)
l2 = [a,b,c,d]

"""Création des deux decks de départ"""

deck1 = Deck(l1)
deck2 = Deck(l2)
deck1.shuffle()
deck2.shuffle()