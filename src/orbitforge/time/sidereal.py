from __future__ import annotations
import math
from .julian import unix_to_julian
from .leap_seconds import tai_to_utc_unix

def gmst_angle(tai_s: float) -> float:
    jd = unix_to_julian(tai_to_utc_unix(tai_s))
    d = jd - 2451545.0
    deg = 280.46061837 + 360.98564736629 * d + 0.000387933 * (d / 36525.0) ** 2
    return math.radians(deg % 360.0)

def local_sidereal(tai_s: float, lon_rad: float) -> float:
    return (gmst_angle(tai_s) + lon_rad) % (2 * math.pi)
