from __future__ import annotations
import math
from orbitforge.core.vector import Vec3
from orbitforge.core.constants import R_EARTH_EQUATOR_KM

def eclipse_state(sat_eci: Vec3, sun_eci: Vec3):
    sun_dir = sun_eci.unit()
    x = sat_eci.dot(sun_dir)
    if x >= 0:
        return 'sunlit'
    perp = (sat_eci - sun_dir * x).norm()
    if perp < R_EARTH_EQUATOR_KM:
        return 'umbra'
    earth_ang = math.asin(min(1, R_EARTH_EQUATOR_KM / sat_eci.norm()))
    sun_ang = math.asin(min(1, 696340.0 / (sun_eci - sat_eci).norm()))
    sep = sat_eci.angle(sun_eci - sat_eci)
    return 'penumbra' if sep < earth_ang + sun_ang else 'sunlit'

def sunlight_fraction(state: str) -> float:
    return {'sunlit': 1.0, 'penumbra': 0.5, 'umbra': 0.0}[state]
