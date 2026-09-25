from __future__ import annotations

def component_status(checks):
    return {name: ('ready' if fn() else 'degraded') for name, fn in checks.items()}

def overall(status):
    values = set(status.values())
    if not values or values == {'ready'}:
        return 'ready'
    if 'failed' in values:
        return 'failed'
    return 'degraded'

def readiness_payload(checks):
    status = component_status(checks)
    return {'status': overall(status), 'components': status}
