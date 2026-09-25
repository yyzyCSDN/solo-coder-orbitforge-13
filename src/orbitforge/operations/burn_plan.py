from __future__ import annotations
from dataclasses import dataclass
from orbitforge.core.vector import Vec3

@dataclass(frozen=True)
class Burn:
    name: str
    epoch_tai_s: float
    delta_v_m_s: Vec3
    tolerance_m_s: float


def total_delta_v(burns):
    return sum(b.delta_v_m_s.norm() for b in burns)

def minimum_spacing(burns):
    ordered = sorted(burns, key=lambda b: b.epoch_tai_s)
    gaps = [b.epoch_tai_s - a.epoch_tai_s for a, b in zip(ordered, ordered[1:])]
    return min(gaps) if gaps else float('inf')

def validate_burns(burns, max_single_burn_m_s, minimum_spacing_s):
    findings = []
    ordered = sorted(burns, key=lambda b: b.epoch_tai_s)
    for burn in ordered:
        if burn.delta_v_m_s.norm() > max_single_burn_m_s:
            findings.append((burn.name, 'burn_limit'))
        if burn.tolerance_m_s <= 0.0:
            findings.append((burn.name, 'invalid_tolerance'))
    for a, b in zip(ordered, ordered[1:]):
        if b.epoch_tai_s - a.epoch_tai_s < minimum_spacing_s:
            findings.append((a.name + '+' + b.name, 'spacing'))
    return findings
