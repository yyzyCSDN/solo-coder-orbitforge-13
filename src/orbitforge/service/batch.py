from __future__ import annotations
from dataclasses import dataclass

@dataclass
class BatchResult:
    completed: list
    failed: list


def run_batch(items, worker, continue_on_error=True):
    completed = []
    failed = []
    for item in items:
        try:
            completed.append((item, worker(item)))
        except Exception as exc:
            failed.append((item, type(exc).__name__, str(exc)))
            if not continue_on_error:
                break
    return BatchResult(completed, failed)

def success_fraction(result):
    total = len(result.completed) + len(result.failed)
    return len(result.completed) / total if total else 1.0
