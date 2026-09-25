from __future__ import annotations
from dataclasses import dataclass
from orbitforge.core.vector import Vec3
from orbitforge.core.state import CartesianState

@dataclass(frozen=True)
class Impulse:
    epoch_tai_s: float
    delta_v_km_s: Vec3

def apply_impulse(state: CartesianState, impulse: Impulse) -> CartesianState:
    if abs(state.epoch_tai_s - impulse.epoch_tai_s) > 1e-06:
        raise ValueError('impulse epoch mismatch')
    return CartesianState(state.epoch_tai_s, state.position_km, state.velocity_km_s + impulse.delta_v_km_s, state.frame)

def propellant_fraction(delta_v_m_s: float, isp_s: float, g0: float=9.80665) -> float:
    import math
    return 1 - math.exp(-delta_v_m_s / (isp_s * g0))
