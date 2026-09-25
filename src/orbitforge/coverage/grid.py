from __future__ import annotations
import math

def equal_angle_grid(lat_step_deg=5, lon_step_deg=5):
    pts = []
    lat = -90 + lat_step_deg / 2
    while lat < 90:
        lon = -180 + lon_step_deg / 2
        while lon < 180:
            pts.append((math.radians(lat), math.radians(lon)))
            lon += lon_step_deg
        lat += lat_step_deg
    return pts

def weighted_coverage(visited, weights):
    total = sum(weights.values())
    hit = sum((weights.get(p, 0) for p in visited))
    return hit / total if total else 0
