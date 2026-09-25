from __future__ import annotations

def score(design, weights):
    revisit = design.get('revisit_s', float('inf'))
    coverage = design.get('coverage_fraction', 0.0)
    satellites = design.get('satellites', 0)
    cost = design.get('cost', 0.0)
    return (
        weights.get('coverage', 1.0) * coverage
        - weights.get('revisit', 1.0) * revisit
        - weights.get('satellites', 0.1) * satellites
        - weights.get('cost', 0.01) * cost
    )

def rank(designs, weights):
    return sorted(designs, key=lambda d: score(d, weights), reverse=True)

def feasible(designs, minimum_coverage, maximum_revisit_s, maximum_satellites):
    return [d for d in designs if d.get('coverage_fraction', 0.0) >= minimum_coverage and d.get('revisit_s', float('inf')) <= maximum_revisit_s and d.get('satellites', 0) <= maximum_satellites]
