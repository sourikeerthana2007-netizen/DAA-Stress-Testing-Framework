"""Knapsack variants. items = list of (value, weight)."""
from functools import cmp_to_key
from metrics import BudgetExceeded


def _check(items, W):
    if W < 0 or any(w < 0 or v < 0 for v, w in items):
        raise ValueError("values, weights and capacity must be non-negative")


def fractional_knapsack(items, W, ctr):
    """Greedy by value/weight ratio. Optimal for the FRACTIONAL problem. O(n log n)."""
    _check(items, W)

    def cmp(a, b):  # ratio compare by cross-multiplication (handles weight 0)
        ctr.inc("sort_comparisons")
        x, y = a[0] * b[1], b[0] * a[1]
        return (x < y) - (x > y)           # larger ratio first
    order = sorted(items, key=cmp_to_key(cmp))
    value, room = 0.0, W
    for v, w in order:
        ctr.inc("greedy_steps")
        if w <= room:
            value += v
            room -= w
        else:
            value += v * room / w
            break
    return value


def greedy_01_by_ratio(items, W):
    """The SAME greedy applied to 0/1 knapsack (items indivisible). NOT optimal - used to show why."""
    _check(items, W)
    value, room = 0, W
    for v, w in sorted(items, key=lambda it: (-(it[0] / it[1]) if it[1] else float("-inf"))):
        if w <= room:
            value += v
            room -= w
    return value


def knapsack_01_dp(items, W, ctr):
    """Bottom-up DP table of (n+1) x (W+1) cells: O(nW) time AND space - pseudo-polynomial in W.
    Returns (best_value, chosen_indices)."""
    _check(items, W)
    n = len(items)
    need = (n + 1) * (W + 1)
    if ctr.state_limit is not None and need > ctr.state_limit:
        raise BudgetExceeded(f"DP table needs {need:,} cells (> budget {ctr.state_limit:,})")
    prev = [0] * (W + 1)
    table = [prev]
    for v, w in items:
        if w > W:
            row = prev[:]
        else:
            row = prev[:w] + [max(prev[c], prev[c - w] + v) for c in range(w, W + 1)]
        ctr.inc("cells", W + 1)
        table.append(row)
        prev = row
    chosen, c = [], W
    for i in range(n, 0, -1):
        if table[i][c] != table[i - 1][c]:
            chosen.append(i - 1)
            c -= items[i - 1][1]
    chosen.reverse()
    return table[n][W], chosen
