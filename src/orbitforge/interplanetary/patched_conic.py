from __future__ import annotations
import math


def hyperbolic_excess(departure_velocity, planet_velocity):
    return (departure_velocity - planet_velocity).norm()


def c3_km2_s2(v_infinity_km_s):
    return v_infinity_km_s * v_infinity_km_s


def departure_delta_v(mu_planet, parking_radius_km, v_infinity_km_s):
    circular = math.sqrt(mu_planet / parking_radius_km)
    pericenter = math.sqrt(v_infinity_km_s ** 2 + 2.0 * mu_planet / parking_radius_km)
    return pericenter - circular


def capture_delta_v(mu_planet, periapsis_radius_km, v_infinity_km_s, target_apoapsis_km):
    hyperbolic = math.sqrt(v_infinity_km_s ** 2 + 2.0 * mu_planet / periapsis_radius_km)
    semi_major = 0.5 * (periapsis_radius_km + target_apoapsis_km)
    captured = math.sqrt(mu_planet * (2.0 / periapsis_radius_km - 1.0 / semi_major))
    return hyperbolic - captured
