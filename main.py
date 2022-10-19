from LeJeu import *
from deck import cards_deck_to_deck

game = Game()

############################################# PHASE DE DECKBUILDING ############################################

print("############# C'est au tour de Hadri de choisir ses cartes ###############")
cards_chosen = game.choose_in_deck(10, game.rest, color=HADRI)
cards_deck_to_deck(cards_chosen, game.current.deck, game.rest)
print(game.rest)
print("############# C'est au tour de Clarou de choisir ses cartes ###############")
cards_chosen = game.choose_in_deck(10, game.rest, color=CLAROU)
cards_deck_to_deck(cards_chosen, game.other.deck, game.rest)

print("############# On passe aux cartes Neutres alternativement ###############\n")
for k in range(10):

    print("############# C'est au tour de Hadri de choisir sa carte ###############")
    card_chosen = game.choose_in_deck(1, game.rest, color=NEUTRE)
    cards_deck_to_deck(card_chosen, game.current.deck, game.rest)

    print("############# C'est au tour de Clarou de choisir sa carte ###############")
    card_chosen = game.choose_in_deck(1, game.rest, color=NEUTRE)
    cards_deck_to_deck(card_chosen, game.other.deck, game.rest)

################################################## PHASE DE JEU ##################################################
for card in game.rest.cards:
    card.position = game.rest.cards

game.nb_of_turn = 0
game.current.deck.shuffle()
game.other.deck.shuffle()
game.current.hand = Hand(game.current.deck)
game.other.hand = Hand(game.other.deck)

while (
    # Tant qu'un des deux joueurs n'a pas gagné (joué 5 arguments)
    len(game.current.ingame_arg) < 5
    and len(game.other.ingame_arg) < 5
    # Tant qu'il reste des cartes
    and len(game.current.deck.cards) > 0
    and len(game.other.deck.cards) > 0
):
    game.nb_of_turn += 1
    game.turn()

################################################ ANNONCE VICTOIRE #################################################

if len(game.current.ingame_arg) < len(game.other.ingame_arg):
    print(f"BRAVO: {game.current.name} a gagné !")
else:
    print(f"BRAVO: {game.other.name} a gagné !")
