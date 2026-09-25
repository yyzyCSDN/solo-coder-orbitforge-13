from __future__ import annotations
import math


def ideal_orbital_speed(mu_km3_s2, radius_km):
    return math.sqrt(mu_km3_s2 / radius_km)


def delta_v_budget(target_speed_km_s, rotation_bonus_km_s, gravity_loss_km_s=1.5, drag_loss_km_s=0.2, steering_loss_km_s=0.1):
    required = target_speed_km_s - rotation_bonus_km_s + gravity_loss_km_s + drag_loss_km_s + steering_loss_km_s
    return {
        'target_speed_km_s': target_speed_km_s,
        'rotation_bonus_km_s': rotation_bonus_km_s,
        'gravity_loss_km_s': gravity_loss_km_s,
        'drag_loss_km_s': drag_loss_km_s,
        'steering_loss_km_s': steering_loss_km_s,
        'required_delta_v_km_s': required,
    }


def payload_margin(vehicle_delta_v_km_s, budget):
    return vehicle_delta_v_km_s - budget['required_delta_v_km_s']
