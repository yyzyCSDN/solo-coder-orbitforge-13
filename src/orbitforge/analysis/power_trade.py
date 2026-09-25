from __future__ import annotations

def array_area_for_energy(load_wh_day, sunlight_fraction, efficiency, degradation, solar_constant=1361.0):
    available_hours = 24.0 * sunlight_fraction
    if available_hours <= 0.0 or efficiency <= 0.0 or degradation <= 0.0:
        return float('inf')
    average_required_w = load_wh_day / available_hours
    return average_required_w / (solar_constant * efficiency * degradation)

def battery_mass_for_eclipse(load_w, eclipse_s, specific_energy_wh_kg, depth_of_discharge=0.8):
    energy_wh = load_w * eclipse_s / 3600.0 / depth_of_discharge
    return energy_wh / specific_energy_wh_kg

def rank_options(options):
    return sorted(options, key=lambda row: (row['mass_kg'], row.get('cost', 0.0)))
