from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Material:
    name: str
    density_kg_m3: float
    specific_heat_j_kg_k: float
    conductivity_w_m_k: float
    emissivity: float
    solar_absorptivity: float

MATERIALS = {
    'aluminum_6061': Material('aluminum_6061', 2700.0, 896.0, 167.0, 0.09, 0.35),
    'aluminum_7075': Material('aluminum_7075', 2810.0, 960.0, 130.0, 0.08, 0.34),
    'titanium': Material('titanium', 4500.0, 523.0, 21.9, 0.30, 0.45),
    'cfrp': Material('cfrp', 1600.0, 800.0, 6.0, 0.80, 0.75),
    'kapton': Material('kapton', 1420.0, 1090.0, 0.12, 0.81, 0.35),
    'white_paint': Material('white_paint', 1800.0, 900.0, 0.30, 0.88, 0.20),
    'black_paint': Material('black_paint', 1800.0, 900.0, 0.30, 0.90, 0.90),
}

def material(name):
    return MATERIALS[name]

def areal_heat_capacity(name, thickness_m):
    m = material(name)
    return m.density_kg_m3 * thickness_m * m.specific_heat_j_kg_k

def radiative_property_ratio(name):
    m = material(name)
    return m.solar_absorptivity / m.emissivity
