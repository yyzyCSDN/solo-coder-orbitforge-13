from __future__ import annotations
import math
SIGMA = 5.670374419e-08

def equilibrium_temp_k(absorbed_w, area_m2, emissivity):
    return (absorbed_w / (SIGMA * area_m2 * emissivity)) ** 0.25

def radiator_area_m2(waste_heat_w, temp_k, emissivity=0.85):
    return waste_heat_w / (SIGMA * emissivity * temp_k ** 4)
