from __future__ import annotations
import math
from orbitforge.core.state import CartesianState
from orbitforge.core.constants import MU_EARTH_KM3_S2
from .elements import state_to_elements, elements_to_state, KeplerianElements
from .kepler import solve_kepler_elliptic, true_from_eccentric, eccentric_from_true

def propagate_two_body(state: CartesianState, dt_s: float, mu: float=MU_EARTH_KM3_S2) -> CartesianState:
    el = state_to_elements(state.position_km, state.velocity_km_s, mu)
    if el.e >= 1:
        raise ValueError('elliptic only')
    E0 = eccentric_from_true(el.nu_rad, el.e)
    M0 = E0 - el.e * math.sin(E0)
    n = math.sqrt(mu / el.a_km ** 3)
    E = solve_kepler_elliptic(M0 + n * dt_s, el.e)
    nu = true_from_eccentric(E, el.e)
    r, v = elements_to_state(KeplerianElements(el.a_km, el.e, el.i_rad, el.raan_rad, el.argp_rad, nu), mu)
    return CartesianState(state.epoch_tai_s + dt_s, r, v, state.frame)
