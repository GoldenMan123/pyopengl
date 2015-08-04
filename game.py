from numpy import *
from item import *
from random import *
from player import Player


class Game:
    free_items = []
    player_main = Player()

    def __init__(self):
        for i in range(100):
            r = randint(0, 2)
            clr = COLOR_RED
            if r == 1:
                clr = COLOR_BLUE
            if r == 2:
                clr = COLOR_GREEN
            rx = random() * 100 - 50
            ry = random() * 100 - 50
            rz = random() * 100 - 50
            self.free_items.append(Item(array([rx, ry, rz], 'f'), clr))

    def getFreeItems(self):
        return self.free_items

    def getMainPlayer(self):
        return self.player_main

