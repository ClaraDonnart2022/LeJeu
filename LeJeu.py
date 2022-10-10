"""
1: Hadri
2: Clarou
3: Neutre
"""

from re import L
from random import shuffle

HADRI = 1
CLAROU = 2
NEUTRE = 3
AMOUR = 10
BOUFFE = 11
PICOLE = 12
BEAUF = 13
NB_OF_CARD_IN_DECK = 20


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

    #TODO: créer un draw_type(self,type= None) qui combine draw draw_argument et draw_action
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
        """Pioche la première action du deck: s'il n'y en a plus retourne None"""
        c = self.cards[0]
        i=0
        try:
            while c.arg:
                i+=1
                c = self.cards[i]
            return(self.cards.pop(i))
        except IndexError: 
            return None
        

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
        return " \n".join(f"{i+1}. {c}" for i,c in enumerate(self.cards))


class Game:
    """ Un jeu de LeJeu."""

    def __init__(self):
        players = ["Hadri", "Clarou"]

        """ Définition des decks """

        from deck import deck1, deck2
        self.current = Player(players[0],deck1)
        self.other = Player(players[1], deck2)
        self.discard = []

    def discard_card(self, card, player):
        self.discard.append(card)
        player.hand.cards.remove(card)

    def view_n_fist_cards_of_deck(self, n):
        print(f"Voici les {n} premières cartes de votre deck: ")
        l = []
        for k in range(n):
            l.append(self.current.deck.draw())
            print(k+1,". ", l[k], '\n')
        return(l)

    def turn(self):
         #TODO: gérer mettre un numéro à la place de j 
        self.arg_played = 0
        #Si une carte de passe-tour (sieste inopinée) a été jouée, le joueur passe son tour
        if self.current.allowed_to_play[0]:
            try:
                self.current.cards.append(self.current.deck.draw())
            except IndexError:
                pass  # deck vide
            
            print(f"C'est le tour de {self.current.name}. Voici tes cartes:")
            rep = "j"
            #Spécifique aux cartes qui empêchent de jouer plus de x cartes (Posé num 19)
            count_of_card_played = 0
            while (rep == "j" or rep == "") and len(self.current.cards)!=0 and count_of_card_played < self.current.allowed_to_play[1]:
                print(self.current.hand)
                rep = input("Veux-tu jouer une carte (j) ou passer (p)?")
                if rep == "j":
                    try :
                        numcardplay = int(input("Laquelle?"))
                        self.card_played = self.current.cards[numcardplay-1]
                        count_of_card_played +=1
                        #Si le joueur n'a pas encore joué d'argument ou que la carte n'est pas un argument
                        if(self.arg_played<1 or self.card_played.arg == False):
                            self.discard_card(self.card_played, self.current)
                            self.card_played.play(self)
                        else:
                            print("Vous avez joué trop d'arguments")
                    except ValueError as e:
                        print("Grand fou met un numéro")
                    except IndexError as e:
                        print("Un numéro que tu as plutôt coco")

                print(f"Vous avez {len(self.current.ingame_arg)} argument(s)")
        else:
            self.current.allowed_to_play[0] = True
        self.current.allowed_to_play[1] = NB_OF_CARD_IN_DECK 
        self.current, self.other = self.other, self.current
        



class Player:

    def __init__(self, name:str, deck):
        self.name = name
        self.deck = deck
        self.hand = Hand(deck)
        #Spécifiques à la carte Sieste inopinée (passe le prochain tour de l'aversaire) num 17
        self.allowed_to_play = [True, NB_OF_CARD_IN_DECK]
        #Spécifique à la carte roi de la bouffe (num 14) et princesse des coeurs (num 16) 
        # le 0 initialise le nombre de cartes *3e argument*(ex: BOUFFE) jouées 
        # Le deuxième argument a pour but de stocker la carte quand elle arrivera
        # Le troisième argument réfère au type de carte qui l'active
        self.roi_de_la_bouffe = [0, None, BOUFFE]
        self.princesse_des_coeurs = [0, None, AMOUR]
        #Utile pour les cartes qui demande de discard un argument
        self.ingame_arg = []

    @property 
    def cards(self):
        return(self.hand.cards)    

    def __str__(self):
        return " \n".join([str(i+1)+". "+str(c) for i,c in enumerate(self.ingame_arg)])
    




if __name__ == "__main__":
    pass
        

        
 







