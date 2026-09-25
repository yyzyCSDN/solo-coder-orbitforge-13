from __future__ import annotations
from dataclasses import dataclass

@dataclass
class PropellantTank:
    capacity_kg: float
    propellant_kg: float
    residual_fraction: float = 0.02

    @property
    def usable_kg(self):
        reserve = self.capacity_kg * self.residual_fraction
        return max(0.0, self.propellant_kg - reserve)

    def consume(self, amount_kg: float):
        if amount_kg < 0.0:
            raise ValueError('negative consumption')
        if amount_kg > self.usable_kg + 1e-12:
            raise ValueError('insufficient usable propellant')
        self.propellant_kg -= amount_kg
        return self.propellant_kg


def center_of_mass(dry_mass_kg, dry_com_m, tank_masses):
    total = dry_mass_kg + sum(m for m, _ in tank_masses)
    if total <= 0.0:
        raise ValueError('mass must be positive')
    moment = [dry_mass_kg * dry_com_m[i] for i in range(3)]
    for mass, location in tank_masses:
        for i in range(3):
            moment[i] += mass * location[i]
    return tuple(x / total for x in moment)
