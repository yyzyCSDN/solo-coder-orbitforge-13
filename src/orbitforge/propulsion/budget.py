from __future__ import annotations
import math
from orbitforge.core.constants import G0_M_S2


def propellant_required(initial_mass_kg, delta_v_m_s, isp_s):
    mass_ratio = math.exp(delta_v_m_s / (isp_s * G0_M_S2))
    final_mass = initial_mass_kg / mass_ratio
    return initial_mass_kg - final_mass


def sequential_budget(initial_mass_kg, maneuvers, reserve_fraction=0.0):
    mass = initial_mass_kg
    rows = []
    for name, delta_v_m_s, isp_s in maneuvers:
        propellant = propellant_required(mass, delta_v_m_s, isp_s)
        mass -= propellant
        rows.append({'name': name, 'delta_v_m_s': delta_v_m_s, 'propellant_kg': propellant, 'mass_after_kg': mass})
    reserve = initial_mass_kg * reserve_fraction
    return {'rows': rows, 'final_mass_kg': mass, 'reserve_kg': reserve, 'reserve_ok': mass >= reserve}


def delta_v_margin(planned_delta_v_m_s, available_propellant_kg, wet_mass_kg, isp_s):
    dry = wet_mass_kg - available_propellant_kg
    if dry <= 0.0:
        raise ValueError('invalid dry mass')
    available = isp_s * G0_M_S2 * math.log(wet_mass_kg / dry)
    return available - planned_delta_v_m_s
