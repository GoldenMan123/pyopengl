import png
import OpenGL.GL as gl
from numpy import *


class Texture:
    inited = False
    texture_id = 0
    width = 0
    height = 0

    def __init__(self, texture_id):
        self.texture_id = texture_id

    def load(self, filename):
        self.width, self.height, r, t = png.Reader(filename=filename).asRGBA8()
        arr = concatenate(array(list(r)))
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

    def bind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)

    def isInited(self):
        return self.inited