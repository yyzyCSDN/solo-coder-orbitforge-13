from __future__ import annotations

def evaluate(min_soc, max_soc, eclipse_margin_wh, battery_temp_k, limits):
    findings = []
    if min_soc < limits['min_soc']:
        findings.append(('soc_low', min_soc))
    if max_soc > limits.get('max_soc', 1.0):
        findings.append(('soc_high', max_soc))
    if eclipse_margin_wh < limits.get('min_eclipse_margin_wh', 0.0):
        findings.append(('eclipse_margin_low', eclipse_margin_wh))
    low_t, high_t = limits.get('battery_temperature_k', (0.0, float('inf')))
    if not low_t <= battery_temp_k <= high_t:
        findings.append(('battery_temperature', battery_temp_k))
    return findings
