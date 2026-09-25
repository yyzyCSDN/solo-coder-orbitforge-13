from __future__ import annotations
from orbitforge.core.vector import Vec3


def finite_difference_jacobian(endpoint_fn, control: Vec3, steps: Vec3):
    columns = []
    for axis, step in enumerate((steps.x, steps.y, steps.z)):
        plus = [control.x, control.y, control.z]
        minus = list(plus)
        plus[axis] += step
        minus[axis] -= step
        yp = endpoint_fn(Vec3(*plus))
        ym = endpoint_fn(Vec3(*minus))
        columns.append((yp - ym) / (2.0 * step))
    return columns

def solve_3x3(columns, error: Vec3):
    a = [[columns[j].as_tuple()[i] for j in range(3)] for i in range(3)]
    b = [error.x, error.y, error.z]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda r: abs(a[r][col]))
        if abs(a[pivot][col]) < 1e-12:
            raise ValueError('singular targeting geometry')
        a[col], a[pivot] = a[pivot], a[col]
        b[col], b[pivot] = b[pivot], b[col]
        scale = a[col][col]
        a[col] = [x / scale for x in a[col]]
        b[col] /= scale
        for row in range(3):
            if row == col:
                continue
            factor = a[row][col]
            a[row] = [a[row][j] - factor * a[col][j] for j in range(3)]
            b[row] -= factor * b[col]
    return Vec3(*b)

def correction(endpoint_fn, control, target, step=1e-4):
    endpoint = endpoint_fn(control)
    error = target - endpoint
    columns = finite_difference_jacobian(endpoint_fn, control, Vec3(step, step, step))
    return solve_3x3(columns, error)
