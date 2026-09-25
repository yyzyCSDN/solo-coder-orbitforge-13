from __future__ import annotations
import math
from orbitforge.core.constants import MU_EARTH_KM3_S2


def semi_major_for_repeat(orbits: int, sidereal_days: int, sidereal_day_s: float = 86164.0905):
    if orbits <= 0 or sidereal_days <= 0:
        raise ValueError('positive repeat integers required')
    period = sidereal_days * sidereal_day_s / orbits
    return (MU_EARTH_KM3_S2 * (period / (2.0 * math.pi)) ** 2) ** (1.0 / 3.0)

def repeat_error_seconds(a_km: float, orbits: int, sidereal_days: int, sidereal_day_s: float = 86164.0905):
    period = 2.0 * math.pi * math.sqrt(a_km ** 3 / MU_EARTH_KM3_S2)
    return orbits * period - sidereal_days * sidereal_day_s

def search_repeat(target_a_km: float, max_days: int = 30, max_orbits: int = 500):
    candidates = []
    for days in range(1, max_days + 1):
        for orbits in range(1, max_orbits + 1):
            a = semi_major_for_repeat(orbits, days)
            candidates.append((abs(a - target_a_km), days, orbits, a))
    candidates.sort()
    return candidates[:20]
