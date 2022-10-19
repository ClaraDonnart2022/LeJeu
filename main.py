from LeJeu import *
from deck import cards_rest
import pandas as pd

game = Game()
game.choose_in_deck(1, game.rest, color=NEUTRE)
print(game.rest)
game.choose_in_deck(1, game.rest, color=NEUTRE)
# for card in game.current.deck.cards:
#    card.position = game.current.deck.cards
# for card in game.other.deck.cards:
#    card.position = game.other.deck.cards
# for card in game.rest.cards:
#    card.position = game.rest.cards


############################################# Phase de deckbuiliding ############################################
#
# print("############# C'est au tour de Hadri de choisir ses cartes ###############")
# cards_chosen = game.choose_in_deck(10, game.rest, color=HADRI)
# for card in cards_chosen:
#    game.current.deck.cards.append(card)
#
# print("############# C'est au tour de Clarou de choisir ses cartes ###############")
# cards_chosen = game.choose_in_deck(10, game.rest, color=CLAROU)
# for card in cards_chosen:
#    game.other.deck.cards.append(card)

# print("############# On passe aux cartes Neutres alternativement ###############\n")
# for k in range(3):
#   print("############# C'est au tour de Hadri de choisir sa carte ###############")
#   card_chosen = game.choose_in_deck(1, game.rest, color=NEUTRE)
#   game.current.deck.cards.append(card_chosen[0])
#   print("############# C'est au tour de Clarou de choisir sa carte ###############")
#   card_chosen = game.choose_in_deck(1, game.rest, color=NEUTRE)
#   game.other.deck.cards.append(card_chosen[0])
################################################## Phase de jeu ##################################################
# game.nb_of_turn = 0
# game.current.hand = Hand(game.current.deck)
# game.other.hand = Hand(game.other.deck)
# while True:
#    game.nb_of_turn += 1
#    game.turn()
#
