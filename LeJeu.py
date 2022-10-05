"""
1: Hadri
2: Clarou
3: Neutre
"""

from re import L
from random import shuffle

class Card:
    """une carte"""

    def __init__(self, color, play, description:str, argum:bool) -> None:
        self.color = color
        self.play = play
        self.description = description
        self.arg = argum

    def __str__(self):
        return(self.description)


class Deck:
    """Un deck"""

    def __init__(self, cards:list):
        self.cards = cards

    def __str__(self):
        return " \n".join([str(c) for c in self.cards])

    def draw(self):
        return(self.cards.pop(-1))

    def shuffle(self):
        shuffle(self.cards)


class Hand:

    def __init__(self,deck):
        self.cards = []
        for i in range(3):
            self.cards.append(deck.draw())
    
    def __str__(self):
        return " \n".join([str(i+1)+". "+str(c) for i,c in enumerate(self.cards)])

class Game:
    """ Un jeu de LeJeu."""

    def __init__(self):
        players = ["Hadri", "Clarou"]

        """ Définition des decks """

        from deck import deck1, deck2
        self.current = Player(players[0],deck1)
        self.other = Player(players[1], deck2)
        self.discard = []

    def turn(self):

        self.current.cards.append(self.current.deck.draw())
        print(f"C'est le tour de {self.current.name}. Voici tes cartes:")
        rep = "j"
        while rep == "j" and len(self.current.cards)!=0:
            print(self.current.hand)
            rep = input("Veux-tu jouer une carte (j) ou passer (p)?")
            if rep == "j":
                try :
                    cardplay = int(input("Laquelle?"))   
                    self.current.cards[cardplay-1].play()
                    cardplayed = self.current.cards.pop(cardplay-1)
                    if cardplayed.arg:
                        self.current.arg +=1
                    self.discard.append(cardplayed)
                except ValueError as e:
                    print("Grand fou met un numéro")
                except IndexError as e:
                    print("Un numéro que tu as plutôt coco")

            print(f"Vous avez {self.current.arg} argument(s)")
            self.current, self.other = self.other, self.current



class Player:

    def __init__(self, name:str, deck):
        self.name = name
        self.deck = deck
        self.hand = Hand(deck)
        self.arg = 0

    @property 
    def cards(self):
        return(self.hand.cards)    

if __name__ == "__main__":
    pass
        

        
 







