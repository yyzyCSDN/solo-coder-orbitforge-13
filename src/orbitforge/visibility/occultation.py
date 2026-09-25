from __future__ import annotations
import math
from orbitforge.core.vector import Vec3

def segment_sphere_clear(a: Vec3, b: Vec3, radius_km: float):
    d = b - a
    denom = d.norm2()
    if denom < 1e-18:
        return a.norm() > radius_km
    u = max(0.0, min(1.0, -a.dot(d) / denom))
    closest = a + d * u
    return closest.norm() > radius_km

def earth_occulted(observer: Vec3, target: Vec3, radius_km: float=6378.137):
    return not segment_sphere_clear(observer, target, radius_km)

def limb_angle(observer: Vec3, radius_km: float=6378.137):
    if observer.norm() <= radius_km:
        raise ValueError('observer inside body')
    return math.asin(radius_km / observer.norm())
