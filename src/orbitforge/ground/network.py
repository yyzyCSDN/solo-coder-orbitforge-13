from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class StationCapability:
    name: str
    bands: frozenset[str]
    max_channels: int
    availability: float = 1.0


def compatible_stations(stations, band):
    return [s for s in stations if band in s.bands and s.max_channels > 0]


def network_availability(stations):
    probability_all_down = 1.0
    for station in stations:
        probability_all_down *= 1.0 - station.availability
    return 1.0 - probability_all_down


def allocate_simultaneous_contacts(requests, stations):
    capacities = {s.name: s.max_channels for s in stations}
    assigned = []
    rejected = []
    for request in sorted(requests, key=lambda x: (-x['priority'], x['start'])):
        candidates = [s for s in stations if request['band'] in s.bands and capacities[s.name] > 0]
        candidates.sort(key=lambda s: (-s.availability, s.name))
        if not candidates:
            rejected.append(request)
            continue
        chosen = candidates[0]
        capacities[chosen.name] -= 1
        assigned.append((request, chosen.name))
    return assigned, rejected
