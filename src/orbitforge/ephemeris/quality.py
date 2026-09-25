from __future__ import annotations
import math

def cadence_stats(times):
    intervals = [b - a for a, b in zip(times, times[1:])]
    if not intervals:
        return {'count': len(times), 'min_s': None, 'max_s': None, 'mean_s': None}
    return {'count': len(times), 'min_s': min(intervals), 'max_s': max(intervals), 'mean_s': sum(intervals) / len(intervals)}

def detect_time_gaps(times, multiple: float=3.0):
    stats = cadence_stats(times)
    if stats['mean_s'] is None:
        return []
    threshold = stats['mean_s'] * multiple
    return [(a, b, b - a) for a, b in zip(times, times[1:]) if b - a > threshold]

def state_norm_drift(points):
    if not points:
        return 0.0
    radii = [p.r.norm() for p in points]
    return max(radii) - min(radii)
