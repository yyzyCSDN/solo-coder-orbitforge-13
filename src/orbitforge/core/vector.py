from __future__ import annotations
from dataclasses import dataclass
import math
from .errors import GeometryError

@dataclass(frozen=True)
class Vec3:
    x: float
    y: float
    z: float

    def __add__(self, o):
        return Vec3(self.x + o.x, self.y + o.y, self.z + o.z)

    def __sub__(self, o):
        return Vec3(self.x - o.x, self.y - o.y, self.z - o.z)

    def __mul__(self, k: float):
        return Vec3(self.x * k, self.y * k, self.z * k)
    __rmul__ = __mul__

    def __truediv__(self, k: float):
        if k == 0:
            raise ZeroDivisionError('vector division by zero')
        return Vec3(self.x / k, self.y / k, self.z / k)

    def dot(self, o):
        return self.x * o.x + self.y * o.y + self.z * o.z

    def cross(self, o):
        return Vec3(self.y * o.z - self.z * o.y, self.z * o.x - self.x * o.z, self.x * o.y - self.y * o.x)

    def norm2(self):
        return self.dot(self)

    def norm(self):
        return math.sqrt(self.norm2())

    def unit(self):
        n = self.norm()
        if n < 1e-15:
            raise GeometryError('cannot normalize zero vector')
        return self / n

    def angle(self, o):
        d = self.norm() * o.norm()
        if d < 1e-15:
            raise GeometryError('angle with zero vector')
        return math.acos(max(-1.0, min(1.0, self.dot(o) / d)))

    def as_tuple(self):
        return (self.x, self.y, self.z)

def lerp(a: Vec3, b: Vec3, t: float) -> Vec3:
    return a * (1 - t) + b * t

def triple(a: Vec3, b: Vec3, c: Vec3) -> float:
    return a.dot(b.cross(c))
