import OpenGL.GL as gl


class Shader:
    shaderType = None
    shaderObject = None

    def __init__(self):
        pass

    def getShaderType(self):
        return self.shaderType

    def getShaderObject(self):
        return self.shaderObject

    def read(self, filename, type):
        self.shaderType = type
        self.shaderObject = gl.glCreateShader(self.shaderType)
        file = open(filename, "r").read()
        gl.glShaderSource(self.shaderObject, file)

    def compile(self):
        gl.glCompileShader(self.shaderObject)

    def readAndCompile(self, filename, type):
        self.read(filename, type)
        self.compile()

    def release(self):
        if self.shaderObject:
            gl.glDeleteShader(self.shaderObject)
            self.shaderObject = None