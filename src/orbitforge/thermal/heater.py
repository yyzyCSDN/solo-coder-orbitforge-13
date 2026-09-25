from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Thermostat:
    on_below_k: float
    off_above_k: float
    heater_w: float
    enabled: bool = False

    def update(self, temperature_k: float):
        if self.enabled and temperature_k >= self.off_above_k:
            self.enabled = False
        elif not self.enabled and temperature_k <= self.on_below_k:
            self.enabled = True
        return self.enabled


def simulate_heater(node_temperature_k, heat_capacity_j_k, thermostat, environment_k, conductance_w_k, dt_s, steps):
    history = []
    temp = node_temperature_k
    for _ in range(steps):
        enabled = thermostat.update(temp)
        heater = thermostat.heater_w if enabled else 0.0
        q = conductance_w_k * (environment_k - temp) + heater
        temp += q * dt_s / heat_capacity_j_k
        history.append((temp, enabled))
    return history
