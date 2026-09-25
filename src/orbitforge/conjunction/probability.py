from __future__ import annotations
import math
from .covariance import inverse, determinant

def collision_probability_2d(miss_x_km: float, miss_y_km: float, cov, hard_body_radius_km: float, samples: int=4000):
    inv = inverse(cov)
    det = determinant(cov)
    r = hard_body_radius_km
    area = math.pi * r * r
    total = 0.0
    n = max(20, int(math.sqrt(samples)))
    for i in range(n):
        x = -r + 2 * r * (i + 0.5) / n
        for j in range(n):
            y = -r + 2 * r * (j + 0.5) / n
            if x * x + y * y > r * r:
                continue
            dx = x - miss_x_km
            dy = y - miss_y_km
            q = dx * (inv[0][0] * dx + inv[0][1] * dy) + dy * (inv[1][0] * dx + inv[1][1] * dy)
            total += math.exp(-0.5 * q) / (2 * math.pi * math.sqrt(det))
    return total * (2 * r / n) ** 2

def mahalanobis2(x, y, cov):
    inv = inverse(cov)
    return x * (inv[0][0] * x + inv[0][1] * y) + y * (inv[1][0] * x + inv[1][1] * y)
