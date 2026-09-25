from __future__ import annotations
import math
from orbitforge.core.vector import Vec3
from orbitforge.core.constants import MU_EARTH_KM3_S2
from orbitforge.core.errors import NoSolutionError

def _stumpff_c(z):
    if z > 1e-08:
        return (1 - math.cos(math.sqrt(z))) / z
    if z < -1e-08:
        return (math.cosh(math.sqrt(-z)) - 1) / -z
    return 0.5 - z / 24 + z * z / 720

def _stumpff_s(z):
    if z > 1e-08:
        return (math.sqrt(z) - math.sin(math.sqrt(z))) / z ** 1.5
    if z < -1e-08:
        return (math.sinh(math.sqrt(-z)) - math.sqrt(-z)) / (-z) ** 1.5
    return 1 / 6 - z / 120 + z * z / 5040

def lambert_universal(r1: Vec3, r2: Vec3, dt: float, mu: float=MU_EARTH_KM3_S2, prograde: bool=True):
    r1n, r2n = (r1.norm(), r2.norm())
    cosd = max(-1, min(1, r1.dot(r2) / (r1n * r2n)))
    dtheta = math.acos(cosd)
    if prograde and r1.cross(r2).z < 0:
        dtheta = 2 * math.pi - dtheta
    if not prograde and r1.cross(r2).z >= 0:
        dtheta = 2 * math.pi - dtheta
    A = math.sin(dtheta) * math.sqrt(r1n * r2n / (1 - math.cos(dtheta)))
    if abs(A) < 1e-12:
        raise NoSolutionError('degenerate geometry')
    z = 0.0
    for _ in range(100):
        c = _stumpff_c(z)
        s = _stumpff_s(z)
        if c <= 0:
            z += 0.1
            continue
        y = r1n + r2n + A * (z * s - 1) / math.sqrt(c)
        if y < 0:
            z += 0.1
            continue
        x = math.sqrt(y / c)
        t = (x ** 3 * s + A * math.sqrt(y)) / math.sqrt(mu)
        err = t - dt
        if abs(err) < 1e-06:
            break
        dz = 1e-05
        cp = _stumpff_c(z + dz)
        sp = _stumpff_s(z + dz)
        yp = r1n + r2n + A * ((z + dz) * sp - 1) / math.sqrt(cp)
        xp = math.sqrt(max(0, yp / cp))
        tp = (xp ** 3 * sp + A * math.sqrt(max(0, yp))) / math.sqrt(mu)
        deriv = (tp - t) / dz
        if abs(deriv) < 1e-12:
            z += 0.05 if err < 0 else -0.05
        else:
            z -= err / deriv
    else:
        raise NoSolutionError('Lambert did not converge')
    f = 1 - y / r1n
    g = A * math.sqrt(y / mu)
    gd = 1 - y / r2n
    return ((r2 - r1 * f) / g, (r2 * gd - r1) / g)
