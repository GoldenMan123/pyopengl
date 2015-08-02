import OpenGL.GL as gl
from numpy import *
from shaderprogram import *
from ctypes import *


class VertexData:
    pos = zeros(3, 'f')
    nor = zeros(3, 'f')
    tex = zeros(2, 'f')


class GLObject:
    pData = None
    pIndices = None

    vao = None
    vbo = None

    def __init__(self):
        pass

    def release(self):
        if self.vbo:
            gl.glDeleteBuffers(2, self.vbo)
        if self.vao:
            gl.glDeleteVertexArrays(1, self.vao)
            self.vao = None

    def initGLBuffers(self):
        if self.vbo:
            gl.glDeleteBuffers(2, self.vbo)
        if self.vao:
            gl.glDeleteVertexArrays(1, self.vao)
            self.vao = None

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)
        self.vbo = gl.glGenBuffers(2)

        data = array([], 'f')
        for i in self.pData:
            data = concatenate((data, i.pos))
            data = concatenate((data, i.nor))
            data = concatenate((data, i.tex))

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo[0])
        gl.glBufferData(gl.GL_ARRAY_BUFFER, (gl.GLfloat * len(data))(*data), gl.GL_STATIC_DRAW)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.vbo[1])
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, (gl.GLuint * len(self.pIndices))(*self.pIndices), gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(POSITION_LOCATION, 3, gl.GL_FLOAT, gl.GL_FALSE,
            8 * sizeof(gl.GLfloat), c_void_p(0 * sizeof(gl.GLfloat)))
        gl.glEnableVertexAttribArray(POSITION_LOCATION)

        gl.glVertexAttribPointer(NORMAL_LOCATION, 3, gl.GL_FLOAT, gl.GL_FALSE,
            8 * sizeof(gl.GLfloat), c_void_p(3 * sizeof(gl.GLfloat)))
        gl.glEnableVertexAttribArray(NORMAL_LOCATION)

        gl.glVertexAttribPointer(TEXTURE_LOCATION, 2, gl.GL_FLOAT, gl.GL_FALSE,
            8 * sizeof(gl.GLfloat), c_void_p(6 * sizeof(gl.GLfloat)))
        gl.glEnableVertexAttribArray(TEXTURE_LOCATION)

        gl.glBindVertexArray(0)

    def draw(self):
        gl.glUniform1i(INST_FLAG_LOCATION, 0)
        gl.glBindVertexArray(self.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, len(self.pIndices), gl.GL_UNSIGNED_INT, None)
        gl.glBindVertexArray(0)
