from __future__ import annotations
from dataclasses import dataclass

@dataclass
class BatteryState:
    capacity_wh: float
    energy_wh: float
    charge_efficiency: float = 0.95
    discharge_efficiency: float = 0.95

    @property
    def soc(self):
        return max(0.0, min(1.0, self.energy_wh / self.capacity_wh))

    def step(self, generation_w: float, load_w: float, dt_s: float):
        net = generation_w - load_w
        delta = (net * self.charge_efficiency if net >= 0 else net / self.discharge_efficiency) * dt_s / 3600
        self.energy_wh = max(0.0, min(self.capacity_wh, self.energy_wh + delta))
        return self.soc

def eclipse_margin_wh(state: BatteryState, eclipse_s: float, load_w: float):
    return state.energy_wh - load_w * eclipse_s / 3600 / state.discharge_efficiency
