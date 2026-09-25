from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Command:
    t: float
    subsystem: str
    opcode: str
    args: tuple = ()

def validate_sequence(commands, minimum_spacing_s: float=0.0):
    issues = []
    ordered = sorted(commands, key=lambda c: c.t)
    for a, b in zip(ordered, ordered[1:]):
        if b.t - a.t < minimum_spacing_s:
            issues.append(('spacing', a, b))
        if a.t == b.t and a.subsystem == b.subsystem:
            issues.append(('same_subsystem_collision', a, b))
    return issues

def command_rate(commands, start: float, end: float):
    if end <= start:
        raise ValueError('invalid interval')
    count = sum((1 for c in commands if start <= c.t < end))
    return count / (end - start)
