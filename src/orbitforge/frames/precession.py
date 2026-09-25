from __future__ import annotations
import math
from orbitforge.frames.rotations import rz, ry, mm, mv
from orbitforge.core.vector import Vec3

def iau76_precession_matrix(jd_tt: float):
    t = (jd_tt - 2451545.0) / 36525.0
    zeta_arcsec = 2306.2181 * t + 0.30188 * t * t + 0.017998 * t ** 3
    z_arcsec = 2306.2181 * t + 1.09468 * t * t + 0.018203 * t ** 3
    theta_arcsec = 2004.3109 * t - 0.42665 * t * t - 0.041833 * t ** 3
    conv = math.pi / (180.0 * 3600.0)
    zeta = zeta_arcsec * conv
    z = z_arcsec * conv
    theta = theta_arcsec * conv
    return mm(mm(rz(-z), ry(theta)), rz(-zeta))

def precess_j2000_to_date(vector: Vec3, jd_tt: float) -> Vec3:
    return mv(iau76_precession_matrix(jd_tt), vector)

def precess_date_to_j2000(vector: Vec3, jd_tt: float) -> Vec3:
    from orbitforge.frames.rotations import transpose
    return mv(transpose(iau76_precession_matrix(jd_tt)), vector)

def precession_angles_arcsec(jd_tt: float):
    t = (jd_tt - 2451545.0) / 36525.0
    return {'zeta': 2306.2181 * t + 0.30188 * t * t + 0.017998 * t ** 3, 'z': 2306.2181 * t + 1.09468 * t * t + 0.018203 * t ** 3, 'theta': 2004.3109 * t - 0.42665 * t * t - 0.041833 * t ** 3}
