from __future__ import annotations
import math

def dish_gain_dbi(diameter_m: float, freq_hz: float, efficiency: float=0.6):
    lam = 299792458.0 / freq_hz
    return 10 * math.log10(efficiency * (math.pi * diameter_m / lam) ** 2)

def beamwidth_deg(diameter_m: float, freq_hz: float):
    lam = 299792458.0 / freq_hz
    return 70 * lam / diameter_m

def pointing_loss_db(error_deg: float, half_power_beamwidth_deg: float):
    if half_power_beamwidth_deg <= 0:
        raise ValueError('beamwidth')
    return 12 * (error_deg / half_power_beamwidth_deg) ** 2
