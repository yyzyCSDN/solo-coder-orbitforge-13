from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Scenario:
    name: str
    parameters: dict
    tags: set[str] = field(default_factory=set)

def cartesian_scenarios(axes):
    keys = list(axes)
    out = [({}, 0)]
    for key in keys:
        next_out = []
        for base, _ in out:
            for value in axes[key]:
                row = dict(base)
                row[key] = value
                next_out.append((row, 0))
        out = next_out
    return [Scenario('scenario_%04d' % i, row) for i, (row, _) in enumerate(out, 1)]

def filter_scenarios(scenarios, predicate):
    return [s for s in scenarios if predicate(s.parameters)]

def group_by_tag(scenarios, tag):
    return [s for s in scenarios if tag in s.tags]
