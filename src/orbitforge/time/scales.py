from __future__ import annotations
from dataclasses import dataclass
from .leap_seconds import utc_unix_to_tai, tai_to_utc_unix
TT_MINUS_TAI = 32.184
GPS_MINUS_TAI = -19.0

@dataclass(frozen=True)
class TimeScales:
    tai_s: float

    @property
    def utc_unix_s(self):
        return tai_to_utc_unix(self.tai_s)

    @property
    def tt_s(self):
        return self.tai_s + TT_MINUS_TAI

    @property
    def gps_s(self):
        return self.tai_s + GPS_MINUS_TAI

    @classmethod
    def from_utc_unix(cls, s: float):
        return cls(utc_unix_to_tai(s))

    @classmethod
    def from_gps(cls, s: float):
        return cls(s - GPS_MINUS_TAI)

def delta_t_approx(year: float) -> float:
    t = year - 2000.0
    return 62.92 + 0.32217 * t + 0.005589 * t * t
