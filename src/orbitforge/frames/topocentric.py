from __future__ import annotations
import math
from orbitforge.core.vector import Vec3
from .geodetic import geodetic_to_ecef

def ecef_to_enu(target: Vec3, lat: float, lon: float, alt: float=0.0) -> Vec3:
    d = target - geodetic_to_ecef(lat, lon, alt)
    sl, cl = (math.sin(lat), math.cos(lat))
    so, co = (math.sin(lon), math.cos(lon))
    return Vec3(-so * d.x + co * d.y, -sl * co * d.x - sl * so * d.y + cl * d.z, cl * co * d.x + cl * so * d.y + sl * d.z)

def az_el_range(enu: Vec3):
    rng = enu.norm()
    el = math.asin(enu.z / rng) if rng else math.pi / 2
    az = math.atan2(enu.x, enu.y) % (2 * math.pi)
    return (az, el, rng)
