from __future__ import annotations
from dataclasses import dataclass
import math
from orbitforge.core.vector import Vec3
from orbitforge.frames.eci_ecef import eci_to_ecef
from orbitforge.frames.topocentric import ecef_to_enu, az_el_range

@dataclass(frozen=True)
class RangeMeasurement:
    epoch_tai_s: float
    station_ecef_km: Vec3
    range_km: float
    sigma_km: float

@dataclass(frozen=True)
class RangeRateMeasurement:
    epoch_tai_s: float
    station_ecef_km: Vec3
    station_velocity_km_s: Vec3
    range_rate_km_s: float
    sigma_km_s: float

@dataclass(frozen=True)
class AngleMeasurement:
    epoch_tai_s: float
    station_lat_rad: float
    station_lon_rad: float
    station_alt_km: float
    az_rad: float
    el_rad: float
    sigma_rad: float


def predicted_range(position_eci: Vec3, epoch_tai_s: float, station_ecef: Vec3) -> float:
    satellite_ecef = eci_to_ecef(position_eci, epoch_tai_s)
    return (satellite_ecef - station_ecef).norm()


def predicted_angles(position_eci: Vec3, epoch_tai_s: float, lat: float, lon: float, alt: float):
    satellite_ecef = eci_to_ecef(position_eci, epoch_tai_s)
    enu = ecef_to_enu(satellite_ecef, lat, lon, alt)
    return az_el_range(enu)[:2]


def range_residual(position_eci: Vec3, measurement: RangeMeasurement) -> float:
    return measurement.range_km - predicted_range(position_eci, measurement.epoch_tai_s, measurement.station_ecef_km)


def normalized_range_residual(position_eci: Vec3, measurement: RangeMeasurement) -> float:
    if measurement.sigma_km <= 0.0:
        raise ValueError('positive range sigma required')
    return range_residual(position_eci, measurement) / measurement.sigma_km


def angle_residuals(position_eci: Vec3, measurement: AngleMeasurement):
    az, el = predicted_angles(position_eci, measurement.epoch_tai_s, measurement.station_lat_rad, measurement.station_lon_rad, measurement.station_alt_km)
    da = (measurement.az_rad - az + math.pi) % (2.0 * math.pi) - math.pi
    de = measurement.el_rad - el
    return da, de


def reject_outliers(residuals, sigma_limit: float = 4.0):
    return [r for r in residuals if abs(r) <= sigma_limit]
