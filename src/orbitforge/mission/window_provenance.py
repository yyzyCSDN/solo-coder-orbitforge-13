from __future__ import annotations
from dataclasses import dataclass
from orbitforge.core.state import TimeWindow

@dataclass(frozen=True)
class DerivedWindow:
    window: TimeWindow
    sources: frozenset[str]

def intersect(a, b):
    start = max(a.window.start_tai_s, b.window.start_tai_s)
    end = min(a.window.end_tai_s, b.window.end_tai_s)
    if start >= end:
        return None
    return DerivedWindow(TimeWindow(start, end), a.sources | b.sources)

def merge_touching(windows):
    ordered = sorted(windows, key=lambda x: x.window.start_tai_s)
    out = []
    for item in ordered:
        if not out or item.window.start_tai_s > out[-1].window.end_tai_s:
            out.append(item)
        else:
            previous = out[-1]
            out[-1] = DerivedWindow(TimeWindow(previous.window.start_tai_s, max(previous.window.end_tai_s, item.window.end_tai_s)), previous.sources | item.sources)
    return out

def source_usage(windows):
    counts = {}
    for item in windows:
        for source in item.sources:
            counts[source] = counts.get(source, 0) + 1
    return counts
