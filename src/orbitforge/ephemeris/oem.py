from __future__ import annotations
from orbitforge.core.vector import Vec3
from .interpolation import EphemerisPoint

def write_simple_oem(points, object_id='SPACECRAFT'):
    lines = ['CCSDS_OEM_VERS = 2.0', f'OBJECT_ID = {object_id}', 'REF_FRAME = EME2000', 'TIME_SYSTEM = TAI', 'META_STOP']
    for p in points:
        lines.append(f'{p.t:.6f} {p.r.x:.9f} {p.r.y:.9f} {p.r.z:.9f} {p.v.x:.12f} {p.v.y:.12f} {p.v.z:.12f}')
    return '\n'.join(lines) + '\n'

def parse_simple_oem(text):
    pts = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) == 7 and parts[0].replace('.', '', 1).isdigit():
            pts.append(EphemerisPoint(float(parts[0]), Vec3(*map(float, parts[1:4])), Vec3(*map(float, parts[4:7]))))
    return pts
