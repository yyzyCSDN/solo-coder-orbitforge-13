from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import math
from typing import Any


STALE_TLE_DAYS = 14.0
SGP4_MODEL = 'SGP4/WGS72'


class SGP4UnavailableError(RuntimeError):
    """Raised when the real SGP4 runtime dependency is not installed."""


class TLEParseError(ValueError):
    def __init__(self, message: str, line_number: int | None = None):
        super().__init__(message)
        self.line_number = line_number


class TLEPropagationError(RuntimeError):
    """Raised when SGP4 rejects a propagation request."""


def _checksum(line: str) -> int:
    value = 0
    for char in line[:-1]:
        if char.isdigit():
            value += int(char)
        elif char == '-':
            value += 1
    return value % 10


def validate_tle_line(line: str, expected_number: int, line_number: int | None = None) -> None:
    if len(line) != 69:
        raise TLEParseError(
            f'TLE line {expected_number} must be exactly 69 characters, got {len(line)}',
            line_number,
        )
    if not line.startswith(f'{expected_number} '):
        raise TLEParseError(f'expected TLE line {expected_number}', line_number)
    try:
        stored = int(line[68])
    except ValueError as exc:
        raise TLEParseError(f'TLE line {expected_number} checksum is not numeric', line_number) from exc
    actual = _checksum(line)
    if stored != actual:
        raise TLEParseError(
            f'TLE line {expected_number} checksum mismatch: expected {actual}, found {stored}',
            line_number,
        )


def tle_epoch(year: int, day_of_year: float) -> float:
    """Return a TLE epoch as a POSIX UTC timestamp."""
    jan1 = datetime(year, 1, 1, tzinfo=timezone.utc)
    return jan1.timestamp() + (day_of_year - 1.0) * 86400.0


def epoch_components(line1: str) -> tuple[int, float]:
    try:
        year2 = int(line1[18:20])
        day = float(line1[20:32])
    except (ValueError, IndexError) as exc:
        raise TLEParseError('invalid TLE epoch') from exc
    year = 1900 + year2 if year2 >= 57 else 2000 + year2
    days_in_year = 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365
    if not 0.99999999 <= day <= days_in_year + 0.00000001:
        raise TLEParseError(f'TLE epoch day {day} is outside {year}')
    return year, day


def _decimal_field(line: str, start: int, end: int, label: str) -> float:
    text = line[start:end].strip()
    if not text:
        raise TLEParseError(f'missing {label}')
    try:
        sign = 1.0
        if text[0] in '+-':
            sign = -1.0 if text[0] == '-' else 1.0
            text = text[1:]
        if not text:
            raise ValueError('empty numeric field')
        if 'e' in text.lower():
            return sign * float(text)
        if '-' in text or '+' in text:
            # TLE compact notation: implicit decimal point before all digits,
            # e.g. "36715-3" means 0.36715e-3 = 3.6715e-4.
            sign_index = max(text.rfind('-'), text.rfind('+'))
            mantissa_text = text[:sign_index]
            exponent_marker = text[sign_index]
            exponent_text = text[sign_index + 1:]
            mantissa = float('0.' + mantissa_text) if mantissa_text else 0.0
            exponent = int(exponent_text)
            if exponent_marker == '-':
                exponent = -exponent
            return sign * mantissa * (10.0 ** exponent)
        return sign * float(text)
    except ValueError as exc:
        raise TLEParseError(f'invalid {label}: {line[start:end]!r}') from exc


def version_id_for(line1: str, line2: str) -> str:
    digest = hashlib.sha256((line1 + '\n' + line2).encode('ascii')).hexdigest()
    return digest[:16]


@dataclass(frozen=True)
class TLEVersion:
    version_id: str
    name: str
    line1: str
    line2: str
    satellite_number: int
    classification: str
    international_designator: str
    epoch_year: int
    epoch_day: float
    epoch_unix: float
    bstar: float
    mean_motion_dot: float
    mean_motion_ddot: float
    ephemeris_type: int
    element_set_number: int | None
    inclination_rad: float
    raan_rad: float
    eccentricity: float
    argp_rad: float
    mean_anomaly_rad: float
    mean_motion_rev_day: float
    revolutions: int

    @classmethod
    def from_lines(cls, name: str, line1: str, line2: str) -> 'TLEVersion':
        validate_tle_line(line1, 1)
        validate_tle_line(line2, 2)
        try:
            satellite_number = int(line1[2:7])
            line2_number = int(line2[2:7])
        except ValueError as exc:
            raise TLEParseError('invalid TLE satellite number') from exc
        if satellite_number != line2_number:
            raise TLEParseError('TLE satellite numbers disagree')

        year, day = epoch_components(line1)
        try:
            inclination = math.radians(float(line2[8:16]))
            raan = math.radians(float(line2[17:25]))
            ecc_text = line2[26:33].strip()
            eccentricity = float('0.' + ecc_text) if ecc_text else 0.0
            argp = math.radians(float(line2[34:42]))
            mean_anomaly = math.radians(float(line2[43:51]))
            mean_motion = float(line2[52:63])
            revolutions = int(line2[63:68])
            ephemeris_type = int(line1[62:63])
            element_set_text = line1[64:68].strip()
            element_set_number = int(element_set_text) if element_set_text else None
        except ValueError as exc:
            raise TLEParseError('invalid TLE orbital element') from exc

        return cls(
            version_id=version_id_for(line1, line2),
            name=name.strip(),
            line1=line1,
            line2=line2,
            satellite_number=satellite_number,
            classification=line1[7:8].strip() or 'U',
            international_designator=line1[9:17].strip(),
            epoch_year=year,
            epoch_day=day,
            epoch_unix=tle_epoch(year, day),
            bstar=_decimal_field(line1, 54, 61, 'BSTAR drag term'),
            mean_motion_dot=float(line1[33:43]),
            mean_motion_ddot=_decimal_field(line1, 45, 52, 'mean motion second derivative'),
            ephemeris_type=ephemeris_type,
            element_set_number=element_set_number,
            inclination_rad=inclination,
            raan_rad=raan,
            eccentricity=eccentricity,
            argp_rad=argp,
            mean_anomaly_rad=mean_anomaly,
            mean_motion_rev_day=mean_motion,
            revolutions=revolutions,
        )

    @property
    def raw_tle(self) -> str:
        return self.line1 + '\n' + self.line2

    @property
    def three_line_tle(self) -> str:
        name = self.name or str(self.satellite_number)
        return name + '\n' + self.raw_tle

    def age_days_at(self, when_unix: float) -> float:
        return (when_unix - self.epoch_unix) / 86400.0

    def is_stale_at(self, when_unix: float, max_age_days: float = STALE_TLE_DAYS) -> bool:
        return self.age_days_at(when_unix) > max_age_days

    def metadata(self) -> dict[str, Any]:
        return {
            'version_id': self.version_id,
            'name': self.name,
            'satellite_number': self.satellite_number,
            'classification': self.classification,
            'international_designator': self.international_designator,
            'epoch_year': self.epoch_year,
            'epoch_day': self.epoch_day,
            'epoch_unix': self.epoch_unix,
            'epoch_utc': datetime.fromtimestamp(self.epoch_unix, timezone.utc).isoformat(),
            'bstar': self.bstar,
            'bstar_units': '1/earth_radius',
            'mean_motion_dot': self.mean_motion_dot,
            'mean_motion_ddot': self.mean_motion_ddot,
            'ephemeris_type': self.ephemeris_type,
            'element_set_number': self.element_set_number,
            'inclination_rad': self.inclination_rad,
            'raan_rad': self.raan_rad,
            'eccentricity': self.eccentricity,
            'argp_rad': self.argp_rad,
            'mean_anomaly_rad': self.mean_anomaly_rad,
            'mean_motion_rev_day': self.mean_motion_rev_day,
            'revolutions': self.revolutions,
        }


@dataclass(frozen=True)
class VersionSelection:
    version: TLEVersion
    policy: str
    query_unix: float
    warnings: tuple[str, ...]
    elapsed_from_epoch_s: float
    stale: bool

    def metadata(self) -> dict[str, Any]:
        data = self.version.metadata()
        data['raw_tle'] = self.version.raw_tle
        data.update(
            {
                'selection_policy': self.policy,
                'elapsed_from_epoch_s': self.elapsed_from_epoch_s,
                'stale': self.stale,
                'warnings': list(self.warnings),
                'propagator': SGP4_MODEL,
                'propagates_from_epoch_unix': self.version.epoch_unix,
            }
        )
        return data


def parse_tle_text(text: str) -> tuple[list[tuple[TLEVersion, int]], list[dict[str, Any]]]:
    """Parse 2LE/3LE text, retaining every distinct raw line-pair version."""
    lines = text.lstrip('﻿').splitlines()
    versions: list[tuple[TLEVersion, int]] = []
    errors: list[dict[str, Any]] = []
    pending_name = ''
    pending_line1: str | None = None
    pending_line1_number: int | None = None

    def drop_pending_line1() -> None:
        nonlocal pending_line1, pending_line1_number, pending_name
        errors.append({
            'line_number': pending_line1_number,
            'message': 'TLE line 1 was not followed by line 2',
        })
        pending_line1 = None
        pending_line1_number = None
        pending_name = ''

    for zero_based, raw in enumerate(lines):
        line_no = zero_based + 1
        line = raw.rstrip('\r')
        if not line.strip():
            continue

        if line.startswith('1 '):
            if pending_line1 is not None:
                drop_pending_line1()
            pending_line1 = line
            pending_line1_number = line_no
        elif line.startswith('2 '):
            if pending_line1 is None:
                errors.append({'line_number': line_no, 'message': 'TLE line 2 has no preceding line 1'})
                continue
            try:
                parsed_version = TLEVersion.from_lines(pending_name, pending_line1, line)
                versions.append((parsed_version, pending_line1_number or line_no))
            except TLEParseError as exc:
                errors.append({'line_number': exc.line_number or pending_line1_number or line_no, 'message': str(exc)})
            pending_name = ''
            pending_line1 = None
            pending_line1_number = None
        else:
            # In 2LE catalogs there is no name between successive line pairs.
            # A name only applies when it appears before the following line 1.
            if pending_line1 is not None:
                drop_pending_line1()
            pending_name = line.strip()

    if pending_line1 is not None:
        errors.append({
            'line_number': pending_line1_number,
            'message': 'TLE line 1 was not followed by line 2',
        })
    return versions, errors
