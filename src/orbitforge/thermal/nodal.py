from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ThermalNode:
    name: str
    heat_capacity_j_k: float
    temperature_k: float
    internal_w: float = 0.0

def step_nodes(nodes, conductances, environment_k: float, radiation_coefficients, dt_s: float):
    rates = {n.name: n.internal_w for n in nodes}
    by_name = {n.name: n for n in nodes}
    for a, b, g in conductances:
        q = g * (by_name[b].temperature_k - by_name[a].temperature_k)
        rates[a] += q
        rates[b] -= q
    for name, coeff in radiation_coefficients.items():
        node = by_name[name]
        rates[name] += coeff * (environment_k ** 4 - node.temperature_k ** 4)
    for node in nodes:
        node.temperature_k += rates[node.name] * dt_s / node.heat_capacity_j_k
    return {n.name: n.temperature_k for n in nodes}

def thermal_limits(nodes, limits):
    return {n.name: limits[n.name][0] <= n.temperature_k <= limits[n.name][1] for n in nodes if n.name in limits}
