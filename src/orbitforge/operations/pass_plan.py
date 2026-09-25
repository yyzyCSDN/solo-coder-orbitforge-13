from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class PassRequest:
    satellite: str
    station: str
    start: float
    end: float
    priority: int
    expected_mb: float


def conflicts(a: PassRequest, b: PassRequest):
    if a.station != b.station:
        return False
    return a.start < b.end and b.start < a.end

def select(requests):
    selected = []
    rejected = []
    for request in sorted(requests, key=lambda r: (-r.priority, r.end, r.satellite)):
        if any(conflicts(request, existing) for existing in selected):
            rejected.append(request)
        else:
            selected.append(request)
    return sorted(selected, key=lambda r: r.start), rejected

def total_volume(requests):
    return sum(r.expected_mb for r in requests)

def station_utilization(requests, start, end):
    by_station = {}
    duration = end - start
    for request in requests:
        overlap = max(0.0, min(end, request.end) - max(start, request.start))
        by_station[request.station] = by_station.get(request.station, 0.0) + overlap
    return {station: value / duration for station, value in by_station.items()}
