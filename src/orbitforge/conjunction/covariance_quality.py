from __future__ import annotations
import math

def correlation(cov, i, j):
    denom = math.sqrt(cov[i][i] * cov[j][j])
    return cov[i][j] / denom if denom > 0.0 else 0.0

def covariance_findings(cov, max_abs_correlation=0.999):
    findings = []
    n = len(cov)
    for i in range(n):
        if cov[i][i] <= 0.0:
            findings.append(('nonpositive_variance', i, cov[i][i]))
        for j in range(i + 1, n):
            if abs(cov[i][j] - cov[j][i]) > 1e-10:
                findings.append(('asymmetric', i, j))
            if abs(correlation(cov, i, j)) > max_abs_correlation:
                findings.append(('near_singular_pair', i, j))
    return findings

def sigma_vector(cov):
    return [math.sqrt(max(0.0, cov[i][i])) for i in range(len(cov))]
