EVENT_WAVE_TIMER = 0
EVENT_ENEMY = 1
EVENT_DELAY = 2


class Event:
    def __init__(self, type, object):
        self.type = type
        self.object = object

    def getType(self):
        return self.type

    def getObject(self):
        return self.object
