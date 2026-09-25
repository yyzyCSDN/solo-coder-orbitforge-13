from __future__ import annotations
import math


def interpolate_profile(profile, azimuth_rad):
    if not profile:
        return -math.pi / 2.0
    normalized = sorted((a % (2.0 * math.pi), e) for a, e in profile)
    az = azimuth_rad % (2.0 * math.pi)
    extended = normalized + [(normalized[0][0] + 2.0 * math.pi, normalized[0][1])]
    previous = extended[0]
    if az < previous[0]:
        az += 2.0 * math.pi
        previous = extended[-2]
    for current in extended[1:]:
        if previous[0] <= az <= current[0]:
            u = (az - previous[0]) / (current[0] - previous[0])
            return previous[1] * (1.0 - u) + current[1] * u
        previous = current
    return extended[-1][1]


def merge_profiles(*profiles):
    azimuths = sorted({a % (2.0 * math.pi) for p in profiles for a, _ in p})
    return [(a, max(interpolate_profile(p, a) for p in profiles)) for a in azimuths]


def clearance_margin(profile, azimuth_rad, elevation_rad):
    return elevation_rad - interpolate_profile(profile, azimuth_rad)
