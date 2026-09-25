from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class BiasEstimate:
    station: str
    range_bias_km: float
    doppler_bias_hz: float
    sample_count: int

def estimate_bias(station, range_residuals, doppler_residuals):
    if not range_residuals and not doppler_residuals:
        raise ValueError('no calibration residuals')
    range_bias = sum(range_residuals) / len(range_residuals) if range_residuals else 0.0
    doppler_bias = sum(doppler_residuals) / len(doppler_residuals) if doppler_residuals else 0.0
    return BiasEstimate(station, range_bias, doppler_bias, max(len(range_residuals), len(doppler_residuals)))

def apply_range_bias(measured_km, estimate):
    return measured_km - estimate.range_bias_km

def apply_doppler_bias(measured_hz, estimate):
    return measured_hz - estimate.doppler_bias_hz

def drift_between(old, new, days):
    if days <= 0.0:
        raise ValueError('positive interval required')
    return {
        'range_km_per_day': (new.range_bias_km - old.range_bias_km) / days,
        'doppler_hz_per_day': (new.doppler_bias_hz - old.doppler_bias_hz) / days,
    }
