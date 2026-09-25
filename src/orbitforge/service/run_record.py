from __future__ import annotations
from dataclasses import dataclass
import time

@dataclass
class RunRecord:
    run_id: str
    analysis: str
    snapshot_id: str
    started: float
    finished: float | None = None
    status: str = 'running'
    error: str | None = None

    @property
    def duration_s(self):
        end = self.finished if self.finished is not None else time.time()
        return max(0.0, end - self.started)

    def succeed(self):
        self.finished = time.time()
        self.status = 'succeeded'
        self.error = None

    def fail(self, error):
        self.finished = time.time()
        self.status = 'failed'
        self.error = str(error)

def failure_rate(records):
    completed = [r for r in records if r.status in {'succeeded', 'failed'}]
    return sum(r.status == 'failed' for r in completed) / len(completed) if completed else 0.0
