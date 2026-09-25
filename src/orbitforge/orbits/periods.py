from __future__ import annotations
import math
from orbitforge.core.constants import MU_EARTH_KM3_S2, J2_EARTH, R_EARTH_EQUATOR_KM

def orbital_period_s(a_km):
    return 2 * math.pi * math.sqrt(a_km ** 3 / MU_EARTH_KM3_S2)

def mean_motion_rad_s(a_km):
    return math.sqrt(MU_EARTH_KM3_S2 / a_km ** 3)

def j2_raan_rate(a_km, e, i):
    n = mean_motion_rad_s(a_km)
    p = a_km * (1 - e * e)
    return -1.5 * J2_EARTH * n * (R_EARTH_EQUATOR_KM / p) ** 2 * math.cos(i)

def sun_sync_inclination(a_km, e=0.0, target_rate_rad_s=1.991063853e-07):
    n = mean_motion_rad_s(a_km)
    p = a_km * (1 - e * e)
    c = -target_rate_rad_s / (1.5 * J2_EARTH * n * (R_EARTH_EQUATOR_KM / p) ** 2)
    return math.acos(max(-1, min(1, c)))
