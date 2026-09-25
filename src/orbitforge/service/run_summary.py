from __future__ import annotations

def summarize(records):
    by_analysis = {}
    for record in records:
        row = by_analysis.setdefault(record.analysis, {'total': 0, 'succeeded': 0, 'failed': 0, 'duration_s': 0.0})
        row['total'] += 1
        row['duration_s'] += record.duration_s
        if record.status == 'succeeded':
            row['succeeded'] += 1
        if record.status == 'failed':
            row['failed'] += 1
    for row in by_analysis.values():
        row['mean_duration_s'] = row['duration_s'] / row['total'] if row['total'] else 0.0
    return by_analysis

def failure_hotspots(records, minimum_failures=1):
    summary = summarize(records)
    return sorted(((name, row['failed']) for name, row in summary.items() if row['failed'] >= minimum_failures), key=lambda item: (-item[1], item[0]))
