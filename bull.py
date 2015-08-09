class Bull:
    def __init__(self, start, target, power):
        self.start = start
        self.target = target
        self.position = start
        self.power = power

    def getStart(self):
        return self.start

    def getTarget(self):
        return self.target

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    def getPower(self):
        return self.power
