# -*- coding: utf-8 -*-
from game import Game
from gui import GUI
from objectquad import objectQuad
from objectcube import objectCube
from item import *
from bull import Bull
import OpenGL.GL as gl
from glutils import *
import glfw
import sys


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
    cube = None
    target = None
    shoot = False
    runtime = 0.0
    cam_dir = array([0, 0, 1], 'f')
    cam_up  = array([0, 1, 0], 'f')
    cam_flag = False

    def __init__(self, window):
        self.window = window
        self.game = Game()
        self.gui = GUI()
        self.quad = objectQuad()
        self.cube = objectCube()
        self.runtime = 0.0
        self.gui.initTexture(0, "data/item.png")
        self.gui.initTexture(1, "data/aim.png")
        for i in range(10):
            self.gui.renderText(2 + i, "data/mono.ttf", 256, str(i), (255, 255, 255, 255))
        self.gui.renderText(12, "data/mono.ttf", 256, "STR:", (255, 255, 255, 255))
        self.gui.renderText(13, "data/mono.ttf", 256, "DEF:", (255, 255, 255, 255))
        self.gui.renderText(14, "data/mono.ttf", 256, "SPD:", (255, 255, 255, 255))
        self.gui.renderText(15, "data/mono.ttf", 256, "SHIELD", (255, 255, 255, 255))

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

    def camera_switch(self):
        if self.cam_flag:
            self.camera_off()
        else:
            self.camera_on()

    def camera_scroll(self, d):
        pass

    def shoot_on(self):
        self.shoot = True

    def shoot_off(self):
        self.shoot = False

    def __process_camera(self):
        x, y = glfw.get_cursor_pos(self.window)
        dx = x - self.gui.window_width / 2.0
        dy = y - self.gui.window_height / 2.0
        cam_dir = v4_v3(mul_v(rotate(-dy, cross(self.cam_dir, self.cam_up)), v3_v4(self.cam_dir)))
        cam_up  = v4_v3(mul_v(rotate(-dy, cross(self.cam_dir, self.cam_up)), v3_v4(self.cam_up)))
        cam_dir = v4_v3(mul_v(rotate(-dx, cam_up), v3_v4(cam_dir)))
        self.cam_dir = normalize(cam_dir)
        self.cam_up  = normalize(cam_up)
        glfw.set_cursor_pos(self.window, self.gui.window_width / 2, self.gui.window_height / 2)

    def __process_game(self, elapsedTime):
        # Move player
        mp = self.game.getMainPlayer()
        self.game.getMainPlayer().addStamina(-elapsedTime)
        if self.game.getMainPlayer().getStamina() < 0:
            self.game.getMainPlayer().setStamina(0.0)
        if self.game.getMainPlayer().getStamina() < 10.0 ** -5:
            if self.game.getMainPlayer().getGreenItems():
                self.game.getMainPlayer().addStamina(1.0)
                self.game.getMainPlayer().addGreenItems(-1)
        if self.game.getMainPlayer().getStamina() > 0:
            mult = 2
        else:
            mult = 1
        mp.setPosition(mp.getPosition() + self.cam_dir * elapsedTime * (1.25 ** mp.getSpeed()) * mult)
        # Process health
        for i in self.game.getEnemies():
            i.setHealth(i.getHealth() + 0.05 * elapsedTime)
            if i.getHealth() > 1.0:
                i.setHealth(1.0)
        mp.setHealth(mp.getHealth() + 0.05 * elapsedTime)
        if mp.getHealth() > 1.0:
            mp.setHealth(1.0)
        # Process bulls
        td = []
        for i in self.game.getBulls():
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
                if target == mp:
                    sys.exit(0)
                self.game.getEnemies().remove(target)
            self.game.getBulls().remove(i)
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
        # Process item spawn
        self.game.process_item_spawn()
        # Process reload
        self.game.getMainPlayer().setReload(self.game.getMainPlayer().getReload() + elapsedTime)
        for i in self.game.getEnemies():
            i.setReload(i.getReload() + elapsedTime)
        # Process AI
        self.game.process_ai(elapsedTime)

    def step(self, elapsedTime):
        self.runtime += elapsedTime
        # Process logic
        self.__process_game(elapsedTime)
        if self.cam_flag:
            self.__process_camera()
        # Process target
        target = None
        for i in self.game.getEnemies():
            dst = dist(i.getPosition(), self.game.getMainPlayer().getPosition())
            if dst > 10000:
                continue
            ang = dot(self.cam_dir, normalize(i.getPosition() - self.game.getMainPlayer().getPosition()))
            if ang < 0.99:
                continue
            if not target:
                target = i
                ang_old = ang
            else:
                if ang > ang_old:
                    target = i
                    ang_old = ang
        self.target = target
        # Process shooting
        if self.shoot and self.target and self.game.getMainPlayer().getReload() > 0.5:
            if self.game.getMainPlayer().getRedItems():
                pwr = self.game.getMainPlayer().getPower() * 2
                self.game.getMainPlayer().addRedItems(-1)
            else:
                pwr = self.game.getMainPlayer().getPower()
            self.game.getBulls().add(Bull(self.game.getMainPlayer().getPosition() - self.cam_up,
                self.target, pwr))
            self.game.getMainPlayer().setReload(0.0)
        # Redraw
        gl.glClearColor(0.75, 0.75, 1.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT | gl.GL_STENCIL_BUFFER_BIT)
        gl.glViewport(0, 0, self.gui.window_width, self.gui.window_height)
        # 3D
        gl.glEnable(gl.GL_DEPTH_TEST)
        # Calculate view and projection matrices
        self.gui.projectionMatrix = self.gui.perspective()
        self.gui.eye = self.game.getMainPlayer().getPosition()
        self.gui.cen = self.gui.eye + self.cam_dir
        self.gui.up  = self.cam_up
        self.gui.viewMatrix = self.gui.lookAt()
        # Draw enemies
        self.gui.bindTexture(-1)
        self.gui.enableLighting()
        for i in self.game.getEnemies():
            self.gui.modelMatrix = translate(i.getPosition())
            self.gui.sendMatrices()
            if i == target:
                self.gui.setColor(array([1, 0, 0, 1], 'f'))
                target_display_pos = v4_v3(mul_v(self.gui.projectionMatrix,
                    mul_v(self.gui.viewMatrix, v3_v4(i.getPosition()))))
            else:
                self.gui.setColor(array([0, 1, 0, 1], 'f'))
            self.cube.draw()
        self.gui.disableLighting()
        # Draw items
        self.gui.bindTexture(0)
        free_items = sorted(self.game.getFreeItems(), cmp=comparer(self.gui.eye))
        for i in free_items:
            pos_dir = normalize(i.getPosition() - self.gui.eye)
            base_dir = array([0, 0, 1], 'f')
            if abs(dot(base_dir, pos_dir)) > 1 - (10.0 ** -5):
                rot_axis = array([0, 1, 0], 'f')
                if dot(base_dir, pos_dir) > 0:
                    rot_angle = 0
                else:
                    rot_angle = 180
            else:
                rot_axis = cross(pos_dir, base_dir)
                rot_angle = 180 - 180 * arccos(dot(pos_dir, base_dir)) / pi
            self.gui.modelMatrix = mul(translate(i.getPosition()),
                rotate(rot_angle, rot_axis))
            self.gui.sendMatrices()
            if i.getColor() == COLOR_RED:
                self.gui.setColor(array([1, 0, 0, i.getLifetime()], 'f'))
            if i.getColor() == COLOR_BLUE:
                self.gui.setColor(array([0, 0, 1, i.getLifetime()], 'f'))
            if i.getColor() == COLOR_GREEN:
                self.gui.setColor(array([0, 1, 0, i.getLifetime()], 'f'))
            self.quad.draw()
        # Draw bulls
        self.gui.bindTexture(0)
        for i in sorted(self.game.getBulls(), cmp=comparer(self.gui.eye)):
            pos_dir = normalize(i.getPosition() - self.gui.eye)
            base_dir = array([0, 0, 1], 'f')
            if abs(dot(base_dir, pos_dir)) > 1 - (10.0 ** -5):
                rot_axis = array([0, 1, 0], 'f')
                if dot(base_dir, pos_dir) > 0:
                    rot_angle = 0
                else:
                    rot_angle = 180
            else:
                rot_axis = cross(pos_dir, base_dir)
                rot_angle = 180 - 180 * arccos(dot(pos_dir, base_dir)) / pi
            self.gui.modelMatrix = mul(translate(i.getPosition()),
                rotate(rot_angle, rot_axis))
            self.gui.setColor(array([1, 0, 0, 1], 'f'))
            self.gui.sendMatrices()
            self.quad.draw()
        # 2D
        gl.glDisable(gl.GL_DEPTH_TEST)
        self.gui.projectionMatrix = identity(4, 'f')
        self.gui.viewMatrix = scale(array([1.0 / self.gui.aspect, 1, 1], 'f'))
        # Target stats
        if target:
            str_str = str(target.getPower())
            def_str = str(target.getDefence())
            spd_str = str(target.getSpeed())
            self.gui.modelMatrix = mul(translate(array([target_display_pos[0] * self.gui.aspect - 0.125
                - (len(str_str) + len(def_str) + len(spd_str)) * 0.025,
                target_display_pos[1] + 0.15, 0], 'f')),
                scale(array([0.05, 0.1, 0.1], 'f')))
            self.gui.setColor(array([1, 0, 0, 1], 'f'))
            for i in str_str:
                self.gui.bindTexture(int(i) + 2)
                self.gui.modelMatrix = mul(translate(array([0.05, 0, 0], 'f')), self.gui.modelMatrix)
                self.gui.sendMatrices()
                self.quad.draw()
            self.gui.setColor(array([0, 0, 1, 1], 'f'))
            self.gui.modelMatrix = mul(translate(array([0.1, 0, 0], 'f')), self.gui.modelMatrix)
            for i in def_str:
                self.gui.bindTexture(int(i) + 2)
                self.gui.modelMatrix = mul(translate(array([0.05, 0, 0], 'f')), self.gui.modelMatrix)
                self.gui.sendMatrices()
                self.quad.draw()
            self.gui.setColor(array([0, 1, 0, 1], 'f'))
            self.gui.modelMatrix = mul(translate(array([0.1, 0, 0], 'f')), self.gui.modelMatrix)
            for i in spd_str:
                self.gui.bindTexture(int(i) + 2)
                self.gui.modelMatrix = mul(translate(array([0.05, 0, 0], 'f')), self.gui.modelMatrix)
                self.gui.sendMatrices()
                self.quad.draw()
        # Target health
        if target:
            self.gui.bindTexture(-1)
            self.gui.modelMatrix = mul(translate(array([target_display_pos[0] * self.gui.aspect,
                target_display_pos[1] + 0.2, 0], 'f')),
                scale(array([0.4, 0.025, 1], 'f')))
            self.gui.sendMatrices()
            self.gui.setColor(array([0, 0, 0.25, 1], 'f'))
            self.quad.draw()
            self.gui.modelMatrix = mul(translate(array([target_display_pos[0] * self.gui.aspect + 0.2 *
                (target.getHealth() - 1.0), target_display_pos[1] + 0.2, 0], 'f')),
                scale(array([0.4 * target.getHealth(), 0.025, 1], 'f')))
            self.gui.sendMatrices()
            self.gui.setColor(array([0, 0, 1.0, 1], 'f'))
            self.quad.draw()
        # Draw aim
        self.gui.bindTexture(1)
        self.gui.modelMatrix = scale(array([0.2, 0.2, 0.2], 'f'))
        self.gui.sendMatrices()
        if target:
            self.gui.setColor(array([1, 0, 0, 1], 'f'))
        else:
            self.gui.setColor(array([0, 0, 0, 1], 'f'))
        self.quad.draw()
        if target:
            self.gui.modelMatrix = mul(translate(array([target_display_pos[0] * self.gui.aspect,
                target_display_pos[1], 0], 'f')),
                scale(array([0.2, 0.2, 0.2], 'f')))
            self.gui.sendMatrices()
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
        # Stats
        self.gui.modelMatrix = mul(translate(array([- self.gui.aspect + 0.2, 0.85, 0], 'f')),
            scale(array([0.4, 0.2, 0.2], 'f')))
        self.gui.setColor(array([1, 0, 0, 1], 'f'))
        self.gui.sendMatrices()
        self.gui.bindTexture(12)
        self.quad.draw()
        self.gui.modelMatrix = mul(translate(array([- self.gui.aspect +
                0.5 + 0.1 * len(str(self.game.getMainPlayer().getPower())), 0.85, 0], 'f')),
                scale(array([0.1, 0.2, 0.2], 'f')))
        for i in reversed(str(self.game.getMainPlayer().getPower())):
            self.gui.bindTexture(int(i) + 2)
            self.gui.modelMatrix = mul(translate(array([-0.1, 0, 0], 'f')), self.gui.modelMatrix)
            self.gui.sendMatrices()
            self.quad.draw()
        self.gui.modelMatrix = mul(translate(array([- self.gui.aspect + 0.2, 0.7, 0], 'f')),
            scale(array([0.4, 0.2, 0.2], 'f')))
        self.gui.setColor(array([0, 0, 1, 1], 'f'))
        self.gui.sendMatrices()
        self.gui.bindTexture(13)
        self.quad.draw()
        self.gui.modelMatrix = mul(translate(array([- self.gui.aspect +
                0.5 + 0.1 * len(str(self.game.getMainPlayer().getDefence())), 0.7, 0], 'f')),
                scale(array([0.1, 0.2, 0.2], 'f')))
        for i in reversed(str(self.game.getMainPlayer().getDefence())):
            self.gui.bindTexture(int(i) + 2)
            self.gui.modelMatrix = mul(translate(array([-0.1, 0, 0], 'f')), self.gui.modelMatrix)
            self.gui.sendMatrices()
            self.quad.draw()
        self.gui.modelMatrix = mul(translate(array([- self.gui.aspect + 0.2, 0.55, 0], 'f')),
            scale(array([0.4, 0.2, 0.2], 'f')))
        self.gui.setColor(array([0, 1, 0, 1], 'f'))
        self.gui.sendMatrices()
        self.gui.bindTexture(14)
        self.quad.draw()
        self.gui.modelMatrix = mul(translate(array([- self.gui.aspect +
                0.5 + 0.1 * len(str(self.game.getMainPlayer().getSpeed())), 0.55, 0], 'f')),
                scale(array([0.1, 0.2, 0.2], 'f')))
        for i in reversed(str(self.game.getMainPlayer().getSpeed())):
            self.gui.bindTexture(int(i) + 2)
            self.gui.modelMatrix = mul(translate(array([-0.1, 0, 0], 'f')), self.gui.modelMatrix)
            self.gui.sendMatrices()
            self.quad.draw()
        # Health
        self.gui.bindTexture(-1)
        self.gui.modelMatrix = mul(translate(array([0, -1 + 0.05, 0], 'f')),
            scale(array([2 * self.gui.aspect, 0.1, 1], 'f')))
        self.gui.sendMatrices()
        self.gui.setColor(array([0, 0, 0.25, 1], 'f'))
        self.quad.draw()
        self.gui.modelMatrix = mul(translate(array([self.gui.aspect *
            (self.game.getMainPlayer().getHealth() - 1.0), -1 + 0.05, 0], 'f')),
            scale(array([2 * self.gui.aspect * self.game.getMainPlayer().getHealth(), 0.1, 1], 'f')))
        self.gui.sendMatrices()
        self.gui.setColor(array([0, 0, 1.0, 1], 'f'))
        self.quad.draw()
        self.gui.bindTexture(15)
        self.gui.modelMatrix = mul(translate(array([0, -1 + 0.05, 0], 'f')),
            scale(array([0.3, 0.1, 1], 'f')))
        self.gui.sendMatrices()
        self.gui.setColor(array([1.0, 1.0, 1.0, 1], 'f'))
        self.quad.draw()
