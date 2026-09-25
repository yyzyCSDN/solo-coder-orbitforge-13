from __future__ import annotations

def topological_order(nodes, edges):
    incoming = {node: 0 for node in nodes}
    outgoing = {node: [] for node in nodes}
    for source, target in edges:
        if source not in incoming or target not in incoming:
            raise ValueError('edge references unknown node')
        outgoing[source].append(target)
        incoming[target] += 1
    ready = sorted(node for node, degree in incoming.items() if degree == 0)
    order = []
    while ready:
        node = ready.pop(0)
        order.append(node)
        for target in outgoing[node]:
            incoming[target] -= 1
            if incoming[target] == 0:
                ready.append(target)
                ready.sort()
    if len(order) != len(nodes):
        raise ValueError('dependency cycle')
    return order

def transitive_dependencies(target, edges):
    parents = {}
    for source, child in edges:
        parents.setdefault(child, set()).add(source)
    seen = set()
    stack = list(parents.get(target, ()))
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(parents.get(node, ()))
    return seen
