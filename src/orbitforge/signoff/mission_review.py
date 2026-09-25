from __future__ import annotations

def aggregate(sections):
    blocking = []
    warnings = []
    for name, result in sections.items():
        for finding in result.get('findings', []):
            severity = finding[-1] if isinstance(finding, tuple) and finding and finding[-1] in {'warning', 'error'} else 'error'
            entry = (name, finding)
            if severity == 'warning':
                warnings.append(entry)
            else:
                blocking.append(entry)
    return {'ready': not blocking, 'blocking': blocking, 'warnings': warnings}

def decision(summary, approver=None):
    if summary['ready']:
        return {'status': 'approved', 'approver': approver, 'reason': None}
    return {'status': 'blocked', 'approver': approver, 'reason': f"{len(summary['blocking'])} blocking findings"}
