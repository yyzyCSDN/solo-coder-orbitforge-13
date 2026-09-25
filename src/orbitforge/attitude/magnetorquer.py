from __future__ import annotations
from orbitforge.core.vector import Vec3

def torque(moment_dipole_am2: Vec3, magnetic_field_t: Vec3):
    return moment_dipole_am2.cross(magnetic_field_t)

def dipole_for_desired_torque(desired_torque: Vec3, magnetic_field_t: Vec3, max_dipole_am2: float):
    b2 = magnetic_field_t.norm2()
    if b2 < 1e-20:
        return Vec3(0.0, 0.0, 0.0)
    dipole = magnetic_field_t.cross(desired_torque) / b2
    magnitude = dipole.norm()
    if magnitude > max_dipole_am2:
        dipole = dipole.unit() * max_dipole_am2
    return dipole

def controllable_component(desired_torque: Vec3, magnetic_field_t: Vec3):
    if magnetic_field_t.norm2() < 1e-20:
        return Vec3(0.0, 0.0, 0.0)
    parallel = magnetic_field_t * (desired_torque.dot(magnetic_field_t) / magnetic_field_t.norm2())
    return desired_torque - parallel
