from __future__ import annotations
import math
from orbitforge.core.vector import Vec3
from orbitforge.core.constants import AU_KM
from orbitforge.time.julian import tai_to_julian_utc

def sun_eci(tai_s: float) -> Vec3:
    jd = tai_to_julian_utc(tai_s)
    n = jd - 2451545.0
    L = math.radians((280.46 + 0.9856474 * n) % 360)
    g = math.radians((357.528 + 0.9856003 * n) % 360)
    lam = L + math.radians(1.915) * math.sin(g) + math.radians(0.02) * math.sin(2 * g)
    eps = math.radians(23.439 - 4e-07 * n)
    r = AU_KM * (1.00014 - 0.01671 * math.cos(g) - 0.00014 * math.cos(2 * g))
    return Vec3(r * math.cos(lam), r * math.cos(eps) * math.sin(lam), r * math.sin(eps) * math.sin(lam))
