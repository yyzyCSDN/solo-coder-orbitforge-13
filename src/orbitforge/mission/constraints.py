from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ConstraintResult:
    name: str
    ok: bool
    value: float
    limit: float
    sense: str

def upper(name, value, limit):
    return ConstraintResult(name, value <= limit, value, limit, '<=')

def lower(name, value, limit):
    return ConstraintResult(name, value >= limit, value, limit, '>=')

def all_ok(results):
    return all((r.ok for r in results))

def violations(results):
    return [r for r in results if not r.ok]
