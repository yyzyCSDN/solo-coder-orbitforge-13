from __future__ import annotations


def orbital_state_invariants(state):
    findings = []
    if state.position_km.norm() <= 6378.0:
        findings.append('inside_earth')
    if state.velocity_km_s.norm() <= 0.0:
        findings.append('zero_velocity')
    if not state.frame:
        findings.append('missing_frame')
    return findings


def covariance_invariants(matrix):
    findings = []
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        return ['not_square']
    for i in range(n):
        if matrix[i][i] < 0.0:
            findings.append(f'negative_variance_{i}')
        for j in range(i + 1, n):
            if abs(matrix[i][j] - matrix[j][i]) > 1e-10:
                findings.append(f'asymmetry_{i}_{j}')
    return findings


def timeline_invariants(activities):
    findings = []
    ordered = sorted(activities, key=lambda a: a.window.start_tai_s)
    for a in ordered:
        if a.window.end_tai_s < a.window.start_tai_s:
            findings.append(('negative_window', a.name))
    return findings
