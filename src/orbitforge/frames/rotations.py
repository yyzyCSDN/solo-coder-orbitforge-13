from __future__ import annotations
import math
from orbitforge.core.vector import Vec3

def rx(a):
    c, s = (math.cos(a), math.sin(a))
    return ((1, 0, 0), (0, c, -s), (0, s, c))

def ry(a):
    c, s = (math.cos(a), math.sin(a))
    return ((c, 0, s), (0, 1, 0), (-s, 0, c))

def rz(a):
    c, s = (math.cos(a), math.sin(a))
    return ((c, -s, 0), (s, c, 0), (0, 0, 1))

def mv(m, v: Vec3) -> Vec3:
    return Vec3(sum((m[0][i] * v.as_tuple()[i] for i in range(3))), sum((m[1][i] * v.as_tuple()[i] for i in range(3))), sum((m[2][i] * v.as_tuple()[i] for i in range(3))))

def mm(a, b):
    return tuple((tuple((sum((a[i][k] * b[k][j] for k in range(3))) for j in range(3))) for i in range(3)))

def transpose(m):
    return tuple((tuple((m[j][i] for j in range(3))) for i in range(3)))
