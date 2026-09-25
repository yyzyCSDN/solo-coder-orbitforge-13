from __future__ import annotations

def flatten(payload, prefix=''):
    out = {}
    if isinstance(payload, dict):
        for key, value in payload.items():
            name = f'{prefix}.{key}' if prefix else str(key)
            out.update(flatten(value, name))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            out.update(flatten(value, f'{prefix}[{index}]'))
    else:
        out[prefix] = payload
    return out

def diff(a, b):
    fa = flatten(a)
    fb = flatten(b)
    keys = sorted(set(fa) | set(fb))
    return [{'path': key, 'before': fa.get(key), 'after': fb.get(key)} for key in keys if fa.get(key) != fb.get(key)]

def changed_paths(a, b):
    return [row['path'] for row in diff(a, b)]
