import sys
sys.path.insert(0, '.')
from game import *

class EngineGag:
    '''
    Gag for game defeat
    '''
    def __init__(self):
        self.flag = False

    def defeat(self):
        self.flag = True

    def getFlag(self):
        return self.flag

    def setFlag(self, flag):
        self.flag = flag


class TestLogic:
    '''
    Class TestLogic contains tests for game logic
    '''
    def test_health_recovering(self):
        game = Game(EngineGag())
        game.getMainPlayer().setHealth(0.5)
        assert game.getMainPlayer().getHealth() == 0.5
        game._Game__process_health(5.0)
        assert game.getMainPlayer().getHealth() > 0.6
        assert game.getMainPlayer().getHealth() <= 1.0
        old = len(game.getEnemies())
        for i in range(10):
            game.getEnemies().add(Player(1, 1, 1))
        assert len(game.getEnemies()) == old + 10
        for i in game.getEnemies():
            i.setHealth(0.5)
            assert i.getHealth() == 0.5
        game._Game__process_health(5.0)
        for i in game.getEnemies():
            assert i.getHealth() > 0.6
            assert i.getHealth() <= 1.0

    def test_bulls_processing(self):
        game = Game(EngineGag())
        game.getMainPlayer().setPosition(array([0, 0, 1], 'f'))
        assert game.getMainPlayer().getPosition()[0] == 0
        assert game.getMainPlayer().getPosition()[1] == 0
        assert game.getMainPlayer().getPosition()[2] == 1
        game.getMainPlayer().setHealth(1.0)
        assert game.getMainPlayer().getHealth() == 1.0
        game.getMainPlayer().setBlueItems(0)
        assert game.getMainPlayer().getBlueItems() == 0
        game.getMainPlayer().setDefence(1)
        assert game.getMainPlayer().getDefence() == 1
        b = Bull(array([0, 0, 0], 'f'), game.getMainPlayer(), 1)
        old = len(game.getBulls())
        game.getBulls().add(b)
        assert len(game.getBulls()) == old + 1
        game._Game__process_bulls(0.001)
        assert b.getPosition()[2] > 0.01
        game._Game__process_bulls(1)
        assert len(game.getBulls()) == old
        assert game.getMainPlayer().getHealth() < 0.9

    def test_pickup(self):
        game = Game(EngineGag())
        game.getMainPlayer().setPosition(array([0, 0, 0], 'f'))
        assert game.getMainPlayer().getPosition()[0] == 0
        assert game.getMainPlayer().getPosition()[1] == 0
        assert game.getMainPlayer().getPosition()[2] == 0
        i = Item(array([0, 0, 10], 'f'), COLOR_RED, 23)
        assert i.getColor() == COLOR_RED
        assert i.getCount() == 23
        assert i.getPosition()[0] == 0
        assert i.getPosition()[1] == 0
        assert i.getPosition()[2] == 10
        game.getFreeItems().clear()
        game.getFreeItems().add(i)
        assert len(game.getFreeItems()) == 1
        assert i in game.getFreeItems()
        old = game.getMainPlayer().getRedItems()
        game._Game__process_pickup()
        assert old == game.getMainPlayer().getRedItems()
        game.getMainPlayer().setPosition(array([0, 0, 10], 'f'))
        assert game.getMainPlayer().getPosition()[0] == 0
        assert game.getMainPlayer().getPosition()[1] == 0
        assert game.getMainPlayer().getPosition()[2] == 10
        game._Game__process_pickup()
        assert old + 23 == game.getMainPlayer().getRedItems()

    def test_item_lifetime(self):
        game = Game(EngineGag())
        i = Item(array([0, 0, 0], 'f'), COLOR_BLUE, 1)
        assert i.getColor() == COLOR_BLUE
        assert i.getCount() == 1
        assert i.getPosition()[0] == 0
        assert i.getPosition()[1] == 0
        assert i.getPosition()[2] == 0
        old = len(game.getFreeItems())
        game.getFreeItems().add(i)
        assert old + 1 == len(game.getFreeItems())
        assert i in game.getFreeItems()
        i.setLifetime(1.0)
        assert i.getLifetime() == 1.0
        game._Game__process_item_lifetime(1)
        assert abs(i.getLifetime() - 1.0) < 10.0 ** -5
        i.setCount(0)
        assert i.getCount() == 0
        game._Game__process_item_lifetime(0.1)
        assert i.getLifetime() < 0.99
        assert i in game.getFreeItems()
        game._Game__process_item_lifetime(100)
        assert i.getLifetime() <= 0
        assert i not in game.getFreeItems()

    def test_item_spawn(self):
        game = Game(EngineGag())
        game.getMainPlayer().setPosition(array([0, 0, 0], 'f'))
        assert game.getMainPlayer().getPosition()[0] == 0
        assert game.getMainPlayer().getPosition()[1] == 0
        assert game.getMainPlayer().getPosition()[2] == 0
        game.getFreeItems().clear()
        assert len(game.getFreeItems()) == 0
        game._Game__process_item_spawn()
        assert len(game.getFreeItems()) > 0
        old = []
        for i in game.getFreeItems():
            old.append(i)
        game.getMainPlayer().setPosition(array([10 ** 5, 0, 0], 'f'))
        assert game.getMainPlayer().getPosition()[0] == 10 ** 5
        assert game.getMainPlayer().getPosition()[1] == 0
        assert game.getMainPlayer().getPosition()[2] == 0
        game._Game__process_item_spawn()
        assert len(game.getFreeItems()) > 0
        for i in old:
            assert i not in game.getFreeItems()

    def test_reload(self):
        game = Game(EngineGag())
        game.getMainPlayer().setReload(0)
        assert game.getMainPlayer().getReload() == 0
        game._Game__process_reload(0)
        assert game.getMainPlayer().getReload() == 0
        game._Game__process_reload(1)
        assert game.getMainPlayer().getReload() > 0.1
        old = len(game.getEnemies())
        e = Player(1, 1, 1)
        e.setReload(0)
        assert e.getReload() == 0
        game.getEnemies().add(e)
        assert e in game.getEnemies()
        assert len(game.getEnemies()) == old + 1
        game._Game__process_reload(0)
        assert e.getReload() == 0
        game._Game__process_reload(1)
        assert e.getReload() > 0.1
        assert e in game.getEnemies()

    def test_ai(self):
        game = Game(EngineGag())
        game.getEnemies().clear()
        game.getBulls().clear()
        game.getMainPlayer().setPosition(array([0, 0, 0], 'f'))
        assert game.getMainPlayer().getPosition()[0] == 0
        assert game.getMainPlayer().getPosition()[1] == 0
        assert game.getMainPlayer().getPosition()[2] == 0
        game.getMainPlayer().setDefence(1)
        assert game.getMainPlayer().getDefence() == 1
        e = Player(10, 10, 10)
        e.setPosition(array([10 ** 5, 0, 0], 'f'))
        assert e.getPosition()[0] == 10 ** 5
        assert e.getPosition()[1] == 0
        assert e.getPosition()[2] == 0
        game.getEnemies().add(e)
        assert len(game.getBulls()) == 0
        assert len(game.getEnemies()) == 1
        game._Game__process_ai(117.0)
        assert len(game.getBulls()) == 0
        assert len(game.getEnemies()) == 1
        assert e.getPosition()[0] < 10 ** 5 - 100
        e.setPosition(array([0, 0, 10], 'f'))
        assert e.getPosition()[0] == 0
        assert e.getPosition()[1] == 0
        assert e.getPosition()[2] == 10
        e.setReload(0)
        game._Game__process_ai(0.1)
        assert len(game.getEnemies()) == 1
        assert e.getPosition()[0] == 0
        assert e.getPosition()[1] == 0
        assert e.getPosition()[2] == 10
        assert len(game.getBulls()) == 0
        e.setReload(1.0)
        game._Game__process_ai(0.1)
        assert len(game.getEnemies()) == 1
        assert e.getPosition()[0] == 0
        assert e.getPosition()[1] == 0
        assert e.getPosition()[2] == 10
        assert len(game.getBulls()) == 1
        assert e.getReload() == 0
        for i in game.getBulls():
            assert i.getTarget() == game.getMainPlayer()
            assert i.getPosition()[0] == 0
            assert i.getPosition()[1] == 0
            assert i.getPosition()[2] == 10

    def test_move(self):
        game = Game(EngineGag())
        game.getMainPlayer().setPosition(array([0, 0, 0], 'f'))
        assert game.getMainPlayer().getPosition()[0] == 0
        assert game.getMainPlayer().getPosition()[1] == 0
        assert game.getMainPlayer().getPosition()[2] == 0
        game.move(0, array([1, 1, 1], 'f'))
        assert game.getMainPlayer().getPosition()[0] == 0
        assert game.getMainPlayer().getPosition()[1] == 0
        assert game.getMainPlayer().getPosition()[2] == 0
        game.move(1.0, array([0, 0, 1], 'f'))
        assert game.getMainPlayer().getPosition()[0] == 0
        assert game.getMainPlayer().getPosition()[1] == 0
        assert game.getMainPlayer().getPosition()[2] != 0
        game.getMainPlayer().setPosition(array([0, 0, 0], 'f'))
        game.move(1.0, array([0, 1, 0], 'f'))
        assert game.getMainPlayer().getPosition()[0] == 0
        assert game.getMainPlayer().getPosition()[1] != 0
        assert game.getMainPlayer().getPosition()[2] == 0
        game.getMainPlayer().setPosition(array([0, 0, 0], 'f'))
        game.move(1.0, array([1, 0, 0], 'f'))
        assert game.getMainPlayer().getPosition()[0] != 0
        assert game.getMainPlayer().getPosition()[1] == 0
        assert game.getMainPlayer().getPosition()[2] == 0

    def test_shoot(self):
        game = Game(EngineGag())
        e = Player(1, 1, 1)
        game.getEnemies().clear()
        game.getEnemies().add(e)
        assert len(game.getEnemies()) == 1
        game.getMainPlayer().setPosition(array([1, 2, 3], 'f'))
        game.getBulls().clear()
        game.getMainPlayer().setReload(1.0)
        game.shoot(e, array([0, 0, 0], 'f'))
        assert len(game.getBulls()) == 1
        assert game.getMainPlayer().getReload() == 0.0
        game.shoot(e, array([0, 0, 0], 'f'))
        assert len(game.getBulls()) == 1
        for i in game.getBulls():
            assert i.getPosition()[0] == 1
            assert i.getPosition()[1] == 2
            assert i.getPosition()[2] == 3
            for j in game.getEnemies():
                assert i.getTarget() == j
                assert e == j