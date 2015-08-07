from numpy import *
from item import *
from random import *
from player import Player


class Game:
    free_items = set()
    player_main = Player()
    enemies = set()
    bulls = set()

    def __init__(self):
        for i in range(10):
            r = randint(0, 2)
            clr = COLOR_RED
            if r == 1:
                clr = COLOR_BLUE
            if r == 2:
                clr = COLOR_GREEN
            rx = random() * 100 - 50
            ry = random() * 100 - 50
            rz = random() * 100 - 50
            self.free_items.add(Item(array([rx, ry, rz], 'f'), clr))
        for i in range(10):
            p = Player()
            rx = random() * 100 - 50
            ry = random() * 100 - 50
            rz = random() * 100 - 50
            p.setPosition(array([rx, ry, rz], 'f'))
            self.enemies.add(p)

    def getFreeItems(self):
        return self.free_items

    def getMainPlayer(self):
        return self.player_main

    def getEnemies(self):
        return self.enemies

    def getBulls(self):
        return self.bulls
