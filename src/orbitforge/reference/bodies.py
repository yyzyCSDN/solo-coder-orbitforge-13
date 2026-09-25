from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Body:
    name: str
    mu_km3_s2: float
    radius_km: float
    rotation_period_s: float
    semi_major_au: float | None = None

BODIES = {
    'Mercury': Body('Mercury', 22031.86855, 2439.7, 5067031.68, 0.387098),
    'Venus': Body('Venus', 324858.592, 6051.8, -20996797.0, 0.723332),
    'Earth': Body('Earth', 398600.4418, 6378.137, 86164.0905, 1.0),
    'Moon': Body('Moon', 4902.800066, 1737.4, 2360591.5, None),
    'Mars': Body('Mars', 42828.375214, 3396.19, 88642.6848, 1.523679),
    'Jupiter': Body('Jupiter', 126686534.9, 71492.0, 35729.7, 5.2044),
    'Saturn': Body('Saturn', 37931187.8, 60268.0, 38362.4, 9.5826),
    'Uranus': Body('Uranus', 5793939.3, 25559.0, -62063.7, 19.2184),
    'Neptune': Body('Neptune', 6836529.0, 24764.0, 57996.0, 30.11),
}

def body(name):
    return BODIES[name]

def sphere_of_influence_km(primary_name, secondary_name, separation_km):
    primary = body(primary_name)
    secondary = body(secondary_name)
    return separation_km * (secondary.mu_km3_s2 / primary.mu_km3_s2) ** (2.0 / 5.0)

def escape_speed_km_s(name, radius_km=None):
    b = body(name)
    r = radius_km or b.radius_km
    return (2.0 * b.mu_km3_s2 / r) ** 0.5
