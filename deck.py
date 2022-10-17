"""Définition des decks"""

from enum import Enum, unique
from types import NoneType
from LeJeu import *
from time import sleep
from random import *

""" Définition des fonctions des cartes """


def decorate_play(function):
    """Cette fonction génère le décorateur:"""

    def wrapper(game):
        """Le décorateur qui introduit la carte jouée"""
        print(f"Vous jouez la carte {game.card_played}")
        result = function(game)
        return result

    return wrapper


def decorate_type(function):
    """Cette fonction génère le décorateur:"""

    def wrapper(game):
        """décorateur: si la carte spe est en jeu, l'itère de 1
        dans la limite de 3 (se transforme en argument)"""
        # Si la carte spe a été jouée -> On augmente le compteur de 1
        # Aide card_spe: le [0] : nombre de cartes *3e argument*(ex: BOUFFE) jouées
        # le [1]: dit si lal carte a été jouée
        # Le [2] réfère au type de carte qui l'active
        CARD_SPE = [game.current.princesse_des_coeurs, game.current.roi_de_la_bouffe]
        for card_spe in CARD_SPE:
            if card_spe[1] is not None and card_spe[2] in game.card_played.type:
                card_spe[0] += 1
                # Si 3 cartes du bon type ont été jouées, la carte est un argument en jeu, on ajoute 1 au nombre d'arguments joués.
                print(card_spe[0])
                if card_spe[0] == 3:
                    game.current.ingame_arg.append(card_spe[1])
        result = function(game)
        return result

    return wrapper


@decorate_play
def play1(game):
    """Pirouette: Vous pouvez jouer deux arguments de plus pendant ce tour"""
    game.current.arg_played -= 2


@decorate_play
def play2(game):
    """Faux Travail: Vous choisissez une carte dans la main de votre adversaire, elle retourne dans son deck"""
    print("Voici les cartes de votre adversaire: \n")
    print(game.other.hand)
    cardnum = int(input("Quelle carte choisissez vous ?"))
    game.other.deck.append(game.other.cards.pop(cardnum - 1))
    game.other.deck.shuffle()


@decorate_play
@decorate_type
def play3(game):
    """Salade: Ne sert à rien"""
    sleep(1)
    print("\n ...\n")
    sleep(1)
    print("il ne se passe rien")


@decorate_play
def play4(game):
    """Kiffeur: Vous choisissez une carte dans la main de votre adversaire"""
    NB_OF_CARD_CHOSEN = 1
    cards = game.choose_in_deck(NB_OF_CARD_CHOSEN, game.other.hand)
    cards_deck_to_deck(cards, game.current.hand, game.other.hand)


@decorate_play
def play5(game):
    """Pinte de Spritz: L'adversaire se défausse d'un argument"""
    game.other.discard_argument()


@decorate_play
@decorate_type
def play6(game):
    """Un argument"""
    game.current.arg_played += 1
    game.current.ingame_arg.append(game.card_played)


@decorate_play
def play8(game):
    """Pari stupide: Un argument pour l'autre camp mais qui fait piocher 3 cartes"""
    game.other.ingame_arg.append(game.card_played)
    for k in range(3):
        try:
            game.current.cards.append(game.current.deck.draw())
        except IndexError:
            pass  # deck vide


@decorate_play
def play9(game):
    """Si le joueur courant n'a pas d'argument en main, en joue un depuis son deck"""
    l_hand = [c.arg for c in game.current.cards]
    if not True in l_hand:
        card = game.current.deck.draw_type(isarg=1)
        if card is not None:
            card.play(game)
    else:
        print("Vous avez un argument en main, cette carte n'a pas d'effet")


@decorate_play
def play10(game):
    """Pioche deux actions du deck"""
    for i in range(2):
        card_drawn = game.current.deck.draw_type(isarg=0)
        if card_drawn is not None:
            game.current.cards.append(card_drawn)


@decorate_play
def play11(game):
    """Remplace toutes ses cartes par des cartes du deck"""
    nbcards = len(game.current.cards)
    newHand = Hand(game.current.deck, nbcards)
    game.current.deck.cards = game.current.deck.cards + game.current.cards
    game.current.hand = newHand
    game.current.deck.shuffle()


@decorate_play
def play12(game):
    """Bien équipé: Réorganise les trois premières cartes de votre deck"""
    NB_OF_CARDS = 3
    game.reorganise_n_deck(NB_OF_CARDS, game.current)


@decorate_play
def play13(game):
    """Baillement: Vous défaussez une carte. votre adversaire en défausse deux"""
    game.current.nb_of_card_to_discard = 1
    game.other.nb_of_card_to_discard = 2
    for player in [game.current, game.other]:
        for k in range(player.nb_of_card_to_discard):
            print(f"Voici les cartes de {player.name}: ")
            sleep(1)
            print(player.hand)
            card_chosen = player.cards[
                int(input("Quelle carte voulez vous défausser? ")) - 1
            ]
            game.discard_card(card_chosen, player)


# TODO: gérer si jouée deux fois
@decorate_play
def play14(game):
    """Roi de la Bouffe: Cette action reste en jeu. Jouez 3 cartes BOUFFE pour la transformer en argument."""
    game.current.roi_de_la_bouffe[1] = game.card_played


@decorate_type
@decorate_play
def play16(game):
    """Princesse des coeurs: Cette action reste en jeu. Jouez 3 cartes BOUFFE pour la transformer en argument."""
    game.current.princesse_des_coeurs[1] = game.card_played


@decorate_play
def play17(game):
    """Sieste inopinée: l'adversaire passe son prochain tour"""
    game.other.allowed_to_play[0] = False


@decorate_play
def play18(game):
    """Rire mignon: L'adversaire se défausse d'une carte aléatoire"""
    # Choisit une carte alétoire du deck de l'adversaire
    card = choice(game.other.cards)
    game.discard_card(card, game.other)


@decorate_play
def play19(game):
    """Posé: Votre adversaire ne peut pas jouer plus de deux cartes au prochain tour."""
    game.other.allowed_to_play[1] = 2


@decorate_play
def play21(game):
    """Courageuse?: Vous échangez une carte de votre main avec une carte au choix parmi les trois premières de votre deck"""
    l = game.view_n_fist_cards_of_deck(3, game.current)
    indice = int(input("Quelle carte voulez vous prendre?"))
    game.current.cards.append(l[indice - 1])
    print(game.current.hand)
    indice = int(input("Contre quelle carte?"))
    card_removed = game.current.cards.pop(indice - 1)
    game.current.deck.cards.append(card_removed)


@decorate_type
@decorate_play
def play22(game):
    """Kebab: Place une carte salade dans le deck de chaque joueur"""
    game.current.deck.cards.append(card3)
    game.other.deck.cards.append(card3)


@decorate_play
def play23(game):
    """Pipi, les dents et au lit: Votre adversaire ne peut jouer qu'une carte au prochain tour"""
    game.other.allowed_to_play[1] = 1


@decorate_type
@decorate_play
def play24(game):
    """Double date: Vous choisissez deux cartes neutres restantes"""
    NB_OF_CARD_CHOSEN = 2
    # Le joueur choisit deux cartes NEUTRE dans le deck restant
    cards = game.choose_in_deck(NB_OF_CARD_CHOSEN, game.rest, color=NEUTRE)
    # On met les cartes choisies dans la main du joueur
    cards_deck_to_deck(cards, game.current.hand, game.rest)


@decorate_play
def play25(game):
    """Jeu de rôle: Au début du prochain tour adverse, vous piochez à sa place (dans son deck)"""
    game.other.draw_instead = True


@decorate_type
@decorate_play
def play26(game):
    # TODO: changer la boucle pas très jolie
    """Bisous: Chaque joueur donne une carte à l'autre. Si l'un des deux joueurs n'a pas de cartes
    l'autre lui en donne une quand même"""
    for player in [game.current, game.other]:
        if len(player.cards > 0):
            print(f"Voici les cartes de {player.name}: ")
            sleep(1)
            print(player.hand)
            card_chosen = player.cards[
                int(input("Quelle carte voulez vous donner? ")) - 1
            ]
            player.cards.remove(card_chosen)
            # Va chercher l'autre joueur
            for player2 in [game.current, game.other]:
                if player2 != player:
                    # Lui ajoute la carte choisie dans sa main
                    player2.cards.append(card_chosen)


@decorate_type
@decorate_play
def play27(game):
    """Carrot Cake: Vous choisissez une carte bouffe de votre deck"""
    NB_OF_CARD_CHOSEN = 1
    # Le joueur choisit une cartes BOUFFE dans son deck
    cards = game.choose_in_deck(NB_OF_CARD_CHOSEN, game.current.deck, type=BOUFFE)
    # On met les cartes choisies dans la main du joueur
    cards_deck_to_deck(cards, game.current.hand, game.current.deck)


@decorate_play
def play28(game):
    """Grosse dalle: Vous choisissez deux cartes Bouffe restantes"""
    NB_OF_CARD_CHOSEN = 2
    # Le joueur choisit deux cartes BOUFFE dans le deck restant
    cards = game.choose_in_deck(NB_OF_CARD_CHOSEN, game.rest, type=BOUFFE)
    # On met les cartes choisies dans la main du joueur
    # si choose_in_deck -> None
    try:
        cards_deck_to_deck(cards, game.current.hand, game.rest)
    except TypeError:
        pass


@decorate_play
def play29(game):
    """Surprise: Vous prenez une carte aléatoire dans la main de votre adversaire"""
    try:
        card = choice(game.other.cards)
        game.current.cards.append(card)
    except IndexError or TypeError:
        print("L'adversaire n'a plus de carte")


@decorate_play
def play30(game):
    """Kiffeuse: Vous choisissez une carte parmi les trois premières du deck adverse"""
    # TODO: fix bug
    NB_OF_CARD_CHOSEN = 1
    # Le joueur choisit une carte dans
    deck_to_choose = Deck(game.other.deck.cards[0:3])
    cards = game.choose_in_deck(NB_OF_CARD_CHOSEN, deck_to_choose)
    # On met les cartes choisies dans la main du joueur
    cards_deck_to_deck(cards, game.current.hand, game.other.deck)


@decorate_play
def play31(game):
    """Matin difficile: Au début de son prochain tour le joueur adverse ne pioche pas."""
    game.other.allowed_to_play[2] = False


@decorate_play
def play33(game):
    """10h du mat on est déjà à fond: Vous piochez des cartes Picole: jusqu'à avoir autant de cartes que votre adversaire"""
    for k in range(len(game.other.cards)):
        card = game.current.deck.draw_type(istype=PICOLE)
        if card is not None:
            game.current.cards.append(card)
        else:
            break


@decorate_play
def play34(game):
    """Petite bière: Vous choisissez une carte Picole de votre deck"""
    NB_OF_CARDS = 1
    cards = game.choose_in_deck(NB_OF_CARDS, game.current.deck, type=PICOLE)
    cards_deck_to_deck(cards, game.current.hand, game.current.deck)


@decorate_play
def play35(game):
    """J'ai tous les droits: Vous choisissez une carte de la défausse"""
    NB_OF_CARDS = 1
    cards = game.choose_in_deck(NB_OF_CARDS, game.discard, type=PICOLE)
    cards_deck_to_deck(cards, game.current.hand, game.discard)


@decorate_play
def play37(game):
    """Surchargé: Vous piochez deux cartes"""
    NB_OF_CARDS = 2
    for k in range(NB_OF_CARDS):
        card = game.current.deck.draw()
        game.current.hand.cards.append(card)


@decorate_play
def play38(game):
    """Buée: Vous réorganisez les 3 premières cartes du deck adverse"""
    NB_OF_CARDS = 3
    game.reorganise_n_deck(NB_OF_CARDS, game.other)


@decorate_play
def play39(game):
    """Armure: L'adversaire ne peut pas jouer d'argument au prochain tour"""
    # Le nombre max d'argument joué par tour étant de 1,
    # Sachant qu'il existe une carte permettant d'en jouer deux de plus
    # et que la carte est codée de telle sorte à ce que arg_played -= 2
    # On le pose = 3>1 pour éviter les soucis liés à la carte
    game.other.arg_played = 3


@decorate_play
def play40(game):
    """Before arrosé: Tous les joueurs perdent 2 arguments"""
    NB_OF_ARGUMENTS = 2
    for k in range(NB_OF_ARGUMENTS):
        game.current.discard_argument()
        game.other.discard_argument()


@decorate_play
def play41(game):
    """Peinture de guerre: Vous piochez deux cartes Picole"""
    NB_OF_CARDS = 2
    for k in range(NB_OF_CARDS):
        card = game.current.deck.draw_type(istype=PICOLE)
        if card is not None:
            game.current.cards.append(card)


@decorate_play
def play42(game):
    """Vomi tactique: L'adversaire défausse une carte Bouffe. Vous piochez une carte Picole"""
    # L'adversaire se défausse d'une carte Bouffe
    game.discard_type(BOUFFE, game.other)

    # Tire une carte Picole
    card = game.current.deck.draw_type(istype=PICOLE)
    if card is not None:
        game.current.cards.append(card)


@decorate_play
@decorate_type
def play43(game):
    """Gala: l'adversaire défausse une carte Beauf, vous piochez une carte Amour"""
    # L'adversaire se défausse d'une carte BEAUF
    game.discard_type(BEAUF, game.other)

    # Tire une carte AMOUR
    card = game.current.deck.draw_type(istype=AMOUR)
    if card is not None:
        game.current.cards.append(card)


@decorate_play
def play44(game):
    """Coup de fil: Vous ne pouvez jouer que cette carte pendant ce tour.
    Vous piochez trois cartes"""
    NB_OF_CARDS = 3
    # On vérifie qu'aucune autre carte n'a été jouée avant
    if game.count_of_card_played < 1:
        for k in range(NB_OF_CARDS):
            try:
                game.current.cards.append(game.current.deck.draw())
            except IndexError:
                pass  # deck vide
        game.rep = "p"
    else:
        print("Vous avez essayé de tricher ce n'est pas très joli")


@decorate_play
def play46(game):
    """Réfléchissant: Vous rejouez la dernière carte adverse"""
    if game.other.last_played != None:
        game.other.last_played.play(game)
    else:
        print("Votre adversaire n'a pas joué de carte")


@decorate_play
def play47(game):
    # TODO: gérer s'il y en a plusieurs
    """Déconcentration: Retournez un argument adverse, il est invalide pendant deux tours"""
    game.other.deconcentration = game.nb_of_turn
    game.other.hide_argument()


@decorate_play
def play48(game):
    """(interrupt) Impatience: Si votre adversaire a déjà joué 2 cartes pendant son tour vous pouvez y mettre fin"""
    game.rep = "p"


@decorate_play
def play49(game):
    # TODO: Gérer s'il y en a plusieurs
    """Drôle de copie: cette carte est toujours une copie de la dernière carte que vous avez jouée"""
    if game.count_of_card_played >= 1:
        game.current.last_played.play(game)
    else:
        try:
            game.other.last_played.play(game)
        except AttributeError:
            print("Aucune carte n'a été jouée")


@decorate_play
def play50(game):
    """De la suite dans les idées: Vous piochez un argument"""
    card = game.current.deck.draw_type(isarg=1)
    if card is not None:
        game.current.cards.append(card)


@decorate_play
def play51(game):
    """L'adversaire ne peut pas jouer de cartes Beauf au prochain tour"""
    game.other.type_of_cards_not_allowed.append(BEAUF)


def cards_deck_to_deck(cards, deck_recieve, deck_send):
    """Passe une liste de carte du deck_send au deck_recieve:
    prend en argument la liste le deck1 et le deck2"""
    try:
        for card in cards:
            deck_recieve.cards.append(card)
            deck_send.cards.remove(card)
    except TypeError:
        pass


""" Création des cartes """

card1 = Card(
    HADRI,
    play1,
    "Pirouette: Vous pouvez jouer deux arguments de plus pendant ce tour",
    0,
)
card2 = Card(
    NEUTRE,
    play2,
    "Faux Travail: Vous choisissez une carte dans la main de votre adversaire, elle retourne dans son deck",
    0,
)
card3 = Card(NEUTRE, play3, "Salade: Ne sert à rien", 0, type=[BOUFFE])
card4 = Card(
    HADRI,
    play4,
    "Kiffeur: Vous choisissez une carte dans la main de votre adversaire",
    0,
)
card5 = Card(
    NEUTRE, play5, "Pinte de Spritz: L'adversaire se défausse d'un argument", 0
)
card6 = Card(HADRI, play6, "(Argument) Jam: Je dois aider pour installer en plus", 1)
card7 = Card(
    HADRI,
    play6,
    "(Argument) Style incontestable: Une fois cet argument joué il ne peut être défaussé",
    1,
    discardable=False,
)
card8 = Card(
    HADRI,
    play8,
    "Pari stupide: cet argument est pour votre adversaire. Vous piochez 3 cartes",
    0,
)
card9 = Card(
    HADRI,
    play9,
    "Gros Canon: Si vous n'avez pas d'argument en main, en joue un depuis votre deck",
    0,
)
card10 = Card(HADRI, play10, "Jeune investisseur: Vous piochez deux actions", 0)
card11 = Card(
    HADRI,
    play11,
    "Courageux: Echangez toutes vos cartes avec des cartes de votre deck",
    0,
)
card12 = Card(
    HADRI,
    play12,
    "Bien équipé: Vous réorganisez les trois premières cartes de votre deck",
    0,
)
card13 = Card(
    NEUTRE,
    play13,
    "Baillement: Vous défausser une carte. Votre adversaire en défausse deux",
    0,
)
card14 = Card(
    HADRI,
    play14,
    "Roi de la Bouffe: Cette action reste en jeu. Jouez 3 cartes Bouffe pour la transformer en Argument",
    0,
    type=[BOUFFE],
)
card15 = Card(
    CLAROU,
    play6,
    "(Argument) Style incontestable: Une fois cet argument joué il ne peut être défaussé",
    1,
    type=[BEAUF],
    discardable=False,
)
card16 = Card(
    CLAROU,
    play16,
    "Princesse des coeurs: Cette action reste en jeu. Jouez 3 cartes Amour pour la transformeren Argument.",
    0,
    type=[AMOUR],
)
card17 = Card(
    CLAROU, play17, "Sieste inopinée: L'adversaire passe son prochain tour", 0
)
card18 = Card(
    CLAROU, play18, "Rire mignon: l'adversaire se défausse d'une carte aléatoire", 0
)
card19 = Card(
    HADRI,
    play19,
    "Posé: Votre adversaire ne peut pas jouer plus de deux cartes au prochain tour",
    0,
    type=[BEAUF],
)
card20 = Card(
    CLAROU, play6, "(Argument) Journée de la femme: J'y peux rien c'est aujourd'hui", 1
)
card21 = Card(
    CLAROU,
    play21,
    "Courageuse?: Vous échangez une carte de votre main avec une carte au choix parmi les trois premières de votre deck",
    0,
)
card22 = Card(
    NEUTRE,
    play22,
    "Kebab: Place une carte salade dans le deck de chaque joueur",
    0,
    type=[BEAUF, BOUFFE],
)
card23 = Card(
    HADRI,
    play23,
    "Pipi, les dents et au lit: Votre adversaire ne peut jouer qu'une carte au prochain tour",
    0,
)
card24 = Card(
    NEUTRE,
    play24,
    "Double date: Vous choisissez deux cartes neutres restantes",
    0,
    type=[AMOUR],
)
card25 = Card(
    NEUTRE,
    play25,
    "Jeu de rôle: Au début du prochain tour adverse, vous piochez à sa place (dans son deck)",
    0,
)
card26 = Card(
    NEUTRE, play26, "Bisous: Chaque joueur donne une carte à l'autre", 0, type=[AMOUR]
)
card27 = Card(
    NEUTRE,
    play27,
    "Carrot Cake: Vous choisissez une carte bouffe de votre deck",
    0,
    type=[BOUFFE],
)
card28 = Card(
    NEUTRE, play28, "Grosse dalle: Vous choisissez deux cartes Bouffe restantes", 0
)
card29 = Card(
    NEUTRE,
    play29,
    "Surprise: Vous prenez une carte aléatoire dans la main de votre adversaire.",
    0,
)
card30 = Card(
    CLAROU,
    play30,
    "Kiffeuse: Vous choisissez une carte parmi les trois premières du deck adverse",
    0,
    type=[BEAUF],
)
card31 = Card(
    NEUTRE,
    play31,
    "Matin difficile: Au début de son prochain tour le joueur adverse ne pioche pas.",
    0,
    type=[PICOLE],
)
card32 = Card(
    NEUTRE, play5, "Black-out:L'adversaire perd son dernier argument", 0, type=[PICOLE]
)
card33 = Card(
    NEUTRE,
    play33,
    "10h du mat on est déjà à fond: Vous piochez des cartes Picole: jusqu'à avoir autant de cartes que votre adversaire",
    0,
    type=[PICOLE, BEAUF],
)
card34 = Card(
    NEUTRE,
    play34,
    "Petite bière: Vous choisissez une carte Picole de votre deck",
    0,
    type=[PICOLE],
)
card35 = Card(
    CLAROU, play35, "J'ai tous les droits: Vous choisissez une carte de la défausse.", 0
)
card36 = Card(
    NEUTRE, play6, "Lessive: En plus je suis descendu deux fois pour le sèche-linge", 1
)
card37 = Card(NEUTRE, play37, "Surchargé: Vous piochez deux cartes", 0)
card38 = Card(
    CLAROU, play38, "Buée: Vous réorganisez les 3 premières cartes du deck adverse", 0
)
card39 = Card(
    CLAROU,
    play39,
    "Armure: L'adversaire ne peut pas jouer d'argument au prochain tour",
    0,
)
card40 = Card(
    NEUTRE,
    play40,
    "Before arrose: Tous les joueurs perdent 2 arguments",
    0,
    type=[PICOLE],
)
card41 = Card(
    CLAROU,
    play41,
    "Peinture de guerre: Vous piochez deux cartes Picole",
    0,
    type=[BEAUF],
)
card42 = Card(
    NEUTRE,
    play42,
    "Vomi tactique: L'adversaire défausse une carte Bouffe. Vous piochez une carte Picole",
    0,
    type=[PICOLE],
)
card43 = Card(
    NEUTRE,
    play43,
    "Gala: L'adversaire défausse une carte Beauf, vous piochez une carte Amour",
    0,
    type=[AMOUR],
)
card44 = Card(
    NEUTRE,
    play44,
    "Coup de fil: Vous ne pouvez jouer que cette carte pendant ce tour. Vous piochez trois cartes",
    0,
    type=[AMOUR],
)
card45 = Card(
    HADRI,
    play6,
    "(Argument)Bon petit plat: J'ai cuisiné un truc super bon en plus",
    1,
    type=[BOUFFE],
)
card46 = Card(
    HADRI,
    play46,
    "Réfléchissant: Vous rejouez la dernière carte adverse.",
    0,
    type=[BEAUF],
)
card47 = Card(
    HADRI,
    play47,
    "Déconcentration: Retournez un argument adverse il est invalide pendant 2 tours",
    0,
)
card48 = Card(
    HADRI,
    play48,
    "(interrupt) Impatience: Si votre adversaire a déjà joué 2 cartes pendant son tour vous pouvez y mettre fin",
    0,
)
card49 = Card(
    NEUTRE,
    play49,
    "Drôle de copie: cette carte est toujouros une copie de la dernière carte que vous avez jouée",
    0,
)
card50 = Card(NEUTRE, play50, "De la suite dans les idées: Vous piochez un argument", 0)
card51 = Card(
    NEUTRE,
    play51,
    "Massage: L'adversaire ne peut pas jouer de cartes Beauf au prochain tour",
    0,
    type=[AMOUR],
)
l1 = [
    card51,
    card51,
    card51,
    card51,
    card51,
    card6,
    card7,
    card8,
    card9,
    card10,
    card40,
    card45,
    card45,
]

l2 = [
    card15,
    card15,
    card15,
    card15,
    card15,
    card15,
    card15,
    card15,
    card3,
    card3,
    card14,
]
rest = [card2, card2, card5, card5, card5, card13, card7, card8, card9, card10, card22]


"""Création des deux decks de départ"""

deck1 = Deck(l1)
deck2 = Deck(l2)
rest = Deck(rest)

deck1.shuffle()
deck2.shuffle()
