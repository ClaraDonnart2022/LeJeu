"""
The Hand class

Contains a list of Card elements
"""

import pygame


class Hand:
    def __init__(self, cards) -> None:
        self.cards = cards

    def draw(self, screen):
        """
        Draw the hand on screen
        """
        highlited = None
        for card in self.cards:
            if card.contains(pygame.mouse.get_pos()):
                highlited = card
            else:
                card.draw(screen)

        # make card appear bigger when mouse comes over
        try:
            highlited.draw(screen, mul=2.5)
        except AttributeError:
            pass
