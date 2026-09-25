from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class DataProduct:
    name: str
    size_mb: float
    priority: int
    created_tai_s: float

def plan_downlink(products, capacity_mb):
    chosen = []
    used = 0.0
    for p in sorted(products, key=lambda x: (-x.priority, x.created_tai_s, x.name)):
        if used + p.size_mb <= capacity_mb + 1e-12:
            chosen.append(p)
            used += p.size_mb
    return chosen

def backlog_age(products, now):
    return max((now - p.created_tai_s for p in products), default=0.0)
