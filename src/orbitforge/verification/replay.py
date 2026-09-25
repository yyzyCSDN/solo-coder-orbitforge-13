from __future__ import annotations

def replay(events, reducer, initial_state):
    state = initial_state
    versions = []
    for index, event in enumerate(events, 1):
        state = reducer(state, event)
        versions.append((index, state))
    return state, versions

def compare_replays(events, reducer_a, reducer_b, initial_state):
    state_a, versions_a = replay(events, reducer_a, initial_state)
    state_b, versions_b = replay(events, reducer_b, initial_state)
    first_difference = None
    for a, b in zip(versions_a, versions_b):
        if a[1] != b[1]:
            first_difference = a[0]
            break
    return {'equal': state_a == state_b, 'first_difference': first_difference, 'a': state_a, 'b': state_b}
