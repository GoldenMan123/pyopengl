from numpy import *


def dist(x, y):
    r = 0.0
    for i in range(3):
        r += (x[i] - y[i]) ** 2
    return r


def mul(a, b):
    return transpose(dot(transpose(a), transpose(b)))


def mul_v(a, b):
    return dot(transpose(a), b)


def v3_v4(a):
    return array([a[0], a[1], a[2], 1.0], 'f')


def v4_v3(a):
    return array([a[0] / a[3], a[1] / a[3], a[2] / a[3]], 'f')


def normalize(x):
    result = x.copy()
    norm = 0.0
    for i in result:
        norm += i * i
    if norm > 0:
        for i in range(len(result)):
            result[i] /= sqrt(norm)
    return result


def translate(v):
    result = identity(4, 'f')
    result[3][0] = v[0]
    result[3][1] = v[1]
    result[3][2] = v[2]
    return result


def rotate(angle, axis):
    result = identity(4, 'f')
    u = normalize(axis)
    a = angle * pi / 180.0
    result[0][0] = cos(a) + u[0] * u[0] * (1 - cos(a))
    result[0][1] = u[1] * u[0] * (1 - cos(a)) + u[2] * sin(a)
    result[0][2] = u[2] * u[0] * (1 - cos(a)) - u[1] * sin(a)
    result[1][0] = u[0] * u[1] * (1 - cos(a)) - u[2] * sin(a)
    result[1][1] = cos(a) + u[1] * u[1] * (1 - cos(a))
    result[1][2] = u[2] * u[1] * (1 - cos(a)) + u[0] * sin(a)
    result[2][0] = u[0] * u[2] * (1 - cos(a)) + u[1] * sin(a)
    result[2][1] = u[1] * u[2] * (1 - cos(a)) - u[0] * sin(a)
    result[2][2] = cos(a) + u[2] * u[2] * (1 - cos(a))
    return result


def scale(s):
    result = identity(4, 'f')
    result[0][0] = s[0]
    result[1][1] = s[1]
    result[2][2] = s[2]
    return result
