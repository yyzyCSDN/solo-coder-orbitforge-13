from __future__ import annotations
import math
from orbitforge.core.constants import SOLAR_CONSTANT_W_M2

def panel_power_w(area_m2: float, efficiency: float, incidence_rad: float, distance_au: float=1.0, degradation: float=1.0):
    cosine = max(0.0, math.cos(incidence_rad))
    return SOLAR_CONSTANT_W_M2 / (distance_au * distance_au) * area_m2 * efficiency * cosine * degradation

def annual_degradation(initial_efficiency: float, rate_per_year: float, years: float):
    return initial_efficiency * (1 - rate_per_year) ** years
