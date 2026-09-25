from __future__ import annotations
from bisect import bisect_right
from .interpolation import EphemerisPoint, hermite

class EphemerisSeries:

    def __init__(self, points):
        self.points = sorted(points, key=lambda p: p.t)
        self.times = [p.t for p in self.points]
        if any((b <= a for a, b in zip(self.times, self.times[1:]))):
            raise ValueError('strict times required')

    def at(self, t):
        if t < self.times[0] or t > self.times[-1]:
            raise ValueError('outside ephemeris')
        i = max(0, min(len(self.points) - 2, bisect_right(self.times, t) - 1))
        return hermite(self.points[i], self.points[i + 1], t)

    def span(self):
        return (self.times[0], self.times[-1])
