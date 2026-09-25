from __future__ import annotations

def margin_statistics(samples):
    values = [row['margin_db'] for row in samples]
    if not values:
        return {'count': 0, 'min_db': None, 'mean_db': None, 'outage_fraction': 1.0}
    return {
        'count': len(values),
        'min_db': min(values),
        'mean_db': sum(values) / len(values),
        'outage_fraction': sum(1 for x in values if x < 0.0) / len(values),
    }

def fade_events(samples, threshold_db=0.0):
    events = []
    start = None
    for row in samples:
        faded = row['margin_db'] < threshold_db
        if faded and start is None:
            start = row['t']
        if not faded and start is not None:
            events.append((start, row['t']))
            start = None
    if start is not None and samples:
        events.append((start, samples[-1]['t']))
    return events

def throughput_mb(samples):
    total_bits = 0.0
    for a, b in zip(samples, samples[1:]):
        total_bits += max(0.0, b['t'] - a['t']) * max(0.0, a.get('bitrate_bps', 0.0))
    return total_bits / 8e6
