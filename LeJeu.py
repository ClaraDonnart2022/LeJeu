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
    pass
        
 







