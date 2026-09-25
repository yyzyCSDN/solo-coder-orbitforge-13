from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class PowerMode:
    name: str
    load_w: float
    allowed_in_eclipse: bool = True

def validate_mode_timeline(segments, modes):
    table = {m.name: m for m in modes}
    issues = []
    for name, duration_s, eclipse in segments:
        if name not in table:
            issues.append(('unknown_mode', name))
            continue
        if eclipse and (not table[name].allowed_in_eclipse):
            issues.append(('eclipse_forbidden', name))
        if duration_s < 0:
            issues.append(('negative_duration', name))
    return issues

def energy_wh(segments, modes):
    table = {m.name: m.load_w for m in modes}
    return sum((table[name] * duration_s / 3600.0 for name, duration_s, _ in segments))
