from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class TraceNode:
    name: str
    passed: bool
    value: object
    source: str
    parents: tuple[str, ...] = ()

def explain(nodes, target):
    table = {n.name: n for n in nodes}
    ordered = []
    seen = set()
    def visit(name):
        if name in seen:
            return
        seen.add(name)
        node = table[name]
        for parent in node.parents:
            visit(parent)
        ordered.append(node)
    visit(target)
    return ordered

def failing_ancestors(nodes, target):
    return [node for node in explain(nodes, target) if not node.passed]

def trace_summary(nodes, target):
    path = explain(nodes, target)
    return {'target': target, 'passed': path[-1].passed, 'nodes': [n.name for n in path], 'failed': [n.name for n in path if not n.passed]}
