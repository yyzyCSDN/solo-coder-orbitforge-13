from __future__ import annotations
import math
from orbitforge.core.vector import Vec3
from orbitforge.time.julian import tai_to_julian_utc

def moon_eci(tai_s: float):
    jd = tai_to_julian_utc(tai_s)
    d = jd - 2451543.5
    node = math.radians((125.1228 - 0.0529538083 * d) % 360.0)
    inc = math.radians(5.1454)
    arg = math.radians((318.0634 + 0.1643573223 * d) % 360.0)
    a = 384400.0
    e = 0.0549
    mean = math.radians((115.3654 + 13.0649929509 * d) % 360.0)
    E = mean
    for _ in range(8):
        E = mean + e * math.sin(E)
    x = a * (math.cos(E) - e)
    y = a * math.sqrt(1.0 - e * e) * math.sin(E)
    v = math.atan2(y, x)
    r = math.hypot(x, y)
    lon = v + arg
    xe = r * (math.cos(node) * math.cos(lon) - math.sin(node) * math.sin(lon) * math.cos(inc))
    ye = r * (math.sin(node) * math.cos(lon) + math.cos(node) * math.sin(lon) * math.cos(inc))
    ze = r * math.sin(lon) * math.sin(inc)
    eps = math.radians(23.4393)
    return Vec3(xe, ye * math.cos(eps) - ze * math.sin(eps), ye * math.sin(eps) + ze * math.cos(eps))
