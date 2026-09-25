from __future__ import annotations
from dataclasses import dataclass
from orbitforge.core.state import TimeWindow

@dataclass(frozen=True)
class AccessSample:
    t: float
    elevation_rad: float
    range_km: float
    clear: bool

def samples_to_windows(samples, min_duration_s: float=0.0):
    windows = []
    start = None
    last_t = None
    for sample in samples:
        if sample.clear and start is None:
            start = sample.t
        if not sample.clear and start is not None:
            if last_t is not None and last_t - start >= min_duration_s:
                windows.append(TimeWindow(start, last_t))
            start = None
        last_t = sample.t
    if start is not None and last_t is not None and (last_t - start >= min_duration_s):
        windows.append(TimeWindow(start, last_t))
    return windows

def best_access(samples):
    clear = [s for s in samples if s.clear]
    return max(clear, key=lambda x: (x.elevation_rad, -x.range_km)) if clear else None
