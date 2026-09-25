from __future__ import annotations
import math

def rotate_covariance_2d(cov, angle):
    c, s = (math.cos(angle), math.sin(angle))
    r = ((c, -s), (s, c))
    return tuple((tuple((sum((r[i][k] * sum((cov[k][m] * r[j][m] for m in range(2))) for k in range(2))) for j in range(2))) for i in range(2)))

def combine_covariance(a, b):
    return ((a[0][0] + b[0][0], a[0][1] + b[0][1]), (a[1][0] + b[1][0], a[1][1] + b[1][1]))

def determinant(c):
    return c[0][0] * c[1][1] - c[0][1] * c[1][0]

def inverse(c):
    d = determinant(c)
    if d <= 0:
        raise ValueError('covariance must be positive definite')
    return ((c[1][1] / d, -c[0][1] / d), (-c[1][0] / d, c[0][0] / d))
