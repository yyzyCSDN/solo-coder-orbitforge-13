from __future__ import annotations
from dataclasses import dataclass
from orbitforge.core.state import TimeWindow
from .station import GroundStation, look_angles

@dataclass(frozen=True)
class PassEvent:
    rise_tai_s: float
    set_tai_s: float
    max_tai_s: float
    max_elevation_rad: float

def find_passes(station: GroundStation, position_at, start: float, end: float, step: float=30.0):
    out = []
    inside = False
    rise = None
    best = (-1, None)
    t = start
    while t <= end + 1e-09:
        el = look_angles(station, position_at(t), t)[1]
        now = el >= station.min_elevation_rad
        if now and (not inside):
            rise = t
            best = (el, t)
            inside = True
        if now and el > best[0]:
            best = (el, t)
        if inside and (not now):
            out.append(PassEvent(rise, t, best[1], best[0]))
            inside = False
        t += step
    if inside:
        out.append(PassEvent(rise, end, best[1], best[0]))
    return out
