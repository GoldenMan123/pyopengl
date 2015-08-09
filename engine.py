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


class Engine:
    window = None
    game = None
    gui = None
    quad = None
    cube = None
    target = None
    target_display_pos = None
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
        self.gui.renderText(16, "data/mono.ttf", 256, "+", (255, 255, 255, 255))

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
        if self.cam_flag:
            self.shoot = True
        else:
            if self.game.getSP():
                x, y = glfw.get_cursor_pos(self.window)
                x = float(x) / self.gui.getWindowWidth() * 2.0 * self.gui.aspect - self.gui.aspect
                y = 1.0 - float(y) / self.gui.getWindowHeight() * 2.0
                if x > - self.gui.aspect + 0.6 and x < - self.gui.aspect + 0.7 and y > 0.8 and y < 0.9:
                    self.game.getMainPlayer().addPower(1)
                    self.game.decSP()
                if x > - self.gui.aspect + 0.6 and x < - self.gui.aspect + 0.7 and y > 0.65 and y < 0.75:
                    self.game.getMainPlayer().addDefence(1)
                    self.game.decSP()
                if x > - self.gui.aspect + 0.6 and x < - self.gui.aspect + 0.7 and y > 0.5 and y < 0.6:
                    self.game.getMainPlayer().addSpeed(1)
                    self.game.decSP()

    def shoot_off(self):
        self.shoot = False

    def __process_camera(self):
        x, y = glfw.get_cursor_pos(self.window)
        dx = x - self.gui.window_width / 2.0
        dy = y - self.gui.window_height / 2.0
        cam_dir = v4_v3(mul_v(rotate(-dy * 0.5, cross(self.cam_dir, self.cam_up)), v3_v4(self.cam_dir)))
        cam_up  = v4_v3(mul_v(rotate(-dy * 0.5, cross(self.cam_dir, self.cam_up)), v3_v4(self.cam_up)))
        cam_dir = v4_v3(mul_v(rotate(-dx * 0.5, cam_up), v3_v4(cam_dir)))
        self.cam_dir = normalize(cam_dir)
        self.cam_up  = normalize(cam_up)
        glfw.set_cursor_pos(self.window, self.gui.window_width / 2, self.gui.window_height / 2)

    def __init_3d(self):
        # Clear screen
        gl.glClearColor(0.05, 0.05, 0.1, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT | gl.GL_STENCIL_BUFFER_BIT)
        gl.glViewport(0, 0, self.gui.window_width, self.gui.window_height)
        gl.glEnable(gl.GL_DEPTH_TEST)
        # Calculate view and projection matrices
        self.gui.projectionMatrix = self.gui.perspective()
        self.gui.eye = self.game.getMainPlayer().getPosition()
        self.gui.cen = self.gui.eye + self.cam_dir
        self.gui.up  = self.cam_up
        self.gui.viewMatrix = self.gui.lookAt()

    def __draw_enemies(self):
        self.gui.bindTexture(-1)
        self.gui.enableLighting()
        for i in self.game.getEnemies():
            self.gui.modelMatrix = translate(i.getPosition())
            self.gui.sendMatrices()
            if i == self.target:
                self.gui.setColor(array([1, 0, 0, 1], 'f'))
                self.target_display_pos = v4_v3(mul_v(self.gui.projectionMatrix,
                    mul_v(self.gui.viewMatrix, v3_v4(i.getPosition()))))
            else:
                self.gui.setColor(array([0, 1, 0, 1], 'f'))
            self.cube.draw()
        self.gui.disableLighting()

    def __draw_items(self):
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

    def __draw_bulls(self):
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

    def __init_2d(self):
        gl.glDisable(gl.GL_DEPTH_TEST)
        self.gui.projectionMatrix = identity(4, 'f')
        self.gui.viewMatrix = scale(array([1.0 / self.gui.aspect, 1, 1], 'f'))

    def __draw_target_stats(self):
        str_str = str(self.target.getPower())
        def_str = str(self.target.getDefence())
        spd_str = str(self.target.getSpeed())
        self.gui.modelMatrix = mul(translate(array([self.target_display_pos[0] * self.gui.aspect - 0.125
            - (len(str_str) + len(def_str) + len(spd_str)) * 0.025,
            self.target_display_pos[1] + 0.15, 0], 'f')),
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

    def __draw_target_health(self):
        self.gui.bindTexture(-1)
        self.gui.modelMatrix = mul(translate(array([self.target_display_pos[0] * self.gui.aspect,
            self.target_display_pos[1] + 0.2, 0], 'f')),
            scale(array([0.4, 0.025, 1], 'f')))
        self.gui.sendMatrices()
        self.gui.setColor(array([0, 0, 0.25, 1], 'f'))
        self.quad.draw()
        self.gui.modelMatrix = mul(translate(array([self.target_display_pos[0] * self.gui.aspect + 0.2 *
            (self.target.getHealth() - 1.0), self.target_display_pos[1] + 0.2, 0], 'f')),
            scale(array([0.4 * self.target.getHealth(), 0.025, 1], 'f')))
        self.gui.sendMatrices()
        self.gui.setColor(array([0, 0, 1.0, 1], 'f'))
        self.quad.draw()

    def __draw_aim(self):
        self.gui.bindTexture(1)
        self.gui.modelMatrix = scale(array([0.2, 0.2, 0.2], 'f'))
        self.gui.sendMatrices()
        if self.target:
            self.gui.setColor(array([1, 0, 0, 1], 'f'))
        else:
            self.gui.setColor(array([1, 1, 1, 1], 'f'))
        self.quad.draw()
        if self.target:
            self.gui.modelMatrix = mul(translate(array([self.target_display_pos[0] * self.gui.aspect,
                self.target_display_pos[1], 0], 'f')),
                scale(array([0.2, 0.2, 0.2], 'f')))
            self.gui.sendMatrices()
            self.quad.draw()

    def __draw_item_icons(self):
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

    def __draw_item_count(self):
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

    def __draw_player_stats(self):
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
        if self.game.getSP():
            self.gui.modelMatrix = mul(translate(array([- self.gui.aspect + 0.65, 0.85, 0], 'f')),
                scale(array([0.1, 0.2, 0.2], 'f')))
            self.gui.sendMatrices()
            self.gui.bindTexture(16)
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
        if self.game.getSP():
            self.gui.modelMatrix = mul(translate(array([- self.gui.aspect + 0.65, 0.7, 0], 'f')),
                scale(array([0.1, 0.2, 0.2], 'f')))
            self.gui.sendMatrices()
            self.gui.bindTexture(16)
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

    def __draw_update_buttons(self):
        self.gui.modelMatrix = mul(translate(array([- self.gui.aspect + 0.65, 0.55, 0], 'f')),
            scale(array([0.1, 0.2, 0.2], 'f')))
        self.gui.sendMatrices()
        self.gui.bindTexture(16)
        self.quad.draw()

    def __draw_player_health(self):
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

    def step(self, elapsedTime):
        self.runtime += elapsedTime
        # Process logic
        self.game.move(elapsedTime, self.cam_dir)
        self.game.process(elapsedTime)
        if self.cam_flag:
            self.__process_camera()
        # Define target
        self.target = None
        for i in self.game.getEnemies():
            dst = dist(i.getPosition(), self.game.getMainPlayer().getPosition())
            if dst > 10000:
                continue
            ang = dot(self.cam_dir, normalize(i.getPosition() - self.game.getMainPlayer().getPosition()))
            if ang < 0.99:
                continue
            if not self.target:
                self.target = i
                ang_old = ang
            else:
                if ang > ang_old:
                    self.target = i
                    ang_old = ang
        # Process shooting
        if self.shoot and self.target:
            self.game.shoot(self.target, self.cam_up)
        # Redraw
        self.__init_3d()
        self.__draw_enemies()
        self.__draw_items()
        self.__draw_bulls()
        self.__init_2d()
        if self.target:
            self.__draw_target_stats()
            self.__draw_target_health()
        self.__draw_aim()
        self.__draw_item_icons()
        self.__draw_item_count()
        self.__draw_player_stats()
        if self.game.getSP():
            self.__draw_update_buttons()
        self.__draw_player_health()
