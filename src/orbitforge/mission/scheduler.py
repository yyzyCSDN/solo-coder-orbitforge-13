from __future__ import annotations
from .timeline import Timeline, Activity

def greedy_schedule(candidates):
    timeline = Timeline()
    rejected = []
    for a in sorted(candidates, key=lambda x: (-x.priority, x.window.end_tai_s, x.name)):
        try:
            timeline.add(a)
        except ValueError:
            rejected.append(a)
    return (timeline, rejected)

def score_schedule(timeline):
    return sum((a.priority * max(0.0, a.window.duration_s) for a in timeline.activities))
