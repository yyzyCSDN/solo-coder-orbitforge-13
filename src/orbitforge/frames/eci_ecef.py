from __future__ import annotations
from orbitforge.core.vector import Vec3
from orbitforge.core.constants import OMEGA_EARTH_RAD_S
from orbitforge.time.sidereal import gmst_angle
from .rotations import rz, mv, transpose

def eci_to_ecef(position: Vec3, tai_s: float) -> Vec3:
    return mv(rz(gmst_angle(tai_s)), position)

def ecef_to_eci(position: Vec3, tai_s: float) -> Vec3:
    return mv(transpose(rz(gmst_angle(tai_s))), position)

def eci_state_to_ecef(position: Vec3, velocity: Vec3, tai_s: float):
    r = eci_to_ecef(position, tai_s)
    vrot = mv(rz(gmst_angle(tai_s)), velocity)
    omega = Vec3(0, 0, OMEGA_EARTH_RAD_S)
    return (r, vrot - omega.cross(r))

def ecef_state_to_eci(position: Vec3, velocity: Vec3, tai_s: float):
    omega = Vec3(0, 0, OMEGA_EARTH_RAD_S)
    return (ecef_to_eci(position, tai_s), mv(transpose(rz(gmst_angle(tai_s))), velocity + omega.cross(position)))
