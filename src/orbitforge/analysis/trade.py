from __future__ import annotations

def normalize(records, keys):
    ranges = {k: (min((r[k] for r in records)), max((r[k] for r in records))) for k in keys}
    out = []
    for r in records:
        row = dict(r)
        for k, (lo, hi) in ranges.items():
            row[k + '_norm'] = (r[k] - lo) / (hi - lo) if hi > lo else 0.0
        out.append(row)
    return out

def rank(records, weights):
    return sorted(records, key=lambda r: sum((r.get(k + '_norm', 0) * w for k, w in weights.items())), reverse=True)
