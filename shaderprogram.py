import OpenGL.GL as gl
from shader import Shader

POSITION_LOCATION = 0
NORMAL_LOCATION = 1
TEXTURE_LOCATION = 2

TEXTURE_SAMPLER_LOCATION = 29
TEXTURE_FLAG_LOCATION = 30

MODEL_MATRIX_LOCATION = 13
VIEW_MATRIX_LOCATION = 17
NORMAL_MATRIX_LOCATION = 21
PROJECTION_MATRIX_LOCATION = 25

COLOR_LOCATION = 31
LIGHTING_FLAG_LOCATION = 32


class ShaderProgram:
    vertexShader = None
    fragmentShader = None
    programObject = None

    def __init__(self):
        pass

    def init(self, vertexShaderName, fragmentShaderName):
        self.vertexShader = Shader()
        self.vertexShader.readAndCompile(vertexShaderName, gl.GL_VERTEX_SHADER)
        self.fragmentShader = Shader()
        self.fragmentShader.readAndCompile(fragmentShaderName, gl.GL_FRAGMENT_SHADER)
        self.programObject = gl.glCreateProgram()
        gl.glAttachShader(self.programObject, self.vertexShader.getShaderObject())
        gl.glAttachShader(self.programObject, self.fragmentShader.getShaderObject())
        gl.glBindFragDataLocation(self.programObject, gl.GL_NONE, "fragColor")
        gl.glLinkProgram(self.programObject)

    def getProgramObject(self):
        return self.programObject
