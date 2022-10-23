"""
The Card class
"""

import pygame

# local import


class Card:
    width, height = 100, 175

    def __init__(self, x, y, color, picture, description, hidden):
        self.x = x
        self.y = y
        self.color = color
        self.picture = pygame.image.load(picture)
        self.descriprion = description
        self.hidden = hidden

    def draw(self, screen, mul=1):
        """
        if mul is set to 1 card appears noramly
        if mul is > 1 card is shown in more details
        """

        # set up
        topx = self.x - (mul - 1) * self.width / 2
        topy = self.y - (mul - 1) * self.height / 1.5
        width = mul * self.width
        height = mul * self.height

        card_rect = (
            topx,
            topy,
            width,
            height,
        )

        picture_rect = (
            topx + mul * 10,
            topy + mul * 15,
            mul * 80,
            mul * 80,
        )

        if not self.hidden:
            # draw card background
            pygame.draw.rect(
                screen,
                self.color,
                card_rect,
                0,
            )

            # add picture
            picture = pygame.transform.scale(self.picture, (mul * 80, mul * 80))
            screen.blit(picture, picture_rect)

            # add description
            for k, line in enumerate(self.descriprion):
                draw_text(
                    screen,
                    line,
                    int(8 * mul),
                    topx + 10 * mul,
                    topy + (105 + 7 * k) * mul,
                )

        else:
            picture = pygame.transform.scale(
                pygame.image.load("img/card_back.jpg"), (width, height)
            )
            screen.blit(picture, card_rect)

    def contains(self, pos):
        """
        :param: pos a position
        :return: bool : if position in card

        It is used to detect the mouse and highlight the card if needed
        """
        posx, posy = pos
        if (
            posx > self.x
            and posx < self.x + self.width
            and posy > self.y
            and posy < self.y + self.height
        ):
            return True
        else:
            return False


def draw_text(screen, text, size, x, y):
    """
    Draw some text on the screen
    :params: screen, text, size of text and position of text
    """
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", size)
    render = font.render(text, 1, (0, 0, 0))
    screen.blit(render, (x, y))
    pygame.font.quit()
