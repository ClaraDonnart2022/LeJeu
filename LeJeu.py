"""
1: Hadri
2: Clarou
3: Neutre
"""

from re import L
from random import shuffle

class Card():
    """une carte"""

    def __init__(self, color, play, description:str, argum:bool) -> None:
        self.color = color
        self.play = play
        self.description = description
        self.arg = argum

    def __str__(self):
        return(self.description)


class Deck():
    """Un deck"""

    def __init__(self, cards:list):
        self.cards = cards

    def __str__(self):
        return " \n".join([str(c) for c in self.cards])

    def draw(self):
        return(self.cards.pop(-1))

    def shuffle(self):
        shuffle(self.cards)


class Hand():

    def __init__(self,deck):
        self.cards = []
        for i in range(3):
            self.cards.append(deck.draw())
    
    def __str__(self):
        return " \n".join([str(i+1)+". "+str(c) for i,c in enumerate(self.cards)])

#class Game():


class Player():

    def __init__(self, name:str, deck):
        self.name = name
        self.deck = deck
        self.hand = Hand(deck)
        self.arg = 0

    @property 
    def cards(self):
        return(self.hand.cards)    

if __name__ == "__main__":
    

    #But = Arriver à 5 arguments / plus d'arg que l'autre à la fin

    """ Définition des fonctions des cartes """

    def play1():
        print("Appliquer le play de la carte 1")

    def play2():
        print("Appliquer le play de la carte 2")

    def play3():
        print("Appliquer le play de la carte 3")

    def play4():
        print("Appliquer le play de la carte 4")
    

    """ Création des cartes """

    a = Card(1,play1,"Je suis la carte 1",0)
    b = Card(1, play2, "Je suis la carte 2",1)
    c = Card(1,play3,"Je suis la carte 3",1)
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

    """ Création pile de discard """

    discard = []

    """ JEUUUUUUUUUUUUUUU """
    i = 0
    A = True

    current = Player("Hadri", deck1)
    other = Player("Clarou", deck2)

    while A:

        current.cards.append(current.deck.draw())
        print(f"C'est le tour de {current.name}. Voici tes cartes:")
        rep = "j"
        while rep == "j" and len(current.cards)!=0:
            print(current.hand)
            rep = input("Veux-tu jouer une carte (j) ou passer (p)?")
            if rep == "j":
                try :
                    cardplay = int(input("Laquelle?"))   
                    current.cards[cardplay-1].play()
                    cardplayed = current.cards.pop(cardplay-1)
                    if cardplayed.arg:
                        current.arg +=1
                    discard.append(cardplayed)
                except ValueError as e:
                    print("Grand fou met un numéro")
                except IndexError as e:
                    print("Un numéro que tu as plutôt coco")

            print(f"Vous avez {current.arg} argument(s)")
        current,other = other, current
        
 







