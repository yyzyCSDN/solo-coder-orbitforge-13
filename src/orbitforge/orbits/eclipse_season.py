from __future__ import annotations
import math


def beta_angle(orbit_normal, sun_direction):
    return math.asin(max(-1.0, min(1.0, orbit_normal.unit().dot(sun_direction.unit()))))

def critical_beta_rad(earth_radius_km, orbit_radius_km, sun_angular_radius_rad=0.00465):
    limb = math.asin(earth_radius_km / orbit_radius_km)
    return max(0.0, limb - sun_angular_radius_rad)

def eclipse_possible(beta_rad, critical_beta):
    return abs(beta_rad) < critical_beta

def eclipse_fraction_circular(beta_rad, earth_radius_km, orbit_radius_km):
    crit = critical_beta_rad(earth_radius_km, orbit_radius_km, 0.0)
    if abs(beta_rad) >= crit:
        return 0.0
    ratio = math.sqrt(max(0.0, earth_radius_km ** 2 - orbit_radius_km ** 2 * math.sin(beta_rad) ** 2))
    angle = math.asin(min(1.0, ratio / (orbit_radius_km * math.cos(beta_rad))))
    return angle / math.pi
