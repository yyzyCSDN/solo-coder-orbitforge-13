from __future__ import annotations
import math
from orbitforge.core.vector import Vec3
from orbitforge.core.constants import MU_EARTH_KM3_S2
from orbitforge.core.errors import ConvergenceError

def stumpff_c(z: float) -> float:
    if z > 1e-08:
        q = math.sqrt(z)
        return (1.0 - math.cos(q)) / z
    if z < -1e-08:
        q = math.sqrt(-z)
        return (math.cosh(q) - 1.0) / -z
    return 0.5 - z / 24.0 + z * z / 720.0

def stumpff_s(z: float) -> float:
    if z > 1e-08:
        q = math.sqrt(z)
        return (q - math.sin(q)) / q ** 3
    if z < -1e-08:
        q = math.sqrt(-z)
        return (math.sinh(q) - q) / q ** 3
    return 1.0 / 6.0 - z / 120.0 + z * z / 5040.0

def propagate_universal(r0: Vec3, v0: Vec3, dt_s: float, mu: float=MU_EARTH_KM3_S2):
    r0n = r0.norm()
    vr0 = r0.dot(v0) / r0n
    alpha = 2.0 / r0n - v0.norm2() / mu
    chi = math.sqrt(mu) * abs(alpha) * dt_s if abs(alpha) > 1e-10 else math.sqrt(mu) * dt_s / r0n
    for _ in range(80):
        z = alpha * chi * chi
        c = stumpff_c(z)
        s = stumpff_s(z)
        f = r0n * vr0 / math.sqrt(mu) * chi * chi * c + (1.0 - alpha * r0n) * chi ** 3 * s + r0n * chi - math.sqrt(mu) * dt_s
        fp = r0n * vr0 / math.sqrt(mu) * chi * (1.0 - z * s) + (1.0 - alpha * r0n) * chi * chi * c + r0n
        step = f / fp
        chi -= step
        if abs(step) < 1e-10:
            break
    else:
        raise ConvergenceError('universal variable iteration failed')
    z = alpha * chi * chi
    c = stumpff_c(z)
    s = stumpff_s(z)
    fcoef = 1.0 - chi * chi / r0n * c
    gcoef = dt_s - chi ** 3 / math.sqrt(mu) * s
    r = r0 * fcoef + v0 * gcoef
    rn = r.norm()
    fdot = math.sqrt(mu) / (rn * r0n) * (alpha * chi ** 3 * s - chi)
    gdot = 1.0 - chi * chi / rn * c
    v = r0 * fdot + v0 * gdot
    return (r, v)
