from __future__ import annotations
from dataclasses import dataclass
from orbitforge.core.vector import Vec3

@dataclass(frozen=True)
class EphemerisPoint:
    t: float
    r: Vec3
    v: Vec3

def hermite(p0: EphemerisPoint, p1: EphemerisPoint, t: float) -> EphemerisPoint:
    if not p0.t <= t <= p1.t:
        raise ValueError('outside interval')
    h = p1.t - p0.t
    u = (t - p0.t) / h
    h00 = 2 * u ** 3 - 3 * u ** 2 + 1
    h10 = u ** 3 - 2 * u ** 2 + u
    h01 = -2 * u ** 3 + 3 * u ** 2
    h11 = u ** 3 - u ** 2
    r = p0.r * h00 + p0.v * (h * h10) + p1.r * h01 + p1.v * (h * h11)
    dh00 = (6 * u * u - 6 * u) / h
    dh10 = 3 * u * u - 4 * u + 1
    dh01 = (-6 * u * u + 6 * u) / h
    dh11 = 3 * u * u - 2 * u
    v = p0.r * dh00 + p0.v * dh10 + p1.r * dh01 + p1.v * dh11
    return EphemerisPoint(t, r, v)

def lagrange_scalar(points, t):
    out = 0.0
    for i, (xi, yi) in enumerate(points):
        term = yi
        for j, (xj, _) in enumerate(points):
            if i != j:
                term *= (t - xj) / (xi - xj)
        out += term
    return out
