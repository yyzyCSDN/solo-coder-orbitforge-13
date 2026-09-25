from __future__ import annotations
import math


def saastamoinen_delay_m(elevation_rad: float, pressure_hpa: float = 1013.25, temperature_k: float = 293.15, humidity: float = 0.5):
    el = max(math.radians(2.0), elevation_rad)
    dry = 0.0022768 * pressure_hpa / math.sin(el)
    vapor_pressure = humidity * 6.11 * math.exp(17.15 * (temperature_k - 273.15) / (234.7 + temperature_k - 273.15))
    wet = 0.002277 * (1255.0 / temperature_k + 0.05) * vapor_pressure / math.sin(el)
    return dry + wet

def mapping_function(elevation_rad: float):
    s = math.sin(max(math.radians(1.0), elevation_rad))
    return 1.0 / (s + 0.00143 / (math.tan(max(math.radians(1.0), elevation_rad)) + 0.0445))

def range_delay_km(elevation_rad, pressure_hpa=1013.25, temperature_k=293.15, humidity=0.5):
    return saastamoinen_delay_m(elevation_rad, pressure_hpa, temperature_k, humidity) / 1000.0
