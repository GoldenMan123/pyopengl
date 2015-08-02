from shaderprogram import *
import OpenGL.GL as gl
from glutils import *
from texture import Texture

TEXT_COUNT = 64


class GUI:
    window_height = 480
    window_width = 640
    aspect = float(window_width) / window_height

    shaderProgram = ShaderProgram()

    eye = zeros(3, 'f')
    cen = zeros(3, 'f')
    up  = array([0, 1, 0], 'f')

    viewMatrix = identity(4, 'f')
    modelMatrix = identity(4, 'f')
    projectionMatrix = identity(4, 'f')
    normalMatrix = identity(4, 'f')

    textures = []

    def __init__(self):
        self.__initOpenGL()

    def __initOpenGL(self):
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LESS)
        gl.glClearDepth(1.0)

        gl.glDisable(gl.GL_CULL_FACE)

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        self.shaderProgram.init("Vertex.vert", "Fragment.frag")
        gl.glUseProgram(self.shaderProgram.getProgramObject())

        gl.glActiveTexture(gl.GL_TEXTURE0)
        tex_ids = gl.glGenTextures(TEXT_COUNT)
        for i in range(TEXT_COUNT):
            self.textures.append(Texture(tex_ids[i]))

        gl.glUniform1i(INST_FLAG_LOCATION, 0)
        gl.glUniform1i(TEXTURE_SAMPLER_LOCATION, 0)
        gl.glUniform1i(TEXTURE_FLAG_LOCATION, 0)

    def __recalcAspect(self):
        if self.window_height:
            self.aspect = float(self.window_width) / self.window_height

    def getWindowHeight(self):
        return self.window_height

    def setWindowHeight(self, h):
        self.window_height = h
        self.__recalcAspect()

    def getWindowWidth(self):
        return self.window_width

    def setWindowWidth(self, w):
        self.window_width = w
        self.__recalcAspect()

    def sendMatrices(self):
        self.normalMatrix = linalg.inv(transpose(dot(self.viewMatrix, self.modelMatrix)))
        gl.glUniformMatrix4fv(MODEL_MATRIX_LOCATION, 1, gl.GL_FALSE, concatenate(self.modelMatrix))
        gl.glUniformMatrix4fv(VIEW_MATRIX_LOCATION, 1, gl.GL_FALSE, concatenate(self.viewMatrix))
        gl.glUniformMatrix4fv(NORMAL_MATRIX_LOCATION, 1, gl.GL_FALSE, concatenate(self.normalMatrix))
        gl.glUniformMatrix4fv(PROJECTION_MATRIX_LOCATION, 1, gl.GL_FALSE, concatenate(self.projectionMatrix))

    def setColor(self, color):
        gl.glUniform4fv(COLOR_LOCATION, 1, color)

    def lookAt(self):
        f = normalize(self.cen - self.eye)
        u = normalize(self.up)
        s = normalize(cross(f, u))
        u = cross(s, f)
        result = identity(4, 'f')
        result[0][0] = s[0]
        result[1][0] = s[1]
        result[2][0] = s[2]
        result[0][1] = u[0]
        result[1][1] = u[1]
        result[2][1] = u[2]
        result[0][2] = -f[0]
        result[1][2] = -f[1]
        result[2][2] = -f[2]
        result[3][0] = -dot(s, self.eye)
        result[3][1] = -dot(u, self.eye)
        result[3][2] = dot(f, self.eye)
        return result

    def perspective(self):
        fieldOfView = 45.0
        zNear = 0.1
        zFar = 1000.0
        D2R = pi / 180.0
        yScale = 1.0 / tan(D2R * fieldOfView / 2.0)
        xScale = yScale / self.aspect
        nearmfar = zNear - zFar
        return array(
            [[xScale, 0, 0, 0],
            [0, yScale, 0, 0],
            [0, 0, (zFar + zNear) / nearmfar, -1],
            [0, 0, 2 * zFar * zNear / nearmfar, 0]], 'f')

    def initTexture(self, id, filename):
        self.textures[id].load(filename)

    def bindTexture(self, id):
        if id == -1 or not self.textures[id].inited:
            gl.glUniform1i(TEXTURE_FLAG_LOCATION, 0)
        else:
            gl.glUniform1i(TEXTURE_FLAG_LOCATION, 1)
            self.textures[id].bind()
