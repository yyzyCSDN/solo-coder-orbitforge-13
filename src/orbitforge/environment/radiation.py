from __future__ import annotations
import math

def trapped_flux_proxy(alt_km, inclination_rad):
    return max(0.0, (alt_km - 200) / 1800) * (1 + 1.5 * math.sin(inclination_rad) ** 2)

def dose_krad(flux_proxy, shield_mm_al, days):
    return flux_proxy * days * 0.002 * math.exp(-shield_mm_al / 2.5)

def see_rate_per_day(flux_proxy, device_cross_section_cm2):
    return flux_proxy * 1000000.0 * device_cross_section_cm2 * 86400
