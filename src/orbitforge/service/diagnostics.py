from __future__ import annotations

def module_health(modules):
    rows = []
    for name, probe in modules.items():
        try:
            value = probe()
            rows.append({'name': name, 'ok': bool(value), 'detail': value})
        except Exception as exc:
            rows.append({'name': name, 'ok': False, 'detail': f'{type(exc).__name__}: {exc}'})
    return rows

def summary(rows):
    failed = [row for row in rows if not row['ok']]
    return {
        'total': len(rows),
        'healthy': len(rows) - len(failed),
        'failed': len(failed),
        'status': 'ready' if not failed else 'degraded',
        'failures': failed,
    }
