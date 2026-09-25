from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    evidence: str
    severity: str = 'error'

def summarize(checks):
    failed = [c for c in checks if not c.passed]
    blocking = [c for c in failed if c.severity == 'error']
    warnings = [c for c in failed if c.severity == 'warning']
    return {
        'total': len(checks),
        'passed': len(checks) - len(failed),
        'failed': len(failed),
        'blocking': [c.name for c in blocking],
        'warnings': [c.name for c in warnings],
        'ready': not blocking,
    }

def require(checks):
    summary = summarize(checks)
    if not summary['ready']:
        raise ValueError('blocking signoff checks: ' + ','.join(summary['blocking']))
    return summary
