"""
The game class

it uses pygame to display the game
"""


import pygame
from useful_functions import create_hand


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.size = self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Basic Pygame program")

        # Fill background
        self.background = pygame.image.load("img\\background.png")

        # Blit everything to the screen
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        # test / will be in run for update
        cards = [
            {
                "color": "blue",
                "picture": "img\sheep.jpg",
                "description": ["Super:", "une super carte"],
            },
            {
                "color": "pink",
                "picture": "img\sheep.jpg",
                "description": ["Super:", "une super carte"],
            },
            {
                "color": "gray",
                "picture": "img\sheep.jpg",
                "description": ["Super:", "une super carte"],
            },
        ]
        self.hand = create_hand(cards, 500, 600)
        self.opponent = create_hand(cards, 700, 20, hidden=True)

    def run(self) -> None:
        # Event loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            # update display
            self.screen.blit(self.background, (0, 0))
            self.hand.draw(self.screen)
            self.opponent.draw(self.screen)
            pygame.display.update()
            pygame.display.flip()


if __name__ == "__main__":
    g = Game()
    g.run()
