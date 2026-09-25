from __future__ import annotations

def plan(records, now, retention_by_kind):
    keep = []
    archive = []
    delete = []
    for record in records:
        rule = retention_by_kind.get(record['kind'])
        if rule is None:
            keep.append(record)
            continue
        age_days = (now - record['created']) / 86400.0
        archive_after = rule.get('archive_after_days')
        delete_after = rule.get('delete_after_days')
        if delete_after is not None and age_days >= delete_after:
            delete.append(record)
        elif archive_after is not None and age_days >= archive_after:
            archive.append(record)
        else:
            keep.append(record)
    return {'keep': keep, 'archive': archive, 'delete': delete}

def counts(plan_result):
    return {name: len(rows) for name, rows in plan_result.items()}
