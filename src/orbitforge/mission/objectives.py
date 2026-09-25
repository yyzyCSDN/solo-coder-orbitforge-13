from __future__ import annotations

def weighted_score(metrics, weights):
    return sum((metrics.get(k, 0.0) * v for k, v in weights.items()))

def pareto_front(points, keys):
    out = []
    for i, p in enumerate(points):
        dominated = False
        for j, q in enumerate(points):
            if i != j and all((q[k] >= p[k] for k in keys)) and any((q[k] > p[k] for k in keys)):
                dominated = True
                break
        if not dominated:
            out.append(p)
    return out
