from __future__ import annotations
import math


def linear_mismatch_loss_db(angle_rad):
    gain = math.cos(angle_rad) ** 2
    if gain <= 1e-15:
        return float('inf')
    return -10.0 * math.log10(gain)

def axial_ratio_loss_db(axial_ratio_db):
    ratio = 10.0 ** (axial_ratio_db / 20.0)
    efficiency = 4.0 * ratio / ((ratio + 1.0) ** 2)
    return -10.0 * math.log10(efficiency)

def total_polarization_loss_db(linear_angle_rad=None, axial_ratio_db=None):
    loss = 0.0
    if linear_angle_rad is not None:
        loss += linear_mismatch_loss_db(linear_angle_rad)
    if axial_ratio_db is not None:
        loss += axial_ratio_loss_db(axial_ratio_db)
    return loss
