from __future__ import annotations
import bisect, math

class HorizonMask:

    def __init__(self, points):
        pts = sorted(((a % (2 * math.pi), e) for a, e in points))
        self.az = [p[0] for p in pts]
        self.el = [p[1] for p in pts]

    def elevation_limit(self, az):
        if not self.az:
            return -math.pi / 2
        az %= 2 * math.pi
        i = bisect.bisect_right(self.az, az)
        i0 = (i - 1) % len(self.az)
        i1 = i % len(self.az)
        a0 = self.az[i0]
        a1 = self.az[i1]
        if i1 == 0:
            a1 += 2 * math.pi
        aa = az if az >= a0 else az + 2 * math.pi
        u = (aa - a0) / (a1 - a0) if a1 != a0 else 0
        return self.el[i0] * (1 - u) + self.el[i1] * u

    def clear(self, az, el):
        return el >= self.elevation_limit(az)
