from __future__ import annotations
from dataclasses import dataclass
from orbitforge.core.state import TimeWindow

@dataclass(frozen=True)
class Activity:
    name: str
    window: TimeWindow
    resource: str
    priority: int = 0

class Timeline:

    def __init__(self):
        self.activities = []

    def add(self, a: Activity):
        for e in self.activities:
            if e.resource == a.resource and e.window.intersects(a.window):
                raise ValueError(f'resource conflict: {a.resource}')
        self.activities.append(a)
        self.activities.sort(key=lambda x: (x.window.start_tai_s, -x.priority, x.name))

    def gaps(self, start, end, resource):
        cur = start
        out = []
        for a in [x for x in self.activities if x.resource == resource and x.window.end_tai_s > start and (x.window.start_tai_s < end)]:
            if a.window.start_tai_s > cur:
                out.append(TimeWindow(cur, min(a.window.start_tai_s, end)))
            cur = max(cur, a.window.end_tai_s)
        if cur < end:
            out.append(TimeWindow(cur, end))
        return out
