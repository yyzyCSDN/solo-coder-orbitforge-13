from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ClockModel:
    bias_s: float = 0.0
    drift_s_per_s: float = 0.0
    drift_rate_s_per_s2: float = 0.0

    def offset(self, dt_s: float) -> float:
        return self.bias_s + self.drift_s_per_s * dt_s + 0.5 * self.drift_rate_s_per_s2 * dt_s * dt_s

    def advance(self, dt_s: float):
        self.bias_s = self.offset(dt_s)
        self.drift_s_per_s += self.drift_rate_s_per_s2 * dt_s
        return self.bias_s


def two_way_range_clock_error(transmit_clock: ClockModel, receive_clock: ClockModel, epoch_from_reference_s: float):
    tx = transmit_clock.offset(epoch_from_reference_s)
    rx = receive_clock.offset(epoch_from_reference_s)
    return 0.5 * (rx - tx) * 299792.458


def fit_linear_clock(samples):
    if len(samples) < 2:
        raise ValueError('two clock samples required')
    n = len(samples)
    mean_t = sum(t for t, _ in samples) / n
    mean_y = sum(y for _, y in samples) / n
    denom = sum((t - mean_t) ** 2 for t, _ in samples)
    drift = sum((t - mean_t) * (y - mean_y) for t, y in samples) / denom
    bias = mean_y - drift * mean_t
    return ClockModel(bias, drift, 0.0)
