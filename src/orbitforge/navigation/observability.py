from __future__ import annotations
import math


def gram_matrix(rows):
    if not rows:
        return []
    n = len(rows[0])
    return [[sum(row[i] * row[j] for row in rows) for j in range(n)] for i in range(n)]

def determinant_2x2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]

def condition_proxy(rows):
    gram = gram_matrix(rows)
    if not gram:
        return float('inf')
    diagonal = [gram[i][i] for i in range(len(gram))]
    positive = [x for x in diagonal if x > 1e-15]
    if not positive:
        return float('inf')
    return max(positive) / min(positive)

def rank_proxy(rows, tolerance=1e-10):
    work = [list(row) for row in rows]
    if not work:
        return 0
    rank = 0
    col = 0
    while rank < len(work) and col < len(work[0]):
        pivot = max(range(rank, len(work)), key=lambda r: abs(work[r][col]))
        if abs(work[pivot][col]) <= tolerance:
            col += 1
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][col]
        work[rank] = [x / scale for x in work[rank]]
        for r in range(len(work)):
            if r != rank:
                factor = work[r][col]
                work[r] = [work[r][c] - factor * work[rank][c] for c in range(len(work[0]))]
        rank += 1
        col += 1
    return rank
