from __future__ import annotations
from dataclasses import dataclass
from orbitforge.core.vector import Vec3
from orbitforge.core.constants import C_KM_S

@dataclass(frozen=True)
class DopplerMeasurement:
    epoch_tai_s: float
    frequency_hz: float
    observed_shift_hz: float
    sigma_hz: float

def predicted_one_way_shift(frequency_hz: float, relative_position: Vec3, relative_velocity: Vec3):
    line = relative_position.unit()
    range_rate = relative_velocity.dot(line)
    return -frequency_hz * range_rate / C_KM_S

def residual(measurement: DopplerMeasurement, relative_position: Vec3, relative_velocity: Vec3):
    return measurement.observed_shift_hz - predicted_one_way_shift(measurement.frequency_hz, relative_position, relative_velocity)

def normalized_residual(measurement, relative_position, relative_velocity):
    if measurement.sigma_hz <= 0.0:
        raise ValueError('positive Doppler sigma required')
    return residual(measurement, relative_position, relative_velocity) / measurement.sigma_hz

def estimate_range_rate(frequency_hz: float, shift_hz: float):
    if frequency_hz <= 0.0:
        raise ValueError('positive carrier required')
    return -shift_hz * C_KM_S / frequency_hz
