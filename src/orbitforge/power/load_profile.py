from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class LoadMode:
    name: str
    watts: float

def energy_for_segments(segments, modes):
    table = {m.name: m.watts for m in modes}
    return sum((table[name] * duration / 3600 for name, duration in segments))

def peak_load(segments, modes):
    table = {m.name: m.watts for m in modes}
    return max((table[name] for name, _ in segments), default=0.0)
