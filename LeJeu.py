"""
1: Hadri
2: Clarou
3: Neutre
"""

from re import L
from random import shuffle
from random import choice


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

    def append(self,card):
        self.cards.append(card)

    #TODO: créer un draw_type(self,type= None) qui combine draw draw_argument et draw_action
    def draw(self):
        return(self.cards.pop(-1))

    def draw_type(self, isarg= None, istype= None):
        """isarg = 1: Pioche le premier argument du deck
        isarg = 0: Pioche la première action du deck
        Si isarg = None et istype non None:
        Pioche la prochaine carte du type
        s'il n'y en a plus retourne None"""
        #TODO: Prend la dernière carte et pas la première a priori
        
        try:
            c = self.cards[0]
            if isarg is not None and istype is None:
                A = c.arg == isarg
            elif istype is not None and isarg is None:
                A = istype in c.type
            i=0
            #tant que la carte piochée n'est pas du bon type, on itère
            while not A:
                i+=1
                c = self.cards[i]
                if isarg is not None:
                    A = c.arg == isarg
                elif istype is not None:
                    A = istype in c.type
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
        from deck import deck1, deck2, rest
        self.current = Player(players[0],deck1)
        self.other = Player(players[1], deck2)
        # Spécifique aux cartes permettants de choisir dans les cartes restantes
        self.rest = rest
        self.discard = Deck([])

    def discard_card(self, card, player):
        """Permet de défausser une carte à partir d'une main de joueur 
        prend en argument une carte et un joueur
        ne retourne rien"""
        self.discard.append(card)
        player.hand.cards.remove(card)

    def discard_type(self, istype, player):
        """Prend en argument un type de carte et un joueur et défausse
        une carte de ce type dans sa main"""
        #On vérifie si l'adversaire a une carte istype dans sa main
        l = [card for card in player.cards if istype in card.type]
        if len(l) > 0:
            #La défausse si oui
            card = l.pop()
            self.discard_card(card, player)
        else:
            print(f"L'adversaire n'a pas de carte de ce type")

    def view_n_fist_cards_of_deck(self, NB_OF_CARDS, player):
        """Permet de voir les n premières cartes du deck d'un joueur"""
        print(f"Voici les {NB_OF_CARDS} premières cartes du deck de {player}: ")
        l = []
        for k in range(NB_OF_CARDS):
            try:
                l.append(player.deck.draw())
                print(f"{k+1}. {l[k]} \n") 
            except IndexError:
                break
        return(l)
        
    def reorganise_n_deck(self, NB_OF_CARDS, player):
        """Permet de réorganiser les n premières cartes du deck d'un joueur
        prend en argument le nombre de cartes et le joueur dont le deck va être réorganisée"""

        first_cards = self.view_n_fist_cards_of_deck(NB_OF_CARDS, player)
        reorganised = []
        # Demande à l'utilisateur carte par carte laquelle il voudrait placer en premier dans le deck
        for k in range(NB_OF_CARDS):
            indice = int(input("Quelle carte voulez vous mettre en premier?"))
            card_chosen = first_cards.pop(indice-1)
            reorganised.append(card_chosen)
            #Affiche à chaque fois les cartes restantes à trier
            print(" \n".join(f"{i+1}. {c}" for i,c in enumerate(first_cards)))
        player.deck.cards = player.deck.cards + reorganised
    
    def choose_in_deck(self, NB_OF_CARDS,deck, color=None, type=None):
        """Fonction qui prend en argument le type (BOUFFE, AMOUR etc...) ou la couleur (HADRI, CLAROU, NEUTRE) 
        le deck (ou hand)
        et le nombre de cartes à prendre et permet au joueur de choisir dans les cartes restantes d'un deck
        des cartes spéciales
        Retourne les cartes choisies ou None"""
        #Crée la liste des cartes concernés dans les cartes restantes
        if color is not None and type is None:
            deck_spe = [card for card in deck.cards if card.color == color]
        elif type is not None and color is None:
            deck_spe = [card for card in deck.cards if type in card.type]
        elif type is None and color is None:
            deck_spe = deck.cards

        #test s'il reste des cartes du type ou de la couleur choisie
        if len(deck_spe) >0:
            card_chosen_list = []
            print("Voici les cartes:")
            #Permet de choisir les cartes voulues dans la liste
            while len(deck_spe)>0 and len(card_chosen_list) < NB_OF_CARDS:
                print(" \n".join(f"{i+1}. {c}" for i,c in enumerate(deck_spe)))
                try:
                    card_chosen = deck_spe.pop(int(input("Quelle carte voulez-vous?"))-1)
                    card_chosen_list.append(card_chosen)
                except ValueError:
                    pass
            return(card_chosen_list)
        else:
            print("Il n'en reste plus")
            return(None)
        
    def turn(self):
        """Gère un tour de jeu"""
        #TODO: gérer mettre un numéro à la place de j 
        #Si une carte de passe-tour (sieste inopinée) a été jouée, le joueur passe son tour
        if self.current.allowed_to_play[0]:
            try:
                #Si jeu  de rôle a été jouée (num 25) l'adversaire pioche à votre place
                #Si Matin difficile a été jouée (num 31), le joueur ne pioche pas
                if not self.current.draw_instead and self.current.allowed_to_play[2]:
                    self.current.cards.append(self.current.deck.draw())
                    self.current.allowed_to_play[2] = True
                else:
                    self.other.cards.append(self.current.deck.draw())
                    self.current.draw_instead = False
            except IndexError:
                pass  # deck vide
            
            print(f"C'est le tour de {self.current.name}. Voici tes cartes:")
            self.rep = "j"
            #Spécifique aux cartes qui empêchent de jouer plus de x cartes (Posé num 19)
            self.count_of_card_played = 0
            #Si le joueur réponnd j, qu'il lui reste des cartes et qu'il a "le droit" 
            # de jouer (vis à vis une potentielle carte limitante)
            while (self.rep == "j" or self.rep == "") and len(self.current.cards)!=0 and self.count_of_card_played < self.current.allowed_to_play[1]:
                #Affiche la main
                print(self.current.hand)
                self.rep = input("Veux-tu jouer une carte (j) ou passer (p)?")
                #Si il veut jouer une carte
                if self.rep == "j":
                    try :
                        numcardplay = int(input("Laquelle?"))
                        self.card_played = self.current.cards[numcardplay-1]
                        #Si le joueur n'a pas encore joué d'argument ou que la carte n'est pas un argument
                        if(self.current.arg_played<1 or self.card_played.arg == False):
                            #On défausse la carte et on joue son effet 
                            self.discard_card(self.card_played, self.current)
                            self.card_played.play(self)
                            self.count_of_card_played +=1
                        else:
                            #Le jeu ne permet que de jouer 1 argument par tour (sauf carte contraire)
                            print("Vous avez joué trop d'arguments")
                    except ValueError as e:
                        print("Ce n'est pas un numéro")
                    except IndexError as e:
                        print("Un numéro que tu as plutôt")

                print(f"Vous avez {len(self.current.ingame_arg)} argument(s)")
        else:
            self.current.allowed_to_play[0] = True
        self.current.arg_played = 0
        self.current.allowed_to_play[1] = NB_OF_CARD_IN_DECK 
        self.current, self.other = self.other, self.current
        
        



class Player:

    def __init__(self, name:str, deck):
        self.name = name
        self.deck = deck
        self.hand = Hand(deck)
        #Spécifique à Jeu de rôle (num 25): pioche à la place de l'autre à son prochain tour
        self.draw_instead = False
        #1er arg: Spécifiques à la carte Sieste inopinée (passe le prochain tour de l'aversaire) num 17
        #Et aux cartes qui impose de ne pas jouer plus de x cartes (ex: Posé num 19)
        #3eme arg: "allowed_to_draw" spécifique à la carte matin difficile (num 31)
        self.allowed_to_play = [True, NB_OF_CARD_IN_DECK, True]
        #Spécifique à la carte roi de la bouffe (num 14) et princesse des coeurs (num 16) 
        # le 0 initialise le nombre de cartes *3e argument*(ex: BOUFFE) jouées 
        # Le deuxième argument a pour but de stocker la carte quand elle arrivera
        # Le troisième argument réfère au type de carte qui l'active
        self.roi_de_la_bouffe = [0, None, BOUFFE]
        self.princesse_des_coeurs = [0, None, AMOUR]
        #Utile pour les cartes qui demande de discard un argument
        self.ingame_arg = []
        # Utile pour Armure  (num 39) de le mettre comme un élément de Player
        self.arg_played = 0

    @property 
    def cards(self):
        return(self.hand.cards)    

    def discard_argument(self):
        """Défausse un argument d'un joueur s'il en a des défaussables"""
        l = [c for c in self.ingame_arg if c.discardable]
        L = Deck(l)

        #Si l'adversaire a pas d'argument
        if len(self.ingame_arg)<=0:
            print("Il n'y a plus d'argument à défausser votre action est inutile")

        #Si l'adversaire a des arguments défaussables
        elif len(self.ingame_arg)>0 and len(l)!=0:
            print(f"Un argument est défaussé chez {self.name}")
            card = choice(L.cards)
            self.ingame_arg.remove(card)

    def __str__(self):
        return " \n".join([str(i+1)+". "+str(c) for i,c in enumerate(self.ingame_arg)])
    




if __name__ == "__main__":

    pass
        

        
 







