from __future__ import annotations
import statistics


def moving_average(values, window):
    if window <= 0:
        raise ValueError('positive window')
    out = []
    running = 0.0
    for i, value in enumerate(values):
        running += value
        if i >= window:
            running -= values[i - window]
        out.append(running / min(window, i + 1))
    return out


def robust_zscores(values):
    if not values:
        return []
    median = statistics.median(values)
    deviations = [abs(v - median) for v in values]
    mad = statistics.median(deviations)
    scale = 1.4826 * mad
    if scale <= 1e-15:
        return [0.0 for _ in values]
    return [(v - median) / scale for v in values]


def anomalies(values, limit=4.0):
    return [(i, v, z) for i, (v, z) in enumerate(zip(values, robust_zscores(values))) if abs(z) >= limit]
