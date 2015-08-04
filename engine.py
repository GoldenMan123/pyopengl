# -*- coding: utf-8 -*-
from game import Game
from gui import GUI
from objectquad import objectQuad
from item import *
import OpenGL.GL as gl
from glutils import *
import glfw


def dist(x, y):
    r = 0.0
    for i in range(3):
        r += (x[i] - y[i]) ** 2
    return r


def comparer(pos):
    def _cmp(x, y):
        xr = dist(x.getPosition(), pos)
        yr = dist(y.getPosition(), pos)
        if xr < yr:
            return 1
        if xr > yr:
            return -1
        return 0
    return _cmp


class Engine:
    window = None
    game = None
    gui = None
    quad = None
    runtime = 0.0
    cam_angle_x = 0.0
    cam_angle_y = 0.0
    cam_dist = 2.0
    cam_flag = False

    def __init__(self, window):
        self.window = window
        self.game = Game()
        self.gui = GUI()
        self.quad = objectQuad()
        self.runtime = 0.0
        self.gui.initTexture(0, "data/item.png")
        self.gui.initTexture(1, "data/aim.png")
        for i in range(10):
            self.gui.renderText(2 + i, "data/mono.ttf", 256, str(i), (255, 255, 255, 255))

    def setWindowHeight(self, h):
        self.gui.setWindowHeight(h)
        if self.cam_flag:
            glfw.set_cursor_pos(self.window, self.gui.window_width / 2, self.gui.window_height / 2)

    def setWindowWidth(self, w):
        self.gui.setWindowWidth(w)
        if self.cam_flag:
            glfw.set_cursor_pos(self.window, self.gui.window_width / 2, self.gui.window_height / 2)

    def camera_on(self):
        self.cam_flag = True
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
        glfw.set_cursor_pos(self.window, self.gui.window_width / 2, self.gui.window_height / 2)

    def camera_off(self):
        self.cam_flag = False
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)

    def camera_scroll(self, d):
        self.cam_dist *= (1.25 ** -d)
        if self.cam_dist < 1:
            self.cam_dist = 1
        if self.cam_dist > 10:
            self.cam_dist = 10

    def __process_camera(self):
        x, y = glfw.get_cursor_pos(self.window)
        dx = x - self.gui.window_width / 2.0
        dy = y - self.gui.window_height / 2.0
        self.cam_angle_x -= dx * 0.01
        self.cam_angle_y -= dy * 0.01
        if self.cam_angle_y > 1.5:
            self.cam_angle_y = 1.5
        if self.cam_angle_y < -1.5:
            self.cam_angle_y = -1.5
        while self.cam_angle_x > 2 * pi:
            self.cam_angle_x -= 2 * pi
        while self.cam_angle_x < - 2 * pi:
            self.cam_angle_x +=  2 * pi
        glfw.set_cursor_pos(self.window, self.gui.window_width / 2, self.gui.window_height / 2)

    def __process_game(self, elapsedTime):
        # Move player
        mp = self.game.getMainPlayer()
        dir = array([sin(self.cam_angle_x) * cos(self.cam_angle_y),
            sin(self.cam_angle_y), cos(self.cam_angle_x) * cos(self.cam_angle_y)], 'f')
        mp.setPosition(mp.getPosition() + dir * elapsedTime * 10)
        # Process item pickup
        fi = self.game.getFreeItems()
        for i in fi:
            if dist(i.getPosition(), mp.getPosition()) < 10.0:
                if i.getColor() == COLOR_RED:
                    mp.addRedItems(i.getCount())
                if i.getColor() == COLOR_BLUE:
                    mp.addBlueItems(i.getCount())
                if i.getColor() == COLOR_GREEN:
                    mp.addGreenItems(i.getCount())
                i.setCount(0)
        # Process item lifetime
        td = []
        for i in fi:
            if i.getCount() == 0:
                i.setLifetime(i.getLifetime() - 5.0 * elapsedTime)
            if i.getLifetime() <= 0:
                td.append(i)
        for i in td:
            fi.remove(i)

    def step(self, elapsedTime):
        self.runtime += elapsedTime
        # Process logic
        self.__process_game(elapsedTime)
        if self.cam_flag:
            self.__process_camera()
        # Redraw
        gl.glClearColor(0.75, 0.75, 1.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT | gl.GL_STENCIL_BUFFER_BIT)
        gl.glViewport(0, 0, self.gui.window_width, self.gui.window_height)
        # 3D
        gl.glEnable(gl.GL_DEPTH_TEST)
        # Calculate view and projection matrices
        self.gui.projectionMatrix = self.gui.perspective()
        self.gui.eye = self.game.getMainPlayer().getPosition()
        self.gui.cen = self.gui.eye + self.cam_dist * array([sin(self.cam_angle_x) * cos(self.cam_angle_y),
            sin(self.cam_angle_y), cos(self.cam_angle_x) * cos(self.cam_angle_y)], 'f')
        self.gui.up  = array([0, 1, 0], 'f')
        self.gui.viewMatrix = self.gui.lookAt()
        self.gui.bindTexture(0)
        # Draw items
        free_items = sorted(self.game.getFreeItems(), cmp=comparer(self.gui.eye))
        for i in free_items:
            self.gui.modelMatrix = mul(translate(i.getPosition()),
                mul(rotate(self.cam_angle_x / pi * 180.0, array([0, 1, 0], 'f')),
                rotate(- self.cam_angle_y / pi * 180.0, array([1, 0, 0], 'f'))))
            self.gui.sendMatrices()
            if i.getColor() == COLOR_RED:
                self.gui.setColor(array([1, 0, 0, i.getLifetime()], 'f'))
            if i.getColor() == COLOR_BLUE:
                self.gui.setColor(array([0, 0, 1, i.getLifetime()], 'f'))
            if i.getColor() == COLOR_GREEN:
                self.gui.setColor(array([0, 1, 0, i.getLifetime()], 'f'))
            self.quad.draw()
        # 2D
        gl.glDisable(gl.GL_DEPTH_TEST)
        self.gui.bindTexture(1)
        self.gui.projectionMatrix = identity(4, 'f')
        self.gui.viewMatrix = scale(array([1.0 / self.gui.aspect, 1, 1], 'f'))
        # Draw aim
        self.gui.modelMatrix = scale(array([0.2, 0.2, 0.2], 'f'))
        self.gui.sendMatrices()
        self.gui.setColor(array([0, 0, 0, 1], 'f'))
        self.quad.draw()
        # Items icons
        self.gui.bindTexture(0)
        self.gui.modelMatrix = mul(translate(array([self.gui.aspect - 0.1, 0.85, 0], 'f')),
            scale(array([0.2, 0.2, 0.2], 'f')))
        self.gui.setColor(array([1, 0, 0, 1], 'f'))
        self.gui.sendMatrices()
        self.quad.draw()
        self.gui.bindTexture(0)
        self.gui.modelMatrix = mul(translate(array([self.gui.aspect - 0.1, 0.7, 0], 'f')),
            scale(array([0.2, 0.2, 0.2], 'f')))
        self.gui.setColor(array([0, 0, 1, 1], 'f'))
        self.gui.sendMatrices()
        self.quad.draw()
        self.gui.bindTexture(0)
        self.gui.modelMatrix = mul(translate(array([self.gui.aspect - 0.1, 0.55, 0], 'f')),
            scale(array([0.2, 0.2, 0.2], 'f')))
        self.gui.setColor(array([0, 1, 0, 1], 'f'))
        self.gui.sendMatrices()
        self.quad.draw()
        # Items count
        self.gui.modelMatrix = mul(translate(array([self.gui.aspect - 0.15, 0.85, 0], 'f')),
            scale(array([0.1, 0.2, 0.2], 'f')))
        self.gui.setColor(array([1, 0, 0, 1], 'f'))
        for i in reversed(str(self.game.getMainPlayer().getRedItems())):
            self.gui.bindTexture(int(i) + 2)
            self.gui.modelMatrix = mul(translate(array([-0.1, 0, 0], 'f')), self.gui.modelMatrix)
            self.gui.sendMatrices()
            self.quad.draw()
        self.gui.modelMatrix = mul(translate(array([self.gui.aspect - 0.15, 0.7, 0], 'f')),
            scale(array([0.1, 0.2, 0.2], 'f')))
        self.gui.setColor(array([0, 0, 1, 1], 'f'))
        for i in reversed(str(self.game.getMainPlayer().getBlueItems())):
            self.gui.bindTexture(int(i) + 2)
            self.gui.modelMatrix = mul(translate(array([-0.1, 0, 0], 'f')), self.gui.modelMatrix)
            self.gui.sendMatrices()
            self.quad.draw()
        self.gui.modelMatrix = mul(translate(array([self.gui.aspect - 0.15, 0.55, 0], 'f')),
            scale(array([0.1, 0.2, 0.2], 'f')))
        self.gui.setColor(array([0, 1, 0, 1], 'f'))
        for i in reversed(str(self.game.getMainPlayer().getGreenItems())):
            self.gui.bindTexture(int(i) + 2)
            self.gui.modelMatrix = mul(translate(array([-0.1, 0, 0], 'f')), self.gui.modelMatrix)
            self.gui.sendMatrices()
            self.quad.draw()
