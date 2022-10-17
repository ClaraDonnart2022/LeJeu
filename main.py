from LeJeu import *
import pandas as pd

game = Game()
game.nb_of_turn = 0
while True:
    game.nb_of_turn += 1
    game.turn()
