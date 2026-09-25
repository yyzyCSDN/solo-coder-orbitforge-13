from __future__ import annotations
import math
from collections import defaultdict


def angular_distance(lat1, lon1, lat2, lon2):
    dlon = lon2 - lon1
    c = math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(dlon)
    return math.acos(max(-1.0, min(1.0, c)))


def visible_cells(subsatellite_points, grid, max_central_angle_rad):
    visible = set()
    for index, (lat, lon) in enumerate(grid):
        if any(angular_distance(lat, lon, slat, slon) <= max_central_angle_rad for slat, slon in subsatellite_points):
            visible.add(index)
    return visible


def coverage_fraction(visible, grid):
    return len(visible) / len(grid) if grid else 0.0


def multiplicity(subsatellite_points, grid, max_central_angle_rad):
    counts = defaultdict(int)
    for index, (lat, lon) in enumerate(grid):
        for slat, slon in subsatellite_points:
            if angular_distance(lat, lon, slat, slon) <= max_central_angle_rad:
                counts[index] += 1
    return dict(counts)


def minimum_multiplicity(counts, grid_size):
    return min((counts.get(i, 0) for i in range(grid_size)), default=0)
