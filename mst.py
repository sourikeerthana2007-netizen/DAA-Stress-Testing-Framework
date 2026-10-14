"""MST algorithms. Graph = (V, edges) with edges as (u, v, w). Each function returns (total_weight, edges_used).
The representation (edge list / adjacency list / adjacency matrix) is built INSIDE the call so its cost is measured."""
import heapq
from functools import cmp_to_key

INF = float("inf")


def kruskal(V, edges, ctr):
    """Sort edges + union-find. O(E log E). Returns a spanning forest if the graph is disconnected."""
    def cmp(a, b):
        ctr.inc("sort_comparisons")
        return (a[2] > b[2]) - (a[2] < b[2])
    ordered = sorted(edges, key=cmp_to_key(cmp))
    parent, rank = list(range(V)), [0] * V
    steps = 0

    def find(x):
        nonlocal steps
        root = x
        while parent[root] != root:
            root = parent[root]
            steps += 1
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    total, used = 0, 0
    for u, v, w in ordered:
        ru, rv = find(u), find(v)
        ctr.inc("uf_finds", 2)
        if ru != rv:
            if rank[ru] < rank[rv]:
                ru, rv = rv, ru
            parent[rv] = ru
            if rank[ru] == rank[rv]:
                rank[ru] += 1
            total += w
            used += 1
            ctr.inc("uf_unions")
            if used == V - 1:
                break
    ctr.inc("uf_steps", steps)
    return total, used


def prim_heap(V, edges, ctr):
    """Lazy Prim with a binary heap on an adjacency list. O(E log V). Covers vertex 0's component."""
    if V == 0:
        return 0, 0
    adj = [[] for _ in range(V)]
    for u, v, w in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))
    ctr.inc("adj_build", 2 * len(edges))
    seen = [False] * V
    heap = [(0, 0)]
    ctr.inc("heap_push")
    total, used = 0, -1
    while heap:
        w, u = heapq.heappop(heap)
        ctr.inc("heap_pop")
        if seen[u]:
            ctr.inc("stale_pops")
            continue
        seen[u] = True
        total += w
        used += 1
        for item in adj[u]:
            ctr.inc("edge_scans")
            if not seen[item[1]]:
                heapq.heappush(heap, item)
                ctr.inc("heap_push")
    return total, used


def prim_matrix(V, edges, ctr):
    """Array-based Prim on an adjacency matrix. O(V^2) whatever the number of edges."""
    if V == 0:
        return 0, 0
    M = [[INF] * V for _ in range(V)]
    ctr.inc("matrix_cells", V * V)
    for u, v, w in edges:
        if w < M[u][v]:
            M[u][v] = M[v][u] = w
    key, in_tree = [INF] * V, [False] * V
    key[0] = 0
    total, used = 0, -1
    for _ in range(V):
        best, u = INF, -1
        for v in range(V):               # scan for the cheapest fringe vertex
            if not in_tree[v] and key[v] < best:
                best, u = key[v], v
        ctr.inc("key_scans", V)
        if u == -1:
            break                        # remaining vertices unreachable
        in_tree[u] = True
        total += best
        used += 1
        row = M[u]
        for v in range(V):
            if not in_tree[v] and row[v] < key[v]:
                key[v] = row[v]
        ctr.inc("matrix_reads", V)
    return total, used
