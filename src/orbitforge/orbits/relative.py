from __future__ import annotations
import math
from orbitforge.core.vector import Vec3

def hill_frame(chief_r: Vec3, chief_v: Vec3):
    x = chief_r.unit()
    z = chief_r.cross(chief_v).unit()
    y = z.cross(x)
    return (x, y, z)

def relative_hill(chief_r, chief_v, deputy_r, deputy_v):
    x, y, z = hill_frame(chief_r, chief_v)
    dr = deputy_r - chief_r
    dv = deputy_v - chief_v
    return (Vec3(dr.dot(x), dr.dot(y), dr.dot(z)), Vec3(dv.dot(x), dv.dot(y), dv.dot(z)))

def cwh_propagate(rel_r: Vec3, rel_v: Vec3, n: float, t: float):
    c, s = (math.cos(n * t), math.sin(n * t))
    x = (4 - 3 * c) * rel_r.x + s / n * rel_v.x + 2 * (1 - c) / n * rel_v.y
    y = 6 * (s - n * t) * rel_r.x + rel_r.y - 2 * (1 - c) / n * rel_v.x + (4 * s - 3 * n * t) / n * rel_v.y
    z = c * rel_r.z + s / n * rel_v.z
    return Vec3(x, y, z)
