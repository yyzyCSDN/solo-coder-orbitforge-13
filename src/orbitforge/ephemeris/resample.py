from __future__ import annotations
from .interpolation import EphemerisPoint

def resample(series, start: float, end: float, step: float):
    points = []
    t = start
    while t <= end + 1e-09:
        points.append(series.at(min(t, end)))
        t += step
    return points

def interpolation_residuals(series, truth_points):
    residuals = []
    for truth in truth_points:
        estimate = series.at(truth.t)
        residuals.append({'t': truth.t, 'position_error_km': (estimate.r - truth.r).norm(), 'velocity_error_km_s': (estimate.v - truth.v).norm()})
    return residuals

def worst_residual(residuals):
    return max(residuals, key=lambda x: x['position_error_km'], default=None)
