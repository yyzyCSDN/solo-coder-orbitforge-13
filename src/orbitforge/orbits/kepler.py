from __future__ import annotations
import math
from orbitforge.core.errors import ConvergenceError

def solve_kepler_elliptic(mean_anomaly: float, e: float, tol: float=1e-12, max_iter: int=50) -> float:
    if not 0 <= e < 1:
        raise ValueError('elliptic eccentricity required')
    m = (mean_anomaly + math.pi) % (2 * math.pi) - math.pi
    E = m if e < 0.8 else math.copysign(math.pi, m if m else 1)
    for _ in range(max_iter):
        f = E - e * math.sin(E) - m
        fp = 1 - e * math.cos(E)
        step = f / fp
        E -= step
        if abs(step) < tol:
            return E
    raise ConvergenceError('Kepler solver did not converge')

def true_from_eccentric(E: float, e: float) -> float:
    return 2 * math.atan2(math.sqrt(1 + e) * math.sin(E / 2), math.sqrt(1 - e) * math.cos(E / 2))

def eccentric_from_true(nu: float, e: float) -> float:
    return 2 * math.atan2(math.sqrt(1 - e) * math.sin(nu / 2), math.sqrt(1 + e) * math.cos(nu / 2))
