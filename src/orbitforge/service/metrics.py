from __future__ import annotations
from collections import defaultdict

class Metrics:
    def __init__(self):
        self.counters = defaultdict(float)
        self.gauges = {}
        self.histograms = defaultdict(list)

    def inc(self, name, value=1.0):
        self.counters[name] += value

    def set(self, name, value):
        self.gauges[name] = value

    def observe(self, name, value):
        self.histograms[name].append(value)

    def snapshot(self):
        hist = {}
        for name, values in self.histograms.items():
            hist[name] = {
                'count': len(values),
                'min': min(values) if values else None,
                'max': max(values) if values else None,
                'mean': sum(values) / len(values) if values else None,
            }
        return {'counters': dict(self.counters), 'gauges': dict(self.gauges), 'histograms': hist}
