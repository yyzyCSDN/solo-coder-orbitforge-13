from __future__ import annotations
import math
from .quaternion import Quaternion

def quaternion_from_zyx(yaw: float, pitch: float, roll: float):
    cy, sy = (math.cos(yaw / 2), math.sin(yaw / 2))
    cp, sp = (math.cos(pitch / 2), math.sin(pitch / 2))
    cr, sr = (math.cos(roll / 2), math.sin(roll / 2))
    return Quaternion(cr * cp * cy + sr * sp * sy, sr * cp * cy - cr * sp * sy, cr * sp * cy + sr * cp * sy, cr * cp * sy - sr * sp * cy)

def zyx_from_quaternion(q: Quaternion):
    q = q.normalized()
    sinr = 2.0 * (q.w * q.x + q.y * q.z)
    cosr = 1.0 - 2.0 * (q.x * q.x + q.y * q.y)
    roll = math.atan2(sinr, cosr)
    sinp = 2.0 * (q.w * q.y - q.z * q.x)
    pitch = math.copysign(math.pi / 2, sinp) if abs(sinp) >= 1 else math.asin(sinp)
    siny = 2.0 * (q.w * q.z + q.x * q.y)
    cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    yaw = math.atan2(siny, cosy)
    return (yaw, pitch, roll)
