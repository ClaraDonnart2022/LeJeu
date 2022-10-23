"""
A set of usefull fonctions
"""

import pygame
import json
from card import Card
from hand import Hand


class DisplayError(Exception):
    pass


my_colors = {
    "pink": pygame.Color("lightpink"),
    "blue": pygame.Color("lightskyblue"),
    "gray": pygame.Color("lightgray"),
}


def create_hand(cards, xoffset, yoffset, hidden=False):
    """
    :param: - cards a list of cards containing color, path to picture and description
            - xoffset xpostion to start
            - y position to start
            - hidden a boolean for showing the back of the card

    :return: a hand object containing the list of cards dictionary
    """
    res = []
    n = len(cards)
    if n > 10:
        raise DisplayError("Hand is to long")
        # FIXME: Here we should change the display instead
    else:
        startx = xoffset - 105 / 2 * n

    for k, card in enumerate(cards):
        res += [
            Card(
                startx + k * 105,
                yoffset,
                my_colors[card["color"]],
                card["picture"],
                card["description"],
                hidden,
            )
        ]
    return Hand(res)
