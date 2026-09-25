from __future__ import annotations

def evaluate(pointing_error_deg, wheel_saturation_fraction, slew_margin_s, keepout_violations, limits):
    findings = []
    if pointing_error_deg > limits.get('max_pointing_error_deg', float('inf')):
        findings.append(('pointing_error', pointing_error_deg))
    if wheel_saturation_fraction > limits.get('max_wheel_fraction', 1.0):
        findings.append(('wheel_saturation', wheel_saturation_fraction))
    if slew_margin_s < limits.get('min_slew_margin_s', 0.0):
        findings.append(('slew_margin', slew_margin_s))
    if keepout_violations:
        findings.append(('keepout_violations', len(keepout_violations)))
    return findings
