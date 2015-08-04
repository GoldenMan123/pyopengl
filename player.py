from numpy import *


class Player:
    position = array([0, 0, 0], 'f')
    red_items = 0
    blue_items = 0
    green_items = 0
    power = 1
    defence = 1
    speed = 1

    def __init__(self):
        pass

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    def getRedItems(self):
        return self.red_items

    def setRedItems(self, red_items):
        self.red_items = red_items

    def addRedItems(self, red_items):
        self.red_items += red_items

    def getBlueItems(self):
        return self.blue_items

    def setBlueItems(self, blue_items):
        self.blue_items = blue_items

    def addBlueItems(self, blue_items):
        self.blue_items += blue_items

    def getGreenItems(self):
        return self.green_items

    def setGreenItems(self, green_items):
        self.green_items = green_items

    def addGreenItems(self, green_items):
        self.green_items += green_items

    def getPower(self):
        return self.power

    def setPower(self, power):
        self.power = power

    def addPower(self, power):
        self.power += power

    def getDefence(self):
        return self.defence

    def setDefence(self, defence):
        self.defence = defence

    def addDefence(self, defence):
        self.defence += defence

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed

    def addSpeed(self, speed):
        self.speed += speed