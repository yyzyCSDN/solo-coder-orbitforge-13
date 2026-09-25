from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Calibration:
    station: str
    valid_from: float
    valid_to: float
    range_delay_s: float
    frequency_offset_hz: float


def select(calibrations, station, epoch):
    matches = [c for c in calibrations if c.station == station and c.valid_from <= epoch < c.valid_to]
    if len(matches) > 1:
        raise ValueError('overlapping station calibrations')
    return matches[0] if matches else None

def validate(calibrations):
    issues = []
    by_station = {}
    for calibration in calibrations:
        by_station.setdefault(calibration.station, []).append(calibration)
    for station, items in by_station.items():
        ordered = sorted(items, key=lambda c: c.valid_from)
        for item in ordered:
            if item.valid_to <= item.valid_from:
                issues.append((station, 'invalid_window', item))
        for a, b in zip(ordered, ordered[1:]):
            if b.valid_from < a.valid_to:
                issues.append((station, 'overlap', (a, b)))
    return issues

def apply_range_delay(range_km, calibration):
    return range_km - calibration.range_delay_s * 299792.458
