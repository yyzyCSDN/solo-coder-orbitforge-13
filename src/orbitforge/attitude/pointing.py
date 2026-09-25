from __future__ import annotations
from orbitforge.core.vector import Vec3
from .quaternion import Quaternion

def nadir_direction(position_eci: Vec3) -> Vec3:
    return (position_eci * -1).unit()

def off_nadir_angle(position: Vec3, target_direction: Vec3) -> float:
    return nadir_direction(position).angle(target_direction)

def boresight_error(q: Quaternion, body_boresight: Vec3, target: Vec3) -> float:
    return q.rotate(body_boresight).angle(target.unit())

def quaternion_between(a: Vec3, b: Vec3) -> Quaternion:
    au, bu = (a.unit(), b.unit())
    d = au.dot(bu)
    if d < -0.999999:
        axis = Vec3(1, 0, 0).cross(au)
        if axis.norm() < 1e-09:
            axis = Vec3(0, 1, 0).cross(au)
        return Quaternion.from_axis_angle(axis, 3.141592653589793)
    c = au.cross(bu)
    return Quaternion(1 + d, c.x, c.y, c.z).normalized()
