from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class LinkSample:
    t: float
    elevation_rad: float
    margin_db: float
    bitrate_bps: float

def integrate_volume_mb(samples):
    if len(samples) < 2:
        return 0.0
    bits = 0.0
    for a, b in zip(samples, samples[1:]):
        dt = b.t - a.t
        rate = 0.5 * (a.bitrate_bps + b.bitrate_bps)
        bits += max(0.0, dt) * max(0.0, rate)
    return bits / 8000000.0

def outage_fraction(samples):
    if not samples:
        return 1.0
    return sum((1 for s in samples if s.margin_db < 0.0)) / len(samples)

def min_margin(samples):
    return min((s.margin_db for s in samples), default=float('-inf'))
