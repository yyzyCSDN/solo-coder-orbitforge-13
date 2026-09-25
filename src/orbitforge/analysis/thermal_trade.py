from __future__ import annotations

def radiator_mass(area_m2, areal_density_kg_m2):
    return area_m2 * areal_density_kg_m2

def heater_energy_wh(power_w, duty_cycle, duration_h):
    return power_w * duty_cycle * duration_h

def trade(options, maximum_mass_kg, maximum_heater_wh):
    feasible = []
    for option in options:
        if option['radiator_mass_kg'] <= maximum_mass_kg and option['heater_energy_wh'] <= maximum_heater_wh:
            feasible.append(option)
    return sorted(feasible, key=lambda row: (row['radiator_mass_kg'], row['heater_energy_wh']))
