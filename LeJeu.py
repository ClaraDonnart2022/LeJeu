"""
1: Hadri
2: Clarou
3: Neutre
"""

from re import L
from random import shuffle

class Card:
    """une carte"""

    def __init__(self, color, play, description:str, argum:bool, type=[],discardable=True) -> None:
        self.color = color
        self.play = play
        self.description = description
        self.arg = argum
        self.type = type
        self.discardable = discardable

    def __str__(self):
        return(self.description)


class Deck:
    """Un deck"""

    def __init__(self, cards:list):
        self.cards = cards

    def __str__(self):
        return " \n".join([str(i+1)+". "+str(c) for i,c in enumerate(self.cards)])

    def draw(self):
        return(self.cards.pop(-1))


    def draw_argument(self):
        """Pioche le premier argument du deck, cette fonction retourne None si il n'y en a plus dans le deck."""
        c = self.cards[0]
        i=0
        try:
            while not c.arg:
                i+=1
                c = self.cards[i]
            return(self.cards.pop(i))
        except IndexError: 
            return None
        

    def draw_action(self):
    #TODO: Gérer quand il n'y a plus d'action (sinon boucle infinie)
        c = self.cards[0]
        i=0
        while c.arg:
            try:
                i+=1
                c = self.cards[i]
            except IndexError: 
                return None
        return(self.cards.pop(i))

    def shuffle(self):
        shuffle(self.cards)

    def append(self,c):
        self.cards.append(c)


class Hand:

    def __init__(self,deck,nhand = 3):
        self.cards = []
        for i in range(nhand):
            try:
                self.cards.append(deck.draw())
            except IndexError:
                pass  # deck vide
            
    
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
        self.arg_played = 0

    def turn(self):
         #TODO: gérer mettre un numéro à la place de j et espace qui fait rien.
        self.arg_played = 0
        try:
            self.current.cards.append(self.current.deck.draw())
        except IndexError:
            pass  # deck vide
        
        print(f"C'est le tour de {self.current.name}. Voici tes cartes:")
        rep = "j"
        while rep == "j" and len(self.current.cards)!=0:
            print(self.current.hand)
            rep = input("Veux-tu jouer une carte (j) ou passer (p)?")
            if rep == "j":
                try :
                    numcardplay = int(input("Laquelle?"))
                    self.cardplayed = self.current.cards[numcardplay-1]

                    #Si le joueur n'a pas encore joué d'argument ou que la carte n'est pas un argument
                    if(self.arg_played<1 or self.cardplayed.arg == False):
                        self.cardplayed.play(self)
                        self.current.cards.pop(numcardplay-1)
                        self.discard.append(self.cardplayed)
                    else:
                        print("Vous avez joué trop d'arguments")
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
        self.ingame_arg = []

    @property 
    def cards(self):
        return(self.hand.cards)    

    def __str__(self):
        return " \n".join([str(i+1)+". "+str(c) for i,c in enumerate(self.ingame_arg)])
    

if __name__ == "__main__":
    pass
        

        
 







