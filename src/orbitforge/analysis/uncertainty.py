from __future__ import annotations
import math

def rss(sigmas):
    return math.sqrt(sum((s * s for s in sigmas)))

def linear_covariance(jacobian, cov):
    m = len(jacobian)
    n = len(jacobian[0])
    out = [[0.0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            out[i][j] = sum((jacobian[i][k] * cov[k][l] * jacobian[j][l] for k in range(n) for l in range(n)))
    return out

def confidence_interval(mean, sigma, z=1.96):
    return (mean - z * sigma, mean + z * sigma)
