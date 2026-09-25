from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class FaultNode:
    name: str
    kind: str
    children: tuple[str, ...] = ()


def evaluate(nodes, basic_events):
    table = {n.name: n for n in nodes}
    cache = {}
    visiting = set()
    def visit(name):
        if name in cache:
            return cache[name]
        if name in visiting:
            raise ValueError('fault tree cycle')
        visiting.add(name)
        node = table[name]
        if node.kind == 'basic':
            value = bool(basic_events.get(name, False))
        else:
            values = [visit(child) for child in node.children]
            if node.kind == 'and':
                value = all(values)
            elif node.kind == 'or':
                value = any(values)
            else:
                raise ValueError('unknown fault gate')
        visiting.remove(name)
        cache[name] = value
        return value
    return {name: visit(name) for name in table}


def top_event(nodes, basic_events, name):
    return evaluate(nodes, basic_events)[name]
