from __future__ import annotations
import math


def group_delay_m(tec_units: float, frequency_hz: float):
    if frequency_hz <= 0.0:
        raise ValueError('frequency')
    electrons = tec_units * 1e16
    return 40.3 * electrons / (frequency_hz * frequency_hz)

def phase_advance_m(tec_units: float, frequency_hz: float):
    return -group_delay_m(tec_units, frequency_hz)

def slant_tec(vertical_tec: float, elevation_rad: float, shell_height_km: float = 350.0):
    earth_radius = 6378.137
    z = math.pi / 2.0 - elevation_rad
    argument = earth_radius * math.sin(z) / (earth_radius + shell_height_km)
    mapping = 1.0 / math.sqrt(1.0 - argument * argument)
    return vertical_tec * mapping
