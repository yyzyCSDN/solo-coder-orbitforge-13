from __future__ import annotations

def build(orbit, contacts, power, conjunctions, findings):
    critical = [f for f in findings if f.get('severity', 'error') == 'error']
    return {
        'orbit': orbit,
        'contact_count': len(contacts),
        'contact_volume_mb': sum(c.get('volume_mb', 0.0) for c in contacts),
        'minimum_soc': power.get('minimum_soc'),
        'conjunction_count': len(conjunctions),
        'highest_collision_probability': max((c.get('collision_probability', 0.0) for c in conjunctions), default=0.0),
        'blocking_findings': len(critical),
        'ready': not critical,
    }

def concise(summary):
    return f"contacts={summary['contact_count']} volume_mb={summary['contact_volume_mb']:.1f} conjunctions={summary['conjunction_count']} blocking={summary['blocking_findings']}"
