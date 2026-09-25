from __future__ import annotations
import math
from orbitforge.core.vector import Vec3

def cwh_targeting(initial_r: Vec3, target_r: Vec3, mean_motion_rad_s: float, tof_s: float):
    n = mean_motion_rad_s
    nt = n * tof_s
    c = math.cos(nt)
    s = math.sin(nt)
    a11 = s / n
    a12 = 2.0 * (1.0 - c) / n
    a21 = -2.0 * (1.0 - c) / n
    a22 = (4.0 * s - 3.0 * nt) / n
    bx = target_r.x - (4.0 - 3.0 * c) * initial_r.x
    by = target_r.y - (6.0 * (s - nt) * initial_r.x + initial_r.y)
    det = a11 * a22 - a12 * a21
    if abs(det) < 1e-12:
        raise ValueError('singular rendezvous transfer')
    vx = (bx * a22 - a12 * by) / det
    vy = (a11 * by - bx * a21) / det
    vz = n * (target_r.z - c * initial_r.z) / s if abs(s) > 1e-12 else 0.0
    return Vec3(vx, vy, vz)
