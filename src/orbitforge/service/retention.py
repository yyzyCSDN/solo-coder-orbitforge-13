from __future__ import annotations

def retention_preview(records, now, policies):
    keep = []
    delete = []
    for record in records:
        days = policies.get(record['kind'])
        if days is None:
            keep.append((record, 'no_policy'))
            continue
        age = now - record['created']
        if age >= days * 86400.0:
            delete.append((record, 'expired'))
        else:
            keep.append((record, 'within_window'))
    return {'keep': keep, 'delete': delete}

def apply_preview(preview, current_ids):
    approved = []
    stale = []
    for record, reason in preview['delete']:
        if record['id'] in current_ids:
            approved.append(record['id'])
        else:
            stale.append(record['id'])
    return approved, stale
