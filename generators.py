"""Input generators for every test family (all seeded through the rng argument)."""
import math

INF = float("inf")


def shuffled_keys(n, rng):
    ks = list(range(n))
    rng.shuffle(ks)
    return ks


def random_connected_graph(V, E, rng):
    """Random connected simple graph: random spanning tree + random extra edges. Returns [(u, v, w)]."""
    if V <= 1:
        return []
    E = min(max(E, V - 1), V * (V - 1) // 2)
    seen, order = set(), list(range(V))
    rng.shuffle(order)
    for i in range(1, V):
        u, v = order[i], order[rng.randrange(i)]
        seen.add((min(u, v), max(u, v)))
    while len(seen) < E:
        u, v = rng.randrange(V), rng.randrange(V)
        if u != v:
            seen.add((min(u, v), max(u, v)))
    hi = 10 * len(seen)
    return [(u, v, rng.randint(1, hi)) for u, v in seen]


def knapsack_items(n, rng, max_value=1000, max_weight=100):
    return [(rng.randint(1, max_value), rng.randint(1, max_weight)) for _ in range(n)]


def complete_weight_matrix(V, rng, hi=100):
    return [[0 if i == j else rng.randint(1, hi) for j in range(V)] for i in range(V)]


def chain_dims(n, rng):
    return [rng.randint(5, 100) for _ in range(n + 1)]


def hamiltonian_hard(n):
    """K_{n-1} plus one pendant vertex: NO Hamiltonian cycle, yet naive backtracking explores ~(n-2)! paths."""
    adj = [set() for _ in range(n)]
    for u in range(n - 1):
        for v in range(n - 1):
            if u != v:
                adj[u].add(v)
    adj[n - 1].add(0)
    adj[0].add(n - 1)
    return adj


def hamiltonian_planted(n, extra_edges, rng):
    """A Hamiltonian cycle on a random permutation plus extra random chords."""
    adj = [set() for _ in range(n)]
    perm = list(range(n))
    rng.shuffle(perm)
    for i in range(n):
        a, b = perm[i], perm[(i + 1) % n]
        adj[a].add(b)
        adj[b].add(a)
    added = 0
    while added < extra_edges and n > 3:
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b and b not in adj[a]:
            adj[a].add(b)
            adj[b].add(a)
            added += 1
    return adj


def tsp_matrix(n, rng, kind="euclid"):
    """Symmetric integer distance matrix. 'euclid': random points; 'uniform': random edge weights (harder bound)."""
    if kind == "euclid":
        pts = [(rng.randint(0, 1000), rng.randint(0, 1000)) for _ in range(n)]
        return [[round(math.dist(p, q)) for q in pts] for p in pts]
    d = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d[i][j] = d[j][i] = rng.randint(1, 100)
    return d
