from __future__ import annotations
from orbitforge.core.vector import Vec3
from orbitforge.core.constants import MU_EARTH_KM3_S2, R_EARTH_EQUATOR_KM, J2_EARTH

def gravity_j2(r: Vec3) -> Vec3:
    d = r.norm()
    x, y, z = (r.x, r.y, r.z)
    base = -MU_EARTH_KM3_S2 / d ** 3
    f = 1.5 * J2_EARTH * (R_EARTH_EQUATOR_KM / d) ** 2
    q = 5 * z * z / (d * d)
    return Vec3(base * x * (1 + f * (1 - q)), base * y * (1 + f * (1 - q)), base * z * (1 + f * (3 - q)))

def exponential_drag(r: Vec3, v_rel: Vec3, area_m2: float, mass_kg: float, cd: float=2.2) -> Vec3:
    alt = max(0.0, r.norm() - R_EARTH_EQUATOR_KM)
    rho0 = 3.614e-13
    h0 = 700.0
    H = 88.667
    rho = rho0 * __import__('math').exp(-(alt - h0) / H)
    speed = v_rel.norm() * 1000
    factor = -0.5 * cd * area_m2 / mass_kg * rho * speed / 1000
    return v_rel * factor
