from LeJeu import *
import pandas as pd

game = Game()
for card in game.current.deck.cards:
    card.position = game.current.deck.cards
for card in game.other.deck.cards:
    card.position = game.other.deck.cards
for card in game.rest.cards:
    card.position = game.rest.cards

game.nb_of_turn = 0
while True:
    game.nb_of_turn += 1
    game.turn()
