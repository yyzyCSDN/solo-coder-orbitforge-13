from __future__ import annotations
from dataclasses import dataclass
from orbitforge.core.vector import Vec3

@dataclass(frozen=True)
class WheelState:
    momentum_nms: Vec3
    limit_nms: float

def saturation_fraction(state: WheelState):
    return state.momentum_nms.norm() / state.limit_nms

def dump_impulse_required(state: WheelState, target_fraction: float = 0.2):
    if not 0.0 <= target_fraction < 1.0:
        raise ValueError('target fraction')
    current = state.momentum_nms
    norm = current.norm()
    target = state.limit_nms * target_fraction
    if norm <= target:
        return Vec3(0.0, 0.0, 0.0)
    return current.unit() * (norm - target)

def thruster_duration_s(momentum_change_nms, lever_arm_m, thrust_n):
    torque = lever_arm_m * thrust_n
    if torque <= 0.0:
        raise ValueError('positive dump torque')
    return momentum_change_nms.norm() / torque
