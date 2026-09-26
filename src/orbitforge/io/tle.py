from __future__ import annotations
# Metadata-only TLE helper. SGP4 ingestion and propagation use orbitforge.tle
# with the official SGP4 package; do not wire this parser to a two-body/J2 model.
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class TLERecord:
    name: str
    satellite_number: int
    epoch_year: int
    epoch_day: float
    inclination_rad: float
    raan_rad: float
    eccentricity: float
    argp_rad: float
    mean_anomaly_rad: float
    mean_motion_rev_day: float

def parse(name, line1, line2):
    if not line1.startswith('1 ') or not line2.startswith('2 '):
        raise ValueError('invalid TLE line numbers')
    sat1 = int(line1[2:7])
    sat2 = int(line2[2:7])
    if sat1 != sat2:
        raise ValueError('TLE satellite numbers disagree')
    year2 = int(line1[18:20])
    year = 1900 + year2 if year2 >= 57 else 2000 + year2
    day = float(line1[20:32])
    return TLERecord(
        name.strip(),
        sat1,
        year,
        day,
        math.radians(float(line2[8:16])),
        math.radians(float(line2[17:25])),
        float('.' + line2[26:33].strip()),
        math.radians(float(line2[34:42])),
        math.radians(float(line2[43:51])),
        float(line2[52:63]),
    )

def orbital_period_s(record):
    return 86400.0 / record.mean_motion_rev_day

def age_days(record, year, day):
    return (year - record.epoch_year) * 365.25 + (day - record.epoch_day)
