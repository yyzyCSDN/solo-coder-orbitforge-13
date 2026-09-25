from __future__ import annotations
from orbitforge.core.vector import Vec3

def rtn_basis(r: Vec3, v: Vec3):
    radial = r.unit()
    normal = r.cross(v).unit()
    transverse = normal.cross(radial).unit()
    return (radial, transverse, normal)

def inertial_to_rtn(vector: Vec3, r: Vec3, v: Vec3) -> Vec3:
    radial, transverse, normal = rtn_basis(r, v)
    return Vec3(vector.dot(radial), vector.dot(transverse), vector.dot(normal))

def rtn_to_inertial(vector: Vec3, r: Vec3, v: Vec3) -> Vec3:
    radial, transverse, normal = rtn_basis(r, v)
    return radial * vector.x + transverse * vector.y + normal * vector.z

def velocity_normal_binormal(r: Vec3, v: Vec3):
    along = v.unit()
    normal = r.cross(v).unit()
    cross_track = normal.cross(along).unit()
    return (along, cross_track, normal)
