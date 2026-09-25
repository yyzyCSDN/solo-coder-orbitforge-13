from __future__ import annotations

def revisit_intervals(access_times):
    times = sorted(access_times)
    return [b - a for a, b in zip(times, times[1:])]

def revisit_statistics(access_times):
    intervals = revisit_intervals(access_times)
    if not intervals:
        return {'count': len(access_times), 'mean_s': None, 'max_s': None, 'p90_s': None}
    ordered = sorted(intervals)
    idx = int(0.9 * (len(ordered) - 1))
    return {'count': len(access_times), 'mean_s': sum(intervals) / len(intervals), 'max_s': max(intervals), 'p90_s': ordered[idx]}

def service_level(access_times, target_revisit_s):
    intervals = revisit_intervals(access_times)
    return 1.0 if not intervals else sum((1 for x in intervals if x <= target_revisit_s)) / len(intervals)
