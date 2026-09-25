from __future__ import annotations

def required_battery_wh(eclipse_duration_s: float, load_w: float, depth_of_discharge: float=0.8, discharge_efficiency: float=0.95):
    if not 0.0 < depth_of_discharge <= 1.0:
        raise ValueError('depth of discharge')
    if not 0.0 < discharge_efficiency <= 1.0:
        raise ValueError('efficiency')
    energy = load_w * eclipse_duration_s / 3600.0
    return energy / (depth_of_discharge * discharge_efficiency)

def recharge_time_s(energy_wh: float, net_charge_w: float, charge_efficiency: float=0.95):
    if net_charge_w <= 0.0:
        return float('inf')
    return energy_wh / (net_charge_w * charge_efficiency) * 3600.0

def cycle_depth(consumed_wh: float, capacity_wh: float):
    return consumed_wh / capacity_wh if capacity_wh > 0.0 else 1.0
