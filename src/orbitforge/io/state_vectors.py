from __future__ import annotations
import csv
import io
from orbitforge.core.vector import Vec3
from orbitforge.core.state import CartesianState

FIELDS = ['epoch_tai_s','x_km','y_km','z_km','vx_km_s','vy_km_s','vz_km_s','frame']

def write_csv(states):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(FIELDS)
    for state in states:
        writer.writerow([
            f'{state.epoch_tai_s:.9f}',
            f'{state.position_km.x:.12f}',
            f'{state.position_km.y:.12f}',
            f'{state.position_km.z:.12f}',
            f'{state.velocity_km_s.x:.15f}',
            f'{state.velocity_km_s.y:.15f}',
            f'{state.velocity_km_s.z:.15f}',
            state.frame,
        ])
    return buffer.getvalue()

def read_csv(text):
    reader = csv.DictReader(io.StringIO(text))
    states = []
    for row in reader:
        states.append(CartesianState(
            float(row['epoch_tai_s']),
            Vec3(float(row['x_km']), float(row['y_km']), float(row['z_km'])),
            Vec3(float(row['vx_km_s']), float(row['vy_km_s']), float(row['vz_km_s'])),
            row.get('frame') or 'ECI',
        ))
    return states

def validate_monotonic(states):
    return all(b.epoch_tai_s > a.epoch_tai_s for a, b in zip(states, states[1:]))

def span(states):
    if not states:
        return None
    return states[0].epoch_tai_s, states[-1].epoch_tai_s
