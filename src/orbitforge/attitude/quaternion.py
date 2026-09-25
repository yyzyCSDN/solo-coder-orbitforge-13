from __future__ import annotations
from dataclasses import dataclass
import math
from orbitforge.core.vector import Vec3

@dataclass(frozen=True)
class Quaternion:
    w: float
    x: float
    y: float
    z: float

    def norm(self):
        return math.sqrt(self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z)

    def normalized(self):
        n = self.norm()
        return Quaternion(self.w / n, self.x / n, self.y / n, self.z / n)

    def conj(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def __mul__(self, o):
        return Quaternion(self.w * o.w - self.x * o.x - self.y * o.y - self.z * o.z, self.w * o.x + self.x * o.w + self.y * o.z - self.z * o.y, self.w * o.y - self.x * o.z + self.y * o.w + self.z * o.x, self.w * o.z + self.x * o.y - self.y * o.x + self.z * o.w)

    def rotate(self, v: Vec3) -> Vec3:
        q = self.normalized()
        p = q * Quaternion(0, v.x, v.y, v.z) * q.conj()
        return Vec3(p.x, p.y, p.z)

    @classmethod
    def from_axis_angle(cls, axis: Vec3, angle: float):
        u = axis.unit()
        s = math.sin(angle / 2)
        return cls(math.cos(angle / 2), u.x * s, u.y * s, u.z * s)

def slerp(a: Quaternion, b: Quaternion, t: float) -> Quaternion:
    a, b = (a.normalized(), b.normalized())
    d = a.w * b.w + a.x * b.x + a.y * b.y + a.z * b.z
    if d < 0:
        b = Quaternion(-b.w, -b.x, -b.y, -b.z)
        d = -d
    if d > 0.9995:
        return Quaternion(a.w + t * (b.w - a.w), a.x + t * (b.x - a.x), a.y + t * (b.y - a.y), a.z + t * (b.z - a.z)).normalized()
    th = math.acos(max(-1, min(1, d)))
    s = math.sin(th)
    u = math.sin((1 - t) * th) / s
    v = math.sin(t * th) / s
    return Quaternion(a.w * u + b.w * v, a.x * u + b.x * v, a.y * u + b.y * v, a.z * u + b.z * v)
