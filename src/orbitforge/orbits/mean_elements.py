from __future__ import annotations
import math
from orbitforge.core.constants import MU_EARTH_KM3_S2, J2_EARTH, R_EARTH_EQUATOR_KM

def secular_j2_rates(a_km: float, e: float, inc_rad: float):
    p = a_km * (1.0 - e * e)
    n = math.sqrt(MU_EARTH_KM3_S2 / a_km ** 3)
    factor = 1.5 * J2_EARTH * n * (R_EARTH_EQUATOR_KM / p) ** 2
    raan_rate = -factor * math.cos(inc_rad)
    argp_rate = 0.5 * factor * (5.0 * math.cos(inc_rad) ** 2 - 1.0)
    mean_rate = n + 0.5 * factor * math.sqrt(1.0 - e * e) * (3.0 * math.cos(inc_rad) ** 2 - 1.0)
    return (raan_rate, argp_rate, mean_rate)

def advance_mean_elements(elements: dict, dt_s: float):
    raan_rate, argp_rate, mean_rate = secular_j2_rates(elements['a_km'], elements['e'], elements['i_rad'])
    result = dict(elements)
    result['raan_rad'] = (result['raan_rad'] + raan_rate * dt_s) % (2.0 * math.pi)
    result['argp_rad'] = (result['argp_rad'] + argp_rate * dt_s) % (2.0 * math.pi)
    result['mean_anomaly_rad'] = (result.get('mean_anomaly_rad', 0.0) + mean_rate * dt_s) % (2.0 * math.pi)
    return result
