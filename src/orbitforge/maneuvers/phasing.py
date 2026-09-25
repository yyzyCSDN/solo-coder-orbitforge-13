from __future__ import annotations
import math
from orbitforge.core.constants import MU_EARTH_KM3_S2

def phasing_orbit_for_angle(reference_radius_km: float, phase_angle_rad: float, revolutions: int=1):
    reference_period = 2.0 * math.pi * math.sqrt(reference_radius_km ** 3 / MU_EARTH_KM3_S2)
    desired_time = revolutions * reference_period - phase_angle_rad / (2.0 * math.pi) * reference_period
    if desired_time <= 0.0:
        raise ValueError('phase request requires nonpositive time')
    phase_period = desired_time / revolutions
    semi_major = (MU_EARTH_KM3_S2 * (phase_period / (2.0 * math.pi)) ** 2) ** (1.0 / 3.0)
    return {'phase_period_s': phase_period, 'semi_major_km': semi_major, 'reference_period_s': reference_period}

def phasing_delta_v(reference_radius_km: float, phase_semi_major_km: float):
    circular = math.sqrt(MU_EARTH_KM3_S2 / reference_radius_km)
    transfer = math.sqrt(MU_EARTH_KM3_S2 * (2.0 / reference_radius_km - 1.0 / phase_semi_major_km))
    return abs(transfer - circular) * 2.0
