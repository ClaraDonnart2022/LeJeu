from LeJeu import *

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