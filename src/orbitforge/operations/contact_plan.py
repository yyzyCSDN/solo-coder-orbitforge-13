from __future__ import annotations
from dataclasses import dataclass
from orbitforge.core.state import TimeWindow

@dataclass(frozen=True)
class Contact:
    station: str
    window: TimeWindow
    volume_mb: float
    priority: int

def allocate_contacts(contacts, station_capacity_mb):
    used = {}
    selected = []
    rejected = []
    for c in sorted(contacts, key=lambda x: (-x.priority, x.window.start_tai_s)):
        cap = station_capacity_mb.get(c.station, 0)
        cur = used.get(c.station, 0)
        if cur + c.volume_mb <= cap:
            selected.append(c)
            used[c.station] = cur + c.volume_mb
        else:
            rejected.append(c)
    return (selected, rejected)

def contact_utilization(selected, station_capacity_mb):
    out = {}
    for s, cap in station_capacity_mb.items():
        out[s] = sum((c.volume_mb for c in selected if c.station == s)) / cap if cap else 0
    return out
