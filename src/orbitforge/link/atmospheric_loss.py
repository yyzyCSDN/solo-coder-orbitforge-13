from __future__ import annotations
import math

def gaseous_loss_db(freq_ghz, elevation_rad, humidity=0.5):
    sec = 1 / max(0.1, math.sin(max(elevation_rad, math.radians(1))))
    oxygen = 0.006 * freq_ghz * sec
    water = 0.002 * freq_ghz * freq_ghz * humidity * sec
    return oxygen + water

def rain_loss_db(freq_ghz, rain_rate_mm_h, elevation_rad, path_km=2.0):
    k = 0.0001 * freq_ghz ** 1.3
    gamma = k * rain_rate_mm_h ** 0.9
    return gamma * path_km / max(0.2, math.sin(elevation_rad))
