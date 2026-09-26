from __future__ import annotations
from dataclasses import dataclass
import datetime as dt
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
    classification: str = 'U'
    intl_designator: str = ''
    mean_motion_dot_rev_day2: float = 0.0
    mean_motion_ddot_rev_day3: float = 0.0
    bstar_inv_earth_radii: float = 0.0
    ephemeris_type: int = 0
    element_set_number: int = 0
    rev_number: int = 0

def _implied_decimal(field: str) -> float:
    """Parse TLE implied-decimal fields like ' 28098-4' -> 0.28098e-4."""
    field = field.strip()
    if not field:
        return 0.0
    sign = -1.0 if field[0] == '-' else 1.0
    body = field.lstrip('+-')
    if len(body) >= 3 and body[-2] in '+-':
        mantissa, exponent = body[:-2], body[-2:]
    else:
        mantissa, exponent = body, '+0'
    mantissa = mantissa.strip()
    if not mantissa:
        return 0.0
    return sign * float('0.' + mantissa) * 10.0 ** int(exponent)

def checksum_ok(line: str) -> bool:
    """TLE checksum: column 69 holds (sum of digits + 1 per '-') mod 10."""
    if len(line) != 69:
        return False
    if not line[68].isdigit():
        return False
    total = 0
    for ch in line[:68]:
        if ch.isdigit():
            total += int(ch)
        elif ch == '-':
            total += 1
    return total % 10 == int(line[68])

def parse(name, line1, line2, validate_checksum=True):
    line1 = line1.rstrip('\r\n')
    line2 = line2.rstrip('\r\n')
    if not line1.startswith('1 ') or not line2.startswith('2 '):
        raise ValueError('invalid TLE line numbers')
    if len(line1) != 69 or len(line2) != 69:
        raise ValueError(f'TLE lines must be 69 characters, got {len(line1)} and {len(line2)}')
    if validate_checksum:
        if not checksum_ok(line1):
            raise ValueError('TLE line 1 checksum mismatch')
        if not checksum_ok(line2):
            raise ValueError('TLE line 2 checksum mismatch')
    sat1 = int(line1[2:7])
    sat2 = int(line2[2:7])
    if sat1 != sat2:
        raise ValueError('TLE satellite numbers disagree')
    year2 = int(line1[18:20])
    year = 1900 + year2 if year2 >= 57 else 2000 + year2
    day = float(line1[20:32])
    if not 1.0 <= day < 367.0:
        raise ValueError(f'TLE epoch day out of range: {day}')
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
        classification=line1[7],
        intl_designator=line1[9:17].strip(),
        mean_motion_dot_rev_day2=float(line1[33:43]),
        mean_motion_ddot_rev_day3=_implied_decimal(line1[44:52]),
        bstar_inv_earth_radii=_implied_decimal(line1[53:61]),
        ephemeris_type=int(line1[62]) if line1[62].isdigit() else 0,
        element_set_number=int(line1[64:68]),
        rev_number=int(line2[63:68]),
    )

def epoch_datetime(record: TLERecord) -> dt.datetime:
    """TLE epoch (year + day-of-year) as a UTC datetime."""
    base = dt.datetime(record.epoch_year, 1, 1, tzinfo=dt.timezone.utc)
    return base + dt.timedelta(days=record.epoch_day - 1.0)

def orbital_period_s(record):
    return 86400.0 / record.mean_motion_rev_day

def age_days(record, year, day):
    return (year - record.epoch_year) * 365.25 + (day - record.epoch_day)
