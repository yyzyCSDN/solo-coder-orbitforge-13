from __future__ import annotations
import math


def apparent_magnitude(reference_mag, range_km, reference_range_km=1000.0, phase_fraction=1.0):
    if range_km <= 0.0 or phase_fraction <= 0.0:
        return float('inf')
    distance_term = 5.0 * math.log10(range_km / reference_range_km)
    phase_term = -2.5 * math.log10(phase_fraction)
    return reference_mag + distance_term + phase_term

def sky_brightness_penalty(sun_elevation_rad, moon_fraction=0.0):
    twilight = max(0.0, (sun_elevation_rad + math.radians(18.0)) / math.radians(18.0))
    return 5.0 * min(1.0, twilight) + 2.0 * max(0.0, min(1.0, moon_fraction))

def optical_detectable(apparent_mag, limiting_mag, sky_penalty=0.0):
    return apparent_mag + sky_penalty <= limiting_mag
