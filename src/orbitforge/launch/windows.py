from __future__ import annotations
import math
from orbitforge.core.constants import OMEGA_EARTH_RAD_S, R_EARTH_EQUATOR_KM


def launch_site_rotation_speed(lat_rad):
    return OMEGA_EARTH_RAD_S * R_EARTH_EQUATOR_KM * math.cos(lat_rad)


def azimuth_for_inclination(site_lat_rad, target_inclination_rad):
    ratio = math.cos(target_inclination_rad) / math.cos(site_lat_rad)
    if abs(ratio) > 1.0:
        raise ValueError('target inclination unreachable from site without dogleg')
    return math.asin(ratio)


def plane_crossing_times(node_longitude_rad, site_longitude_rad, start_tai_s, sidereal_period_s=86164.0905):
    phase = (node_longitude_rad - site_longitude_rad) % (2.0 * math.pi)
    first = start_tai_s + phase / (2.0 * math.pi) * sidereal_period_s
    return [first + k * sidereal_period_s for k in range(4)]


def launch_energy_bonus_km_s(site_lat_rad, launch_azimuth_rad):
    speed = launch_site_rotation_speed(site_lat_rad)
    return speed * math.sin(launch_azimuth_rad)
