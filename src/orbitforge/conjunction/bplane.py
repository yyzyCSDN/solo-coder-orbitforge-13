from __future__ import annotations
from orbitforge.core.vector import Vec3

def bplane_basis(relative_velocity: Vec3, reference_normal: Vec3=Vec3(0, 0, 1)):
    s = relative_velocity.unit()
    t = s.cross(reference_normal)
    if t.norm() < 1e-10:
        t = s.cross(Vec3(0, 1, 0))
    t = t.unit()
    r = s.cross(t).unit()
    return (s, t, r)

def bplane_coordinates(relative_position: Vec3, relative_velocity: Vec3):
    _, t, r = bplane_basis(relative_velocity)
    return (relative_position.dot(t), relative_position.dot(r))

def projected_miss_distance(relative_position: Vec3, relative_velocity: Vec3):
    bt, br = bplane_coordinates(relative_position, relative_velocity)
    return (bt * bt + br * br) ** 0.5
