from __future__ import annotations

class SimulationClock:
    def __init__(self, start_tai_s=0.0, rate=1.0):
        self.tai_s = float(start_tai_s)
        self.rate = float(rate)
        self.paused = False

    def advance_wall(self, wall_seconds):
        if wall_seconds < 0.0:
            raise ValueError('negative wall time')
        if not self.paused:
            self.tai_s += wall_seconds * self.rate
        return self.tai_s

    def jump(self, target_tai_s):
        self.tai_s = float(target_tai_s)
        return self.tai_s

    def set_rate(self, rate):
        if rate < 0.0:
            raise ValueError('negative simulation rate')
        self.rate = float(rate)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
