from gui import GUI
from objectquad import objectQuad
import OpenGL.GL as gl
from glutils import *
import glfw

class Engine:
    window = None
    gui = None
    quad = None
    runtime = 0.0
    cam_angle_x = 0.0
    cam_angle_y = 0.0
    cam_dist = 2.0
    cam_flag = False

    def __init__(self, window):
        self.window = window
        self.gui = GUI()
        self.quad = objectQuad()
        self.runtime = 0.0
        self.gui.initTexture(0, "data/mmp_gurov.png")
        self.gui.bindTexture(0)

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
        dx = x - self.gui.window_width / 2
        dy = y - self.gui.window_height / 2
        self.cam_angle_x -= dx * 0.01
        self.cam_angle_y += dy * 0.01
        if self.cam_angle_y > 1.5:
            self.cam_angle_y = 1.5
        if self.cam_angle_y < -1.5:
            self.cam_angle_y = -1.5
        while self.cam_angle_x > 2 * pi:
            self.cam_angle_x -= 2 * pi
        while self.cam_angle_x < - 2 * pi:
            self.cam_angle_x +=  2 * pi
        glfw.set_cursor_pos(self.window, self.gui.window_width / 2, self.gui.window_height / 2)

    def step(self, elapsedTime):
        self.runtime += elapsedTime
        gl.glClearColor(0.25 * (1 - cos(0.5 * self.runtime)), 0.5 * (1 + sin(1 * self.runtime)),
            0.5 * (1 + cos(0.33 * self.runtime)), 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT | gl.GL_STENCIL_BUFFER_BIT)
        gl.glViewport(0, 0, self.gui.window_width, self.gui.window_height)
        self.gui.projectionMatrix = self.gui.perspective()
        if self.cam_flag:
            self.__process_camera()
        self.gui.eye = self.cam_dist * array([sin(self.cam_angle_x) * cos(self.cam_angle_y),
            sin(self.cam_angle_y), cos(self.cam_angle_x) * cos(self.cam_angle_y)], 'f')
        self.gui.cen = array([0, 0, 0], 'f')
        self.gui.up  = array([0, 1, 0], 'f')
        self.gui.viewMatrix = self.gui.lookAt()
        self.gui.modelMatrix = mul(mul(translate(array([0, 0, 0.5 * sin(2 * self.runtime)], 'f')),
            rotate(self.runtime * 100, array([0, 1, 0], 'f'))), scale(array([0.5, 0.5, 0.5], 'f')))
        self.gui.sendMatrices()
        self.gui.setColor(array([1, 1, 0, 1], 'f'))
        self.quad.draw()
        self.gui.modelMatrix = mul(translate(array([0, 0, -0.5 * sin(2 * self.runtime)], 'f')),
            rotate(-self.runtime * 200, array([0, 1, 0], 'f')))
        self.gui.sendMatrices()
        self.gui.setColor(array([0, 1, 1, 1], 'f'))
        self.quad.draw()
        for i in range(8):
            self.gui.modelMatrix = mul(rotate(-self.runtime * 50 + 360.0 * i / 8, array([0, 1, 0], 'f')),
                translate(array([0, 0, 2 + sin(self.runtime)], 'f')))
            self.gui.sendMatrices()
            self.gui.setColor(array([0.25, 1 - 0.5 * (1 + sin(self.runtime)), 0.5 * (1 + sin(self.runtime)), 1], 'f'))
            self.quad.draw()
