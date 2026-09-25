from __future__ import annotations
import math
from orbitforge.core.vector import Vec3
from orbitforge.core.constants import R_EARTH_EQUATOR_KM, R_EARTH_POLAR_KM
A = R_EARTH_EQUATOR_KM
B = R_EARTH_POLAR_KM
E2 = 1 - B * B / (A * A)

def geodetic_to_ecef(lat: float, lon: float, alt_km: float) -> Vec3:
    s = math.sin(lat)
    c = math.cos(lat)
    n = A / math.sqrt(1 - E2 * s * s)
    return Vec3((n + alt_km) * c * math.cos(lon), (n + alt_km) * c * math.sin(lon), (n * (1 - E2) + alt_km) * s)

def ecef_to_geodetic(v: Vec3):
    lon = math.atan2(v.y, v.x)
    p = math.hypot(v.x, v.y)
    lat = math.atan2(v.z, p * (1 - E2))
    alt = 0.0
    for _ in range(8):
        n = A / math.sqrt(1 - E2 * math.sin(lat) ** 2)
        alt = p / max(1e-15, math.cos(lat)) - n
        lat = math.atan2(v.z, p * (1 - E2 * n / (n + alt)))
    return (lat, lon, alt)
