from item import *
from glutils import *
from random import *
from player import Player
from bull import Bull


class Game:
    free_items = set()
    player_main = Player()
    enemies = set()
    bulls = set()

    def __init__(self):
        for i in range(0):
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

    def process_item_spawn(self):
        td = []
        for i in self.free_items:
            if dist(i.getPosition(), self.player_main.getPosition()) > 25000:
                td.append(i)
        for i in td:
            self.free_items.remove(i)
        while len(self.free_items) < 10:
            r = randint(0, 2)
            clr = COLOR_RED
            if r == 1:
                clr = COLOR_BLUE
            if r == 2:
                clr = COLOR_GREEN
            rx = random() * 100 - 50 + self.player_main.getPosition()[0]
            ry = random() * 100 - 50 + self.player_main.getPosition()[1]
            rz = random() * 100 - 50 + self.player_main.getPosition()[2]
            cnt = randint(0, 10) + 10
            self.free_items.add(Item(array([rx, ry, rz], 'f'), clr, cnt))

    def process_ai(self, elapsedTime):
        for i in self.enemies:
            dst = dist(self.player_main.getPosition(), i.getPosition())
            if dst > 7500:
                _dir = normalize(self.player_main.getPosition() - i.getPosition())
                i.setPosition(i.getPosition() + _dir * elapsedTime * 10)
            if dst <= 10000 and i.getReload() > 0.5:
                self.bulls.add(Bull(i.getPosition(), self.player_main, i.getPower()))
                i.setReload(0.0)
