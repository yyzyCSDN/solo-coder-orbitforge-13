from __future__ import annotations
import math


def turning_angle(mu_planet, periapsis_radius_km, v_infinity_km_s):
    eccentricity = 1.0 + periapsis_radius_km * v_infinity_km_s ** 2 / mu_planet
    return 2.0 * math.asin(1.0 / eccentricity)


def required_periapsis(mu_planet, v_infinity_km_s, turn_angle_rad):
    eccentricity = 1.0 / math.sin(turn_angle_rad / 2.0)
    return mu_planet * (eccentricity - 1.0) / (v_infinity_km_s ** 2)


def feasible(mu_planet, v_infinity_km_s, turn_angle_rad, minimum_periapsis_km):
    return required_periapsis(mu_planet, v_infinity_km_s, turn_angle_rad) >= minimum_periapsis_km
