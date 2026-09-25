from __future__ import annotations
import math
from orbitforge.core.constants import MU_EARTH_KM3_S2, R_EARTH_EQUATOR_KM
from orbitforge.environment.atmosphere import density_kg_m3

def circular_decay_rate_km_s(alt_km: float, ballistic_coefficient_kg_m2: float):
    radius_km = R_EARTH_EQUATOR_KM + alt_km
    speed_m_s = math.sqrt(MU_EARTH_KM3_S2 / radius_km) * 1000.0
    rho = density_kg_m3(alt_km)
    accel = 0.5 * rho * speed_m_s * speed_m_s / ballistic_coefficient_kg_m2
    specific_energy_rate = -accel * speed_m_s
    da_m_s = 2.0 * specific_energy_rate * (radius_km * 1000.0) ** 2 / (MU_EARTH_KM3_S2 * 1000000000.0)
    return da_m_s / 1000.0

def estimate_lifetime_days(alt_km: float, ballistic_coefficient_kg_m2: float, floor_km: float=120.0):
    altitude = alt_km
    elapsed = 0.0
    step = 3600.0
    while altitude > floor_km and elapsed < 100 * 365.25 * 86400.0:
        rate = circular_decay_rate_km_s(altitude, ballistic_coefficient_kg_m2)
        if rate >= 0.0:
            return float('inf')
        altitude += rate * step
        elapsed += step
        if altitude < 250.0:
            step = 300.0
    return elapsed / 86400.0
