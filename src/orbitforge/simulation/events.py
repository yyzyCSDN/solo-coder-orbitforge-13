from __future__ import annotations
import heapq
from dataclasses import dataclass, field

@dataclass(order=True)
class ScheduledEvent:
    t: float
    order: int
    name: str = field(compare=False)
    payload: object = field(compare=False, default=None)


class EventQueue:
    def __init__(self):
        self._heap = []
        self._counter = 0

    def schedule(self, t, name, payload=None):
        self._counter += 1
        event = ScheduledEvent(t, self._counter, name, payload)
        heapq.heappush(self._heap, event)
        return event

    def pop_ready(self, now):
        out = []
        while self._heap and self._heap[0].t <= now:
            out.append(heapq.heappop(self._heap))
        return out

    def next_time(self):
        return self._heap[0].t if self._heap else None

    def __len__(self):
        return len(self._heap)
