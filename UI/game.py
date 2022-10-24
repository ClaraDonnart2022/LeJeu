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

import time as tm

# local import
import config
from useful_functions import create_hand


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.size = self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Basic Pygame program")
        self.clock = pygame.time.Clock()

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

        # useful for display
        self.mooving = []

    def run(self) -> None:
        # Event loop

        while True:
            tic = tm.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.socket.sendall(b"close connection")
                    return

                # handle MOUSEBUTTONUP
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    # to detect a card play
                    for card in self.hand.cards:
                        if card.contains(pygame.mouse.get_pos()):
                            self.hand.cards.remove(card)
                            card.set_movement()
                            self.mooving.append(card)

            # moove cards if needed
            for card in self.mooving:
                arrived = card.moove()
                if arrived:
                    self.mooving.remove(card)

            # retrieve data from server
            if False:
                self.socket.sendall(b"data please")
                data = dict(json.loads(self.socket.recv(1024)))
                cards = data["cards"]

                # update objects
                self.hand = create_hand(cards, 500, 600)
                self.opponent = create_hand(cards, 700, 20, hidden=True)

            # update display
            self.screen.blit(self.background, (0, 0))
            self.hand.draw(self.screen)
            self.opponent.draw(self.screen)
            for card in self.mooving:
                card.draw(self.screen, mul=2)
            pygame.display.update()
            pygame.display.flip()
            tac = tm.time()
            print(tac - tic)


if __name__ == "__main__":
    g = Game()
    try:
        g.run()
    except KeyboardInterrupt:
        g.socket.sendall(b"close connection")
