from __future__ import annotations

def validate(contacts):
    findings = []
    ordered = sorted(contacts, key=lambda c: (c['station'], c['start'], c['end']))
    for contact in ordered:
        if contact['end'] <= contact['start']:
            findings.append((contact.get('id'), 'invalid_window'))
        if contact.get('max_elevation_rad', 0.0) < contact.get('min_elevation_rad', 0.0):
            findings.append((contact.get('id'), 'elevation_inconsistent'))
    by_station = {}
    for contact in ordered:
        by_station.setdefault(contact['station'], []).append(contact)
    for station, rows in by_station.items():
        for a, b in zip(rows, rows[1:]):
            if b['start'] < a['end']:
                findings.append((station, 'overlap', a.get('id'), b.get('id')))
    return findings

def valid(contacts):
    return not validate(contacts)
