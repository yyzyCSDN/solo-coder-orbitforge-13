from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class OpsEvent:
    t: float
    name: str
    subsystem: str
    severity: str = 'info'

def merge_events(*streams):
    events = [event for stream in streams for event in stream]
    return sorted(events, key=lambda e: (e.t, e.subsystem, e.name))

def subsystem_load(events, start, end):
    counts = {}
    for event in events:
        if start <= event.t < end:
            counts[event.subsystem] = counts.get(event.subsystem, 0) + 1
    return counts

def critical_events(events):
    return [event for event in events if event.severity in {'error', 'critical'}]

def quiet_windows(events, start, end, minimum_gap_s):
    times = [start] + [e.t for e in events if start < e.t < end] + [end]
    return [(a, b) for a, b in zip(times, times[1:]) if b - a >= minimum_gap_s]
