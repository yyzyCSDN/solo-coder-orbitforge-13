from __future__ import annotations
import math
from orbitforge.core.constants import MU_EARTH_KM3_S2

def hohmann(r1_km: float, r2_km: float, mu: float=MU_EARTH_KM3_S2):
    if r1_km <= 0 or r2_km <= 0:
        raise ValueError('positive radii required')
    a = (r1_km + r2_km) / 2
    v1 = math.sqrt(mu / r1_km)
    v2 = math.sqrt(mu / r2_km)
    vt1 = math.sqrt(mu * (2 / r1_km - 1 / a))
    vt2 = math.sqrt(mu * (2 / r2_km - 1 / a))
    t = math.pi * math.sqrt(a ** 3 / mu)
    return {'dv1_km_s': vt1 - v1, 'dv2_km_s': v2 - vt2, 'time_s': t, 'total_dv_km_s': abs(vt1 - v1) + abs(v2 - vt2)}
