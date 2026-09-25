from __future__ import annotations

def evaluate(perigee_alt_km, apogee_alt_km, eccentricity, inclination_rad, limits):
    findings = []
    if perigee_alt_km < limits.get('min_perigee_km', 0.0):
        findings.append(('perigee_low', perigee_alt_km))
    if apogee_alt_km > limits.get('max_apogee_km', float('inf')):
        findings.append(('apogee_high', apogee_alt_km))
    if eccentricity > limits.get('max_eccentricity', 1.0):
        findings.append(('eccentricity_high', eccentricity))
    if inclination_rad < limits.get('min_inclination_rad', 0.0):
        findings.append(('inclination_low', inclination_rad))
    return findings

def ready(findings):
    return len(findings) == 0
