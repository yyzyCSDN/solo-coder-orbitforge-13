from __future__ import annotations
from orbitforge.core.constants import C_KM_S

def doppler_shift_hz(freq_hz: float, range_rate_km_s: float) -> float:
    return -freq_hz * range_rate_km_s / C_KM_S

def observed_frequency(freq_hz: float, range_rate_km_s: float) -> float:
    return freq_hz + doppler_shift_hz(freq_hz, range_rate_km_s)

def coherent_two_way_shift(freq_hz: float, range_rate_km_s: float, turnaround_ratio: float=1.0) -> float:
    return 2 * doppler_shift_hz(freq_hz, range_rate_km_s) * turnaround_ratio
