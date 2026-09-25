from __future__ import annotations
import math

def noise_temperature_from_figure_db(noise_figure_db: float, reference_k: float=290.0):
    factor = 10.0 ** (noise_figure_db / 10.0)
    return reference_k * (factor - 1.0)

def cascaded_noise_temperature(stages):
    total = 0.0
    gain_product = 1.0
    for gain_db, noise_temp_k in stages:
        total += noise_temp_k / gain_product
        gain_product *= 10.0 ** (gain_db / 10.0)
    return total

def gt_db_per_k(gain_dbi: float, system_temp_k: float):
    if system_temp_k <= 0.0:
        raise ValueError('system temperature')
    return gain_dbi - 10.0 * math.log10(system_temp_k)
