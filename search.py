"""Backtracking and Branch & Bound: N-Queens, Hamiltonian cycle, TSP.
Every function ticks ctr 'states' (nodes of the search tree) and counts 'pruned' branches."""
import heapq
import sys

sys.setrecursionlimit(10000)
INF = float("inf")


def nqueens(n, ctr, find_all=False):
    """Backtracking with column + diagonal pruning. Returns (num_solutions_found, first_solution)."""
    cols, d1, d2 = [False] * n, [False] * (2 * n), [False] * (2 * n)
    pos, state = [], {"count": 0, "first": None}

    def place(r):
        ctr.tick("states")
        if r == n:
            state["count"] += 1
            if state["first"] is None:
                state["first"] = pos[:]
            return not find_all
        for c in range(n):
            if cols[c] or d1[r + c] or d2[r - c + n]:
                ctr.inc("pruned")
                continue
            cols[c] = d1[r + c] = d2[r - c + n] = True
            pos.append(c)
            if place(r + 1):
                return True
            pos.pop()
            cols[c] = d1[r + c] = d2[r - c + n] = False
        return False

    place(0)
    return state["count"], state["first"]


def hamiltonian_cycle(adj, ctr, degree_prune=False):
    """Backtracking search for a Hamiltonian cycle. adj = list of neighbour collections.
    degree_prune=True adds a cheap necessary-condition check (every vertex needs degree >= 2)."""
    n = len(adj)
    if n < 3:
        return None
    nbrs = [sorted(a) for a in adj]
    if degree_prune and any(len(a) < 2 for a in nbrs):
        ctr.inc("pruned")
        return None
    path, visited = [0], [False] * n
    visited[0] = True
    adjset = [set(a) for a in nbrs]

    def extend():
        ctr.tick("states")
        last = path[-1]
        if len(path) == n:
            if 0 in adjset[last]:
                return True
            ctr.inc("pruned")
            return False
        for v in nbrs[last]:
            if visited[v]:
                ctr.inc("pruned")
                continue
            visited[v] = True
            path.append(v)
            if extend():
                return True
            path.pop()
            visited[v] = False
        return False

    return path[:] if extend() else None


def tsp_bruteforce(d, ctr):
    """Plain backtracking over all tours starting at city 0 (no bound). Theta((n-1)!)."""
    n = len(d)
    if n <= 1:
        return 0, [0] * n
    best, best_tour = [INF], [None]
    path, visited = [0], [False] * n
    visited[0] = True

    def dfs(cost):
        ctr.tick("states")
        last = path[-1]
        if len(path) == n:
            total = cost + d[last][0]
            if total < best[0]:
                best[0], best_tour[0] = total, path[:]
            return
        for v in range(n):
            if not visited[v]:
                visited[v] = True
                path.append(v)
                dfs(cost + d[last][v])
                path.pop()
                visited[v] = False
    dfs(0)
    return best[0], best_tour[0]


def _nearest_neighbour(d):
    n = len(d)
    tour, seen, cost = [0], {0}, 0
    while len(tour) < n:
        last = tour[-1]
        v = min((u for u in range(n) if u not in seen), key=lambda u: d[last][u])
        cost += d[last][v]
        tour.append(v)
        seen.add(v)
    return cost + d[tour[-1]][0], tour


def tsp_branch_and_bound(d, ctr):
    """Best-first Branch & Bound. Lower bound = cost so far + cheapest edge INTO every unvisited city
    + cheapest edge into the start city. Initial upper bound from nearest-neighbour.
    Records states generated, states pruned and the maximum priority-queue size."""
    n = len(d)
    if n <= 1:
        return 0, [0] * n
    minin = [min(d[u][v] for u in range(n) if u != v) for v in range(n)]
    best, best_tour = _nearest_neighbour(d)
    rem0 = sum(minin[1:])
    heap, tie = [(rem0 + minin[0], 0, 0, (0,), 1, rem0)], 0
    ctr.tick("states")
    ctr.set_max("max_queue", 1)
    while heap:
        lb, _, cost, path, mask, rem = heapq.heappop(heap)
        if lb >= best:
            ctr.inc("pruned", len(heap))      # everything left in the queue is bounded out
            break
        last = path[-1]
        for v in range(n):
            if mask >> v & 1:
                continue
            c = cost + d[last][v]
            ctr.tick("states")
            if len(path) + 1 == n:
                total = c + d[v][0]
                if total < best:
                    best, best_tour = total, list(path) + [v]
                continue
            nrem = rem - minin[v]
            nlb = c + nrem + minin[0]
            if nlb >= best:
                ctr.inc("pruned")
                continue
            tie += 1
            heapq.heappush(heap, (nlb, tie, c, path + (v,), mask | 1 << v, nrem))
            ctr.set_max("max_queue", len(heap))
    return best, best_tour
