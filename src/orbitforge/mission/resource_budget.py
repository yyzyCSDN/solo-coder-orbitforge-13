from __future__ import annotations

def accumulate(resources, activities):
    totals = {name: 0.0 for name in resources}
    for activity in activities:
        duration_s = activity['duration_s']
        for name, rate in activity.get('rates', {}).items():
            totals[name] = totals.get(name, 0.0) + rate * duration_s
    return totals

def margins(capacities, totals):
    return {name: capacities[name] - totals.get(name, 0.0) for name in capacities}

def violations(capacities, totals):
    return {name: margin for name, margin in margins(capacities, totals).items() if margin < 0.0}

def normalized_usage(capacities, totals):
    out = {}
    for name, capacity in capacities.items():
        out[name] = totals.get(name, 0.0) / capacity if capacity else float('inf')
    return out
