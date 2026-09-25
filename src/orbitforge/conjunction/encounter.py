from __future__ import annotations
from orbitforge.core.vector import Vec3

def encounter_frame(rel_r: Vec3, rel_v: Vec3):
    x = rel_v.unit()
    z = rel_r.cross(rel_v).unit()
    y = z.cross(x).unit()
    return (x, y, z)

def project_to_plane(rel_r: Vec3, rel_v: Vec3):
    x, y, z = encounter_frame(rel_r, rel_v)
    return (rel_r.dot(y), rel_r.dot(z))

def time_of_closest_approach(rel_r: Vec3, rel_v: Vec3):
    d = rel_v.norm2()
    return 0.0 if d < 1e-18 else -rel_r.dot(rel_v) / d
