"""Genuine SGP4/SDP4 propagation for catalogued TLEs.

TLE element sets are *mean* elements in the SGP4 perturbation theory (WGS72
constants, BSTAR drag term). They are only meaningful inside SGP4/SDP4 —
feeding them to a two-body or J2-only propagator (e.g. orbitforge.orbits'
Kepler/Cowell helpers) silently produces errors that grow to hundreds of
kilometres within days, and BSTAR would be ignored entirely. This module
therefore delegates to the reference implementation (python-sgp4, the
Vallado STR#3 code verified against the official SGP4-VER test vectors)
and always reports exactly which engine and model branch produced a state.
"""
from __future__ import annotations
from dataclasses import dataclass
import datetime as dt
import math
import sgp4
from sgp4.api import Satrec
from orbitforge.time.julian import UNIX_JD, datetime_to_unix
from .model import TLEVersion

SGP4_ERRORS = {
    1: 'mean eccentricity out of range',
    2: 'mean motion less than zero',
    3: 'perturbed eccentricity out of range',
    4: 'semi-latus rectum less than zero',
    5: 'epoch elements are sub-orbital',
    6: 'satellite has decayed',
}

@dataclass(frozen=True)
class PropagationResult:
    version: TLEVersion
    time: dt.datetime
    frame: str               # always 'TEME'
    position_km: tuple[float, float, float]
    velocity_km_s: tuple[float, float, float]
    minutes_from_epoch: float
    model: str               # 'SGP4' (near-earth) or 'SDP4' (deep-space)
    sgp4_error: int          # 0 = success; see SGP4_ERRORS

class SGP4Propagator:
    name = 'SGP4'
    library = 'python-sgp4'
    library_version = sgp4.__version__

    def __init__(self):
        self._satrecs: dict[str, Satrec] = {}

    def _satrec(self, version: TLEVersion) -> Satrec:
        sat = self._satrecs.get(version.version_id)
        if sat is None:
            sat = Satrec.twoline2rv(version.line1, version.line2)
            self._satrecs[version.version_id] = sat
        return sat

    def propagate(self, version: TLEVersion, when: dt.datetime) -> PropagationResult:
        sat = self._satrec(version)
        # Split into Julian day + fraction *before* forming the JD: a single
        # float JD near 2.46e6 only carries ~0.2 ms of resolution, which would
        # cost metres of along-track error for no reason.
        unix_s = datetime_to_unix(when)
        day = math.floor(unix_s / 86400.0)
        jd = UNIX_JD + day
        fr = (unix_s - day * 86400.0) / 86400.0
        err, r, v = sat.sgp4(jd, fr)
        minutes = (when - version.epoch).total_seconds() / 60.0
        return PropagationResult(
            version=version,
            time=when,
            frame='TEME',
            position_km=(r[0], r[1], r[2]),
            velocity_km_s=(v[0], v[1], v[2]),
            minutes_from_epoch=minutes,
            model='SDP4' if sat.method == 'd' else 'SGP4',
            sgp4_error=err,
        )

    def info(self) -> dict:
        return {
            'name': self.name,
            'library': self.library,
            'library_version': self.library_version,
            'output_frame': 'TEME',
            'notes': 'TLE mean elements are propagated with genuine SGP4/SDP4 '
                     '(Vallado STR#3 reference implementation); BSTAR drag term '
                     'is applied by the theory, not ignored.',
        }
