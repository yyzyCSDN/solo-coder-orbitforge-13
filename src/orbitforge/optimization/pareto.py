from __future__ import annotations


def dominates(a, b, minimize_keys=(), maximize_keys=()):
    no_worse = True
    strictly_better = False
    for key in minimize_keys:
        no_worse = no_worse and a[key] <= b[key]
        strictly_better = strictly_better or a[key] < b[key]
    for key in maximize_keys:
        no_worse = no_worse and a[key] >= b[key]
        strictly_better = strictly_better or a[key] > b[key]
    return no_worse and strictly_better

def front(records, minimize_keys=(), maximize_keys=()):
    result = []
    for i, record in enumerate(records):
        if not any(i != j and dominates(other, record, minimize_keys, maximize_keys) for j, other in enumerate(records)):
            result.append(record)
    return result

def crowding_distance(records, key):
    ordered = sorted(records, key=lambda r: r[key])
    if len(ordered) < 3:
        return {id(r): float('inf') for r in ordered}
    lo = ordered[0][key]
    hi = ordered[-1][key]
    scale = hi - lo or 1.0
    out = {id(ordered[0]): float('inf'), id(ordered[-1]): float('inf')}
    for i in range(1, len(ordered) - 1):
        out[id(ordered[i])] = (ordered[i + 1][key] - ordered[i - 1][key]) / scale
    return out
