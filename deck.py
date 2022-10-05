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
    print("On applique l'action Kiffeur: Voici les cartes de votre adversaire: \n")
    print(game.other.hand)
    cardnum = int(input("Quelle carte choisissez vous ?"))
    game.current.cards.append(game.other.cards.pop(cardnum-1))

def play5(game):
    print("On applique l'action Pinte de Spritz: L'adversaire perd un argument")
    if game.other.arg >0:
        game.other.arg -= 1 

            

""" Création des cartes """

Bouffe = 11
Picole = 12
Beauf = 13

card1 = Card(1,play1,"Pirouette: Vous pouvez jouer deux arguments de plus pendant ce tour (Action)",0)
card2 = Card(0, play2, "Faux Travail: Vous choisissez une carte dans la main de votre adversaire, elle retourne dans son deck (Action)",0)
card3 = Card(1,play3,"Salade: Ne sert à rien (Action)",0,[Bouffe])
card4 = Card(1, play4, "Kiffeur: Vous choisissez une carte dans la main de votre adversaire",0)
card5 = Card(1, play4, "Pinte de Spritz: L'adversaire se défausse d'un argument",0)
l1 = [card1,card2,card3,card4]

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