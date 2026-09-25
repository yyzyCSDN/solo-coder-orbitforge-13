from __future__ import annotations
from orbitforge.core.state import CartesianState
from orbitforge.core.vector import Vec3
from .perturbations import gravity_j2

def _deriv(r: Vec3, v: Vec3):
    return (v, gravity_j2(r))

def propagate_cowell(state: CartesianState, dt_s: float, step_s: float=20.0) -> CartesianState:
    r, v = (state.position_km, state.velocity_km_s)
    remain = dt_s
    sign = 1 if remain >= 0 else -1
    h = abs(step_s) * sign
    while abs(remain) > 1e-12:
        if abs(h) > abs(remain):
            h = remain
        k1r, k1v = _deriv(r, v)
        k2r, k2v = _deriv(r + k1r * (h / 2), v + k1v * (h / 2))
        k3r, k3v = _deriv(r + k2r * (h / 2), v + k2v * (h / 2))
        k4r, k4v = _deriv(r + k3r * h, v + k3v * h)
        r = r + (k1r + k2r * 2 + k3r * 2 + k4r) * (h / 6)
        v = v + (k1v + k2v * 2 + k3v * 2 + k4v) * (h / 6)
        remain -= h
    return CartesianState(state.epoch_tai_s + dt_s, r, v, state.frame)
