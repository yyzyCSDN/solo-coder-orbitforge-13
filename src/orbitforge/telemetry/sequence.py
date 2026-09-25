from __future__ import annotations
MODULUS = 1 << 14


def forward_distance(previous, current):
    return (current - previous) % MODULUS


def classify(previous, current):
    distance = forward_distance(previous, current)
    if distance == 0:
        return 'duplicate'
    if distance == 1:
        return 'next'
    if distance < MODULUS // 2:
        return 'gap'
    return 'old'


def missing_sequences(previous, current, limit=1024):
    distance = forward_distance(previous, current)
    if distance <= 1 or distance >= MODULUS // 2:
        return []
    count = min(distance - 1, limit)
    return [((previous + i) % MODULUS) for i in range(1, count + 1)]
