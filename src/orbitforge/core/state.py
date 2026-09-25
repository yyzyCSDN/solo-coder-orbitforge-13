from __future__ import annotations
from dataclasses import dataclass
from .vector import Vec3

@dataclass(frozen=True)
class CartesianState:
    epoch_tai_s: float
    position_km: Vec3
    velocity_km_s: Vec3
    frame: str = 'ECI'

    def shifted(self, dt: float):
        return CartesianState(self.epoch_tai_s + dt, self.position_km + self.velocity_km_s * dt, self.velocity_km_s, self.frame)

@dataclass(frozen=True)
class GroundPoint:
    lat_rad: float
    lon_rad: float
    alt_km: float = 0.0

@dataclass(frozen=True)
class TimeWindow:
    start_tai_s: float
    end_tai_s: float

    def __post_init__(self):
        if self.end_tai_s < self.start_tai_s:
            raise ValueError('negative window')

    @property
    def duration_s(self):
        return self.end_tai_s - self.start_tai_s

    def intersects(self, o):
        return self.start_tai_s < o.end_tai_s and o.start_tai_s < self.end_tai_s
