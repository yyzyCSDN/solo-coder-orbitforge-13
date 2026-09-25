from __future__ import annotations
import math
from orbitforge.core.constants import J2_EARTH, R_EARTH_EQUATOR_KM
J3_EARTH = -2.532153e-6

def frozen_eccentricity(a_km: float, inc_rad: float):
    numerator = -J3_EARTH * R_EARTH_EQUATOR_KM * math.sin(inc_rad)
    denominator = 2.0 * J2_EARTH * a_km
    return numerator / denominator

def preferred_argument_of_perigee(inc_rad: float):
    return math.pi / 2.0 if math.sin(inc_rad) >= 0.0 else 3.0 * math.pi / 2.0

def frozen_candidate(a_km, inc_rad):
    e = frozen_eccentricity(a_km, inc_rad)
    return {
        'a_km': a_km,
        'e': abs(e),
        'argp_rad': preferred_argument_of_perigee(inc_rad),
        'valid': abs(e) < 0.1,
    }
