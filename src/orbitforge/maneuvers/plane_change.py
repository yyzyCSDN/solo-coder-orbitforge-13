from __future__ import annotations
import math

def plane_change_delta_v(speed_km_s: float, delta_i_rad: float) -> float:
    return 2 * speed_km_s * math.sin(abs(delta_i_rad) / 2)

def combined_burn(v_before: float, v_after: float, turn_angle: float) -> float:
    return math.sqrt(v_before * v_before + v_after * v_after - 2 * v_before * v_after * math.cos(turn_angle))

def split_plane_change(v1: float, v2: float, total_angle: float, samples: int=361):
    best = None
    for k in range(samples):
        a = total_angle * k / (samples - 1)
        dv = plane_change_delta_v(v1, a) + plane_change_delta_v(v2, total_angle - a)
        if best is None or dv < best[0]:
            best = (dv, a)
    return {'delta_v': best[0], 'first_angle': best[1], 'second_angle': total_angle - best[1]}
