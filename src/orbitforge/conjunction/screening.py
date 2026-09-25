from __future__ import annotations
from orbitforge.core.vector import Vec3

def screen_pairs(objects, threshold_km):
    out = []
    for i, a in enumerate(objects):
        for b in objects[i + 1:]:
            d = (a[1] - b[1]).norm()
            if d <= threshold_km:
                out.append((a[0], b[0], d))
    return sorted(out, key=lambda x: x[2])

def severity(miss_km, pc):
    return 'critical' if pc >= 0.0001 else 'high' if pc >= 1e-05 else 'watch' if miss_km < 5 else 'low'
