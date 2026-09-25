from __future__ import annotations
import datetime as dt
from .leap_seconds import tai_to_utc_unix
UNIX_JD = 2440587.5

def unix_to_julian(unix_s: float) -> float:
    return UNIX_JD + unix_s / 86400.0

def julian_to_unix(jd: float) -> float:
    return (jd - UNIX_JD) * 86400.0

def tai_to_julian_utc(tai_s: float) -> float:
    return unix_to_julian(tai_to_utc_unix(tai_s))

def datetime_to_unix(value: dt.datetime) -> float:
    if value.tzinfo is None:
        value = value.replace(tzinfo=dt.timezone.utc)
    return value.timestamp()

def unix_to_datetime(value: float) -> dt.datetime:
    return dt.datetime.fromtimestamp(value, tz=dt.timezone.utc)

def julian_centuries_tt(jd_tt: float) -> float:
    return (jd_tt - 2451545.0) / 36525.0
