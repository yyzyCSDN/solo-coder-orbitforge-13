from __future__ import annotations
from dataclasses import dataclass
import math
from orbitforge.core.constants import G0_M_S2

@dataclass(frozen=True)
class Engine:
    thrust_n: float
    isp_s: float
    min_throttle: float = 0.0
    max_throttle: float = 1.0

def mass_after_burn(initial_mass_kg: float, engine: Engine, duration_s: float, throttle: float=1.0):
    if not engine.min_throttle <= throttle <= engine.max_throttle:
        raise ValueError('throttle outside engine limits')
    mdot = engine.thrust_n * throttle / (engine.isp_s * G0_M_S2)
    final = initial_mass_kg - mdot * duration_s
    if final <= 0.0:
        raise ValueError('burn exhausts spacecraft mass')
    return final

def ideal_delta_v_m_s(initial_mass_kg: float, final_mass_kg: float, isp_s: float):
    if not 0.0 < final_mass_kg <= initial_mass_kg:
        raise ValueError('invalid mass pair')
    return isp_s * G0_M_S2 * math.log(initial_mass_kg / final_mass_kg)

def burn_duration_for_delta_v(initial_mass_kg: float, engine: Engine, delta_v_m_s: float, throttle: float=1.0):
    final_mass = initial_mass_kg / math.exp(delta_v_m_s / (engine.isp_s * G0_M_S2))
    mdot = engine.thrust_n * throttle / (engine.isp_s * G0_M_S2)
    return (initial_mass_kg - final_mass) / mdot
