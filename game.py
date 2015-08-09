from item import *
from glutils import *
from random import *
from player import Player
from bull import Bull
import sys


class Game:
    free_items = set()
    player_main = Player()
    enemies = set()
    bulls = set()
    sp = 10

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

    def getSP(self):
        return self.sp

    def decSP(self):
        self.sp -= 1

    def __process_item_spawn(self):
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

    def __process_ai(self, elapsedTime):
        for i in self.enemies:
            dst = dist(self.player_main.getPosition(), i.getPosition())
            if dst > 7500:
                _dir = normalize(self.player_main.getPosition() - i.getPosition())
                i.setPosition(i.getPosition() + _dir * elapsedTime * 10)
            if dst <= 10000 and i.getReload() > 0.5:
                self.bulls.add(Bull(i.getPosition(), self.player_main, i.getPower()))
                i.setReload(0.0)

    def __process_health(self, elapsedTime):
        for i in self.enemies:
            i.setHealth(i.getHealth() + 0.05 * elapsedTime)
            if i.getHealth() > 1.0:
                i.setHealth(1.0)
        self.player_main.setHealth(self.player_main.getHealth() + 0.05 * elapsedTime)
        if self.player_main.getHealth() > 1.0:
            self.player_main.setHealth(1.0)

    def __process_bulls(self, elapsedTime):
        td = []
        for i in self.bulls:
            rem_dist = sqrt(dist(i.getPosition(), i.getTarget().getPosition()))
            bull_s = elapsedTime * 100
            if bull_s > rem_dist:
                td.append(i)
            else:
                i.setPosition(i.getPosition() + bull_s * normalize(i.getTarget().getPosition() - i.getPosition()))
        for i in td:
            target = i.getTarget()
            if target.getBlueItems():
                t_def = target.getDefence() * 2
                target.addBlueItems(-1)
            else:
                t_def = target.getDefence()
            target.setHealth(target.getHealth() - 0.2 * (2 ** (i.getPower() - t_def)))
            if target.getHealth() < 10.0 ** -5:
                if target == self.player_main:
                    sys.exit(0)
                if target in self.enemies:
                    self.enemies.remove(target)
            self.bulls.remove(i)

    def __process_pickup(self):
        for i in self.free_items:
            if dist(i.getPosition(), self.player_main.getPosition()) < 10.0:
                if i.getColor() == COLOR_RED:
                    self.player_main.addRedItems(i.getCount())
                if i.getColor() == COLOR_BLUE:
                    self.player_main.addBlueItems(i.getCount())
                if i.getColor() == COLOR_GREEN:
                    self.player_main.addGreenItems(i.getCount())
                i.setCount(0)

    def __process_item_lifetime(self, elapsedTime):
        td = []
        for i in self.free_items:
            if i.getCount() == 0:
                i.setLifetime(i.getLifetime() - 5.0 * elapsedTime)
            if i.getLifetime() <= 0:
                td.append(i)
        for i in td:
            self.free_items.remove(i)

    def __process_reload(self, elapsedTime):
        self.player_main.setReload(self.player_main.getReload() + elapsedTime)
        for i in self.enemies:
            i.setReload(i.getReload() + elapsedTime)

    def process(self, elapsedTime):
        self.__process_health(elapsedTime)
        self.__process_bulls(elapsedTime)
        self.__process_pickup()
        self.__process_item_lifetime(elapsedTime)
        self.__process_item_spawn()
        self.__process_reload(elapsedTime)
        self.__process_ai(elapsedTime)

    def move(self, elapsedTime, direction):
        self.player_main.addStamina(-elapsedTime)
        if self.player_main.getStamina() < 0:
            self.player_main.setStamina(0.0)
        if self.player_main.getStamina() < 10.0 ** -5:
            if self.player_main.getGreenItems():
                self.player_main.addStamina(1.0)
                self.player_main.addGreenItems(-1)
        if self.player_main.getStamina() > 0:
            mult = 2
        else:
            mult = 1
        self.player_main.setPosition(self.player_main.getPosition()
            + direction * elapsedTime * (1.25 ** self.player_main.getSpeed()) * mult)

    def shoot(self, target, up):
        if self.player_main.getReload() < 0.5:
            return
        if self.player_main.getRedItems():
            pwr = self.player_main.getPower() * 2
            self.player_main.addRedItems(-1)
        else:
            pwr = self.player_main.getPower()
        self.bulls.add(Bull(self.player_main.getPosition() - up,
            target, pwr))
        self.player_main.setReload(0.0)
