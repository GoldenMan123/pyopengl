COLOR_RED = 0
COLOR_BLUE = 1
COLOR_GREEN = 2


class Item:
    def __init__(self, position, color, count):
        self.position = position
        self.color = color
        self.count = count
        self.lifetime = 1.0

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color

    def getCount(self):
        return self.count

    def setCount(self, count):
        self.count = count

    def getLifetime(self):
        return self.lifetime

    def setLifetime(self, lifetime):
        self.lifetime = lifetime
