from __future__ import annotations
import math

def bang_bang_slew_time(angle_rad, max_rate_rad_s, max_accel_rad_s2):
    if angle_rad < 0:
        angle_rad = abs(angle_rad)
    switch = max_rate_rad_s * max_rate_rad_s / max_accel_rad_s2
    if angle_rad <= switch:
        return 2 * math.sqrt(angle_rad / max_accel_rad_s2)
    return 2 * max_rate_rad_s / max_accel_rad_s2 + (angle_rad - switch) / max_rate_rad_s

def wheel_momentum_change(inertia_kg_m2, delta_rate_rad_s):
    return inertia_kg_m2 * delta_rate_rad_s
