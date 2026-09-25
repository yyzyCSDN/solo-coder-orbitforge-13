from __future__ import annotations
import math
from orbitforge.core.constants import G0_M_S2


def propellant_mass(wet_mass_kg, delta_v_m_s, isp_s):
    ratio = math.exp(delta_v_m_s / (isp_s * G0_M_S2))
    return wet_mass_kg * (1.0 - 1.0 / ratio)

def evaluate(option, wet_mass_kg, delta_v_m_s):
    propellant = propellant_mass(wet_mass_kg, delta_v_m_s, option['isp_s'])
    dry_system_mass = option.get('dry_mass_kg', 0.0)
    tank_factor = option.get('tank_fraction', 0.1)
    tank_mass = propellant * tank_factor
    total_penalty = propellant + dry_system_mass + tank_mass
    return {
        **option,
        'propellant_kg': propellant,
        'tank_mass_kg': tank_mass,
        'mass_penalty_kg': total_penalty,
    }

def rank(options, wet_mass_kg, delta_v_m_s):
    return sorted((evaluate(option, wet_mass_kg, delta_v_m_s) for option in options), key=lambda row: row['mass_penalty_kg'])
