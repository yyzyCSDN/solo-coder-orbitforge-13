from __future__ import annotations
import math
from dataclasses import dataclass

@dataclass(frozen=True)
class WalkerSlot:
    plane: int
    slot: int
    raan_rad: float
    mean_anomaly_rad: float

def walker_delta(total_satellites: int, planes: int, phasing: int):
    if total_satellites % planes != 0:
        raise ValueError('satellites must divide evenly among planes')
    per_plane = total_satellites // planes
    slots = []
    for p in range(planes):
        raan = 2.0 * math.pi * p / planes
        for s in range(per_plane):
            anomaly = 2.0 * math.pi * (s / per_plane + phasing * p / total_satellites)
            slots.append(WalkerSlot(p, s, raan % (2 * math.pi), anomaly % (2 * math.pi)))
    return slots

def plane_spacing_deg(planes):
    return 360.0 / planes
