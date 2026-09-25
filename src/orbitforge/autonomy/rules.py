from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Rule:
    name: str
    metric: str
    operator: str
    threshold: float
    action: str
    priority: int = 0


def matches(rule, metrics):
    if rule.metric not in metrics:
        return False
    value = metrics[rule.metric]
    if rule.operator == '<':
        return value < rule.threshold
    if rule.operator == '<=':
        return value <= rule.threshold
    if rule.operator == '>':
        return value > rule.threshold
    if rule.operator == '>=':
        return value >= rule.threshold
    if rule.operator == '==':
        return value == rule.threshold
    raise ValueError('unsupported rule operator')


def evaluate_rules(rules, metrics):
    fired = [rule for rule in rules if matches(rule, metrics)]
    fired.sort(key=lambda r: (-r.priority, r.name))
    return fired


def selected_action(rules, metrics):
    fired = evaluate_rules(rules, metrics)
    return fired[0].action if fired else None
