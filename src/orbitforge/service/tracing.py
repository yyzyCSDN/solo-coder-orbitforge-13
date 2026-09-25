from __future__ import annotations
import time
from contextlib import contextmanager

class TraceCollector:
    def __init__(self):
        self.spans = []

    @contextmanager
    def span(self, name, attributes=None):
        start = time.perf_counter()
        record = {'name': name, 'attributes': dict(attributes or {}), 'start': start, 'status': 'running'}
        try:
            yield record
            record['status'] = 'ok'
        except Exception as exc:
            record['status'] = 'error'
            record['error'] = f'{type(exc).__name__}: {exc}'
            raise
        finally:
            record['duration_s'] = time.perf_counter() - start
            self.spans.append(record)

    def slowest(self, count=10):
        return sorted(self.spans, key=lambda s: s['duration_s'], reverse=True)[:count]
