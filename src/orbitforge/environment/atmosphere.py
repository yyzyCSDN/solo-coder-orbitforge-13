from __future__ import annotations
import math
TABLE = ((0, 1.225), (25, 0.03899), (50, 0.001027), (75, 3.206e-05), (100, 5.297e-07), (150, 2.07e-09), (200, 2.789e-10), (300, 1.916e-11), (400, 2.803e-12), (500, 5.215e-13), (600, 1.137e-13), (700, 3.614e-14), (800, 1.17e-14), (900, 5.245e-15), (1000, 3.019e-15))

def density_kg_m3(alt_km):
    if alt_km <= TABLE[0][0]:
        return TABLE[0][1]
    for (h0, r0), (h1, r1) in zip(TABLE, TABLE[1:]):
        if h0 <= alt_km <= h1:
            u = (alt_km - h0) / (h1 - h0)
            return math.exp(math.log(r0) * (1 - u) + math.log(r1) * u)
    return TABLE[-1][1] * math.exp(-(alt_km - TABLE[-1][0]) / 200)

def ballistic_coefficient(mass_kg, cd, area_m2):
    return mass_kg / (cd * area_m2)
