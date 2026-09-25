from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ReactionWheel:
    inertia_kg_m2: float
    speed_rad_s: float
    max_speed_rad_s: float
    max_torque_nm: float

    @property
    def momentum_nms(self):
        return self.inertia_kg_m2 * self.speed_rad_s

    def apply_torque(self, torque_nm, dt_s):
        if abs(torque_nm) > self.max_torque_nm:
            raise ValueError('wheel torque limit')
        self.speed_rad_s += torque_nm / self.inertia_kg_m2 * dt_s
        saturated = abs(self.speed_rad_s) > self.max_speed_rad_s
        if saturated:
            self.speed_rad_s = max(-self.max_speed_rad_s, min(self.max_speed_rad_s, self.speed_rad_s))
        return saturated

def distribute_body_torque(desired_torque, axis_matrix):
    if len(axis_matrix) != 3:
        raise ValueError('three body-axis rows required')
    wheel_count = len(axis_matrix[0])
    return [sum(axis_matrix[axis][wheel] * desired_torque[axis] for axis in range(3)) for wheel in range(wheel_count)]
