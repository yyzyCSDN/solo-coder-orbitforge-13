from __future__ import annotations

def evaluate(passes, minimum_daily_contacts, minimum_margin_db, maximum_outage_fraction):
    findings = []
    if len(passes) < minimum_daily_contacts:
        findings.append(('too_few_contacts', len(passes)))
    margins = [row.get('min_margin_db', 0.0) for row in passes]
    if margins and min(margins) < minimum_margin_db:
        findings.append(('link_margin_low', min(margins)))
    outage = sum(row.get('outage_fraction', 0.0) for row in passes) / len(passes) if passes else 1.0
    if outage > maximum_outage_fraction:
        findings.append(('outage_fraction_high', outage))
    return findings

def ready(findings):
    return not findings
