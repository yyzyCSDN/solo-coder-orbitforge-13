from __future__ import annotations
import math


def slot_phase_error(current_rad, target_rad):
    return (target_rad - current_rad + math.pi) % (2.0 * math.pi) - math.pi


def assign_slots(current_phases, target_phases):
    remaining = set(range(len(target_phases)))
    assignment = []
    for i, current in enumerate(current_phases):
        best = min(remaining, key=lambda j: abs(slot_phase_error(current, target_phases[j])))
        assignment.append((i, best, slot_phase_error(current, target_phases[best])))
        remaining.remove(best)
    return assignment


def rephasing_cost(assignment, mean_motion_rad_s, reference_speed_km_s):
    total = 0.0
    for _, _, phase_error in assignment:
        fractional_period = abs(phase_error) / (2.0 * math.pi)
        total += 2.0 * reference_speed_km_s * fractional_period * 0.01
    return total


def worst_phase_error(assignment):
    return max((abs(row[2]) for row in assignment), default=0.0)
