from __future__ import annotations
from orbitforge.frames.eci_ecef import eci_to_ecef
from orbitforge.frames.geodetic import ecef_to_geodetic


def subpoint(position_eci, tai_s):
    ecef = eci_to_ecef(position_eci, tai_s)
    return ecef_to_geodetic(ecef)

def groundtrack(position_at, start, end, step):
    rows = []
    t = start
    while t <= end + 1e-9:
        lat, lon, alt = subpoint(position_at(t), t)
        rows.append((t, lat, lon, alt))
        t += step
    return rows

def longitude_wraps(track):
    wraps = []
    for a, b in zip(track, track[1:]):
        if abs(b[2] - a[2]) > 3.141592653589793:
            wraps.append((a[0], b[0]))
    return wraps

def ascending_equator_crossings(track):
    out = []
    for a, b in zip(track, track[1:]):
        if a[1] < 0.0 <= b[1]:
            out.append((a[0], b[0]))
    return out
