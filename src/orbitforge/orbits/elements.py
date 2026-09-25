from __future__ import annotations
from dataclasses import dataclass
import math
from orbitforge.core.vector import Vec3
from orbitforge.core.constants import MU_EARTH_KM3_S2

@dataclass(frozen=True)
class KeplerianElements:
    a_km: float
    e: float
    i_rad: float
    raan_rad: float
    argp_rad: float
    nu_rad: float

def state_to_elements(r: Vec3, v: Vec3, mu: float=MU_EARTH_KM3_S2) -> KeplerianElements:
    h = r.cross(v)
    n = Vec3(-h.y, h.x, 0)
    evec = v.cross(h) / mu - r / r.norm()
    e = evec.norm()
    energy = v.norm2() / 2 - mu / r.norm()
    a = -mu / (2 * energy)
    i = math.acos(max(-1, min(1, h.z / h.norm())))
    raan = math.atan2(n.y, n.x) % (2 * math.pi) if n.norm() > 1e-12 else 0.0
    argp = math.acos(max(-1, min(1, n.dot(evec) / (n.norm() * e)))) if n.norm() > 1e-12 and e > 1e-12 else 0.0
    if evec.z < 0:
        argp = 2 * math.pi - argp
    nu = math.acos(max(-1, min(1, evec.dot(r) / (e * r.norm())))) if e > 1e-12 else math.atan2(r.y, r.x) % (2 * math.pi)
    if r.dot(v) < 0 and e > 1e-12:
        nu = 2 * math.pi - nu
    return KeplerianElements(a, e, i, raan, argp, nu)

def elements_to_state(el: KeplerianElements, mu: float=MU_EARTH_KM3_S2):
    p = el.a_km * (1 - el.e * el.e)
    c = math.cos(el.nu_rad)
    s = math.sin(el.nu_rad)
    rp = Vec3(p * c / (1 + el.e * c), p * s / (1 + el.e * c), 0)
    k = math.sqrt(mu / p)
    vp = Vec3(-k * s, k * (el.e + c), 0)
    from orbitforge.frames.rotations import rz, rx, mv, mm
    q = mm(mm(rz(el.raan_rad), rx(el.i_rad)), rz(el.argp_rad))
    return (mv(q, rp), mv(q, vp))
