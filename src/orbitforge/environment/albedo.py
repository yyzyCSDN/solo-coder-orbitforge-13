from __future__ import annotations
import math
from orbitforge.core.constants import SOLAR_CONSTANT_W_M2, R_EARTH_EQUATOR_KM

def earth_view_factor(alt_km: float):
    radius = R_EARTH_EQUATOR_KM + alt_km
    beta = math.asin(R_EARTH_EQUATOR_KM / radius)
    return 0.5 * (1.0 - math.cos(beta))

def albedo_flux_w_m2(alt_km: float, sunlit_fraction: float, bond_albedo: float=0.3):
    return SOLAR_CONSTANT_W_M2 * bond_albedo * earth_view_factor(alt_km) * sunlit_fraction

def earth_ir_flux_w_m2(alt_km: float, surface_flux_w_m2: float=237.0):
    return surface_flux_w_m2 * earth_view_factor(alt_km)
