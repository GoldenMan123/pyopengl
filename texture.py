import png
import OpenGL.GL as gl
from numpy import *


class Texture:
    def __init__(self, texture_id):
        self.inited = False
        self.texture_id = 0
        self.width = 0
        self.height = 0
        self.texture_id = texture_id

    def load(self, filename):
        self.width, self.height, r, t = png.Reader(filename=filename).asRGBA8()
        arr = []
        for i in r:
            for j in i:
                arr.append(j)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height, 0,
            gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, (gl.GLubyte * len(arr))(*arr))
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR_MIPMAP_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        # aniso = gl.glGetFloatv(gl.GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT)
        # gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAX_ANISOTROPY_EXT, aniso)
        self.inited = True

    def load_raw(self, width, height, data):
        self.width, self.height = width, height
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height, 0,
            gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, (gl.GLubyte * len(data))(*data))
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR_MIPMAP_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        # aniso = gl.glGetFloatv(gl.GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT)
        # gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAX_ANISOTROPY_EXT, aniso)
        self.inited = True

    def bind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)

    def isInited(self):
        return self.inited
