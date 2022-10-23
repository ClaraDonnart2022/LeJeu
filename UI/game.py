"""
The game class

it uses pygame to display the game

A host server should run on the machine for this script to work properly
To do this open an other terminal and run "py host.py"
"""

# global import
import pygame
import socket
import json

# local import
import config
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

        # add socket to discuss with server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((config.HOST, config.PORT))

        # retrieve data from server
        self.socket.sendall(b"data please")
        data = dict(json.loads(self.socket.recv(1024)))
        cards = data["cards"]

        # update dispay objects
        self.hand = create_hand(cards, 500, 600)
        self.opponent = create_hand(cards, 700, 20, hidden=True)

    def run(self) -> None:
        # Event loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.socket.sendall(b"close connection")
                    return

            # retrieve data from server
            # FIXME, we should only do this when needed
            # ie. when action is trigered from whatever side
            self.socket.sendall(b"data please")
            data = dict(json.loads(self.socket.recv(1024)))
            cards = data["cards"]

            # update dispay objects
            self.hand = create_hand(cards, 500, 600)
            self.opponent = create_hand(cards, 700, 20, hidden=True)

            # update display
            self.screen.blit(self.background, (0, 0))
            self.hand.draw(self.screen)
            self.opponent.draw(self.screen)
            pygame.display.update()
            pygame.display.flip()


if __name__ == "__main__":
    g = Game()
    g.run()
