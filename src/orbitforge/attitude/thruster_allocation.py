from __future__ import annotations
from dataclasses import dataclass
from orbitforge.core.vector import Vec3

@dataclass(frozen=True)
class Thruster:
    name: str
    direction: Vec3
    location_m: Vec3
    max_thrust_n: float

def torque_per_newton(thruster: Thruster):
    return thruster.location_m.cross(thruster.direction.unit())

def greedy_allocate(desired_torque: Vec3, thrusters):
    remaining = desired_torque
    commands = []
    for thruster in sorted(thrusters, key=lambda t: -abs(torque_per_newton(t).dot(remaining))):
        axis = torque_per_newton(thruster)
        norm2 = axis.norm2()
        if norm2 < 1e-12:
            continue
        thrust = max(0.0, min(thruster.max_thrust_n, remaining.dot(axis) / norm2))
        if thrust > 0.0:
            commands.append((thruster.name, thrust))
            remaining = remaining - axis * thrust
    return commands, remaining

def total_thrust(commands):
    return sum(value for _, value in commands)
