from __future__ import annotations
import math
from orbitforge.core.constants import R_EARTH_EQUATOR_KM

def central_angle_to_horizon(alt_km: float) -> float:
    return math.acos(R_EARTH_EQUATOR_KM / (R_EARTH_EQUATOR_KM + alt_km))

def footprint_radius_km(alt_km: float, min_elevation_rad: float=0.0):
    re = R_EARTH_EQUATOR_KM
    rs = re + alt_km
    alpha = math.acos(re / rs * math.cos(min_elevation_rad)) - min_elevation_rad
    return re * alpha

def swath_width_km(alt_km: float, half_angle_rad: float):
    return 2 * alt_km * math.tan(half_angle_rad)

def revisit_estimate_s(orbit_period_s: float, swath_km: float, latitude_rad: float=0.0):
    circumference = 2 * math.pi * R_EARTH_EQUATOR_KM * max(0.1, math.cos(latitude_rad))
    tracks = max(1, circumference / max(swath_km, 1e-09))
    return orbit_period_s * tracks
