from __future__ import annotations
from orbitforge.core.state import TimeWindow

def intersect_windows(a, b):
    out = []
    i = j = 0
    a = sorted(a, key=lambda w: w.start_tai_s)
    b = sorted(b, key=lambda w: w.start_tai_s)
    while i < len(a) and j < len(b):
        s = max(a[i].start_tai_s, b[j].start_tai_s)
        e = min(a[i].end_tai_s, b[j].end_tai_s)
        if s < e:
            out.append(TimeWindow(s, e))
        if a[i].end_tai_s < b[j].end_tai_s:
            i += 1
        else:
            j += 1
    return out

def union_windows(windows, merge_touching: bool=True):
    ws = sorted(windows, key=lambda w: w.start_tai_s)
    out = []
    for w in ws:
        if not out or (w.start_tai_s > out[-1].end_tai_s if merge_touching else w.start_tai_s >= out[-1].end_tai_s):
            out.append(w)
        else:
            out[-1] = TimeWindow(out[-1].start_tai_s, max(out[-1].end_tai_s, w.end_tai_s))
    return out

def subtract_windows(base, blocked):
    result = []
    for w in base:
        parts = [w]
        for b in blocked:
            nxt = []
            for p in parts:
                if b.end_tai_s <= p.start_tai_s or b.start_tai_s >= p.end_tai_s:
                    nxt.append(p)
                    continue
                if b.start_tai_s > p.start_tai_s:
                    nxt.append(TimeWindow(p.start_tai_s, b.start_tai_s))
                if b.end_tai_s < p.end_tai_s:
                    nxt.append(TimeWindow(b.end_tai_s, p.end_tai_s))
            parts = nxt
        result.extend(parts)
    return result
