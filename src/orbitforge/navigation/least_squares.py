from __future__ import annotations
import math


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(a, b):
    rows = len(a)
    cols = len(b[0])
    inner = len(b)
    return [[sum(a[i][k] * b[k][j] for k in range(inner)) for j in range(cols)] for i in range(rows)]


def solve_linear(a, b):
    n = len(a)
    aug = [list(a[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-14:
            raise ValueError('singular normal matrix')
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [aug[row][j] - factor * aug[col][j] for j in range(n + 1)]
    return [aug[i][-1] for i in range(n)]


def weighted_least_squares(design, residual, sigma):
    if not design:
        raise ValueError('empty design matrix')
    weights = [1.0 / (s * s) for s in sigma]
    normal = [[0.0 for _ in range(len(design[0]))] for _ in range(len(design[0]))]
    rhs = [0.0 for _ in range(len(design[0]))]
    for row, r, w in zip(design, residual, weights):
        for i, vi in enumerate(row):
            rhs[i] += w * vi * r
            for j, vj in enumerate(row):
                normal[i][j] += w * vi * vj
    solution = solve_linear(normal, rhs)
    postfit = []
    for row, r in zip(design, residual):
        postfit.append(r - sum(v * x for v, x in zip(row, solution)))
    rms = math.sqrt(sum(x * x for x in postfit) / len(postfit))
    return solution, postfit, rms


def finite_difference_jacobian(model, parameters, steps):
    base = model(parameters)
    jacobian = [[0.0 for _ in parameters] for _ in base]
    for j, h in enumerate(steps):
        plus = list(parameters)
        minus = list(parameters)
        plus[j] += h
        minus[j] -= h
        yp = model(plus)
        ym = model(minus)
        for i in range(len(base)):
            jacobian[i][j] = (yp[i] - ym[i]) / (2.0 * h)
    return jacobian
