"""All experiments, grouped by the six mandatory test families.
Each experiment = generator + runner + theoretical bound (see framework.Experiment)."""
import math

import dp as D
import generators as G
import knapsack as K
import mst as M
import search as Q
import structures as S
from framework import Experiment
from metrics import Counter


def lg(x):
    return math.log2(x) if x > 1 else 1.0


# ===================================================================== Family 1
F1 = "1. Advanced data structures"


def _heap_sort_exp(name, cls, ops_keys):
    def make(n, rng):
        return G.shuffled_keys(n, rng), {}

    def run(keys, ctr):
        h = cls(ctr)
        for k in keys:
            h.insert(k)
        while h.size:
            h.extract_min()
    return Experiment(F1, name, [1000, 2000, 4000, 8000, 16000], make, run,
                      "O(n log n) for n inserts + n extract-mins", lambda m: m["n"] * lg(m["n"]),
                      ops_keys=ops_keys)


def _decrease_key_exp(name, cls, ops_keys, theory_label, theory):
    def make(n, rng):
        return (G.shuffled_keys(n, rng), rng.sample(range(n), n // 2)), {}

    def prepare(inp):
        keys, idx = inp
        h = cls(Counter())
        nodes = {k: h.insert(k) for k in keys}
        nodes.pop(h.extract_min())        # one extract-min builds the real tree shape
        return h, [nodes[keys[i]] for i in idx if keys[i] in nodes]

    def run(state, ctr):
        h, targets = state
        h.ctr = ctr
        for j, node in enumerate(targets):
            h.decrease_key(node, -(j + 1))   # smaller than everything -> worst case for bubbling up
    return Experiment(F1, name, [1000, 2000, 4000, 8000, 16000], make, run, theory_label, theory,
                      ops_keys=ops_keys, prepare=prepare)


def _merge_exp(name, cls, ops_keys, theory_label, theory):
    def make(n, rng):
        return (G.shuffled_keys(n, rng)), {}

    def prepare(keys):
        a, b = cls(Counter()), cls(Counter())
        half = len(keys) // 2
        for k in keys[:half]:
            a.insert(k)
        for k in keys[half:]:
            b.insert(k)
        return a, b

    def run(state, ctr):
        a, b = state
        a.ctr = b.ctr = ctr
        a.merge(b)
    return Experiment(F1, name, [2000, 8000, 32000, 64000], make, run, theory_label, theory,
                      ops_keys=ops_keys, prepare=prepare)


def _tree_exp(name, cls, order, sizes, ops_keys, theory_label, theory, theory_class="poly"):
    def make(n, rng):
        ks = list(range(n))
        if order == "random":
            rng.shuffle(ks)
        elif order == "reverse":
            ks.reverse()
        return ks, {}

    def run(keys, ctr):
        t = cls(ctr)
        for k in keys:
            t.insert(k)
        ctr.set_max("final_height", t.height())
        for k in keys[::10]:
            if hasattr(t, "search"):
                t.search(k)
    return Experiment(F1, name, sizes, make, run, theory_label, theory, theory_class, ops_keys=ops_keys)


def _btree_exp(t):
    def make(n, rng):
        return G.shuffled_keys(n, rng), {}

    def run(keys, ctr):
        tree = S.BTree(t, ctr)
        for k in keys:
            tree.insert(k)
        ctr.set_max("final_height", tree.height())
        for k in keys[::10]:
            tree.search(k)
    return Experiment(F1, f"B-Tree (t={t}): random inserts", [1000, 2000, 4000, 8000, 16000, 32000], make, run,
                      f"O(n log_{t} n) node accesses", lambda m: m["n"] * math.log(max(m["n"], 2), t),
                      ops_keys=("node_accesses",))


def family1():
    heap_keys_b = ("links", "comparisons")
    return [
        _heap_sort_exp("Binomial heap: n inserts + n extract-mins", S.BinomialHeap, heap_keys_b),
        _heap_sort_exp("Fibonacci heap: n inserts + n extract-mins", S.FibonacciHeap, heap_keys_b),
        _decrease_key_exp("Binomial heap: n/2 decrease-keys", S.BinomialHeap, ("swaps",),
                          "O(log n) per decrease-key", lambda m: (m["n"] // 2) * lg(m["n"])),
        _decrease_key_exp("Fibonacci heap: n/2 decrease-keys", S.FibonacciHeap, ("cuts",),
                          "O(1) amortised per decrease-key", lambda m: m["n"] // 2),
        _merge_exp("Binomial heap: merge two heaps", S.BinomialHeap, ("links", "comparisons"),
                   "O(log n)", lambda m: lg(m["n"])),
        _merge_exp("Fibonacci heap: merge two heaps", S.FibonacciHeap, ("splices",),
                   "O(1)", lambda m: 1),
        _tree_exp("Red-Black tree: random inserts", S.RedBlackTree, "random", [1000, 2000, 4000, 8000, 16000, 32000],
                  ("comparisons", "rotations", "recolors"), "O(n log n)", lambda m: m["n"] * lg(m["n"])),
        _tree_exp("Red-Black tree: SORTED inserts", S.RedBlackTree, "sorted", [1000, 2000, 4000, 8000, 16000, 32000],
                  ("comparisons", "rotations", "recolors"), "O(n log n)", lambda m: m["n"] * lg(m["n"])),
        _tree_exp("Naive BST: random inserts", S.NaiveBST, "random", [1000, 2000, 4000, 8000, 16000],
                  ("comparisons",), "O(n log n) expected", lambda m: m["n"] * lg(m["n"])),
        _tree_exp("Naive BST: SORTED inserts (degenerate)", S.NaiveBST, "sorted", [500, 1000, 2000, 4000, 8000],
                  ("comparisons",), "O(n^2)", lambda m: m["n"] ** 2 / 2),
        _btree_exp(2),
        _btree_exp(32),
    ]


# ===================================================================== Family 2
F2 = "2. MST algorithms"


def _mst_exp(kind, algo):
    funcs = {"Kruskal": M.kruskal, "Prim (heap)": M.prim_heap, "Prim (matrix)": M.prim_matrix}
    keys = {"Kruskal": ("sort_comparisons", "uf_steps"),
            "Prim (heap)": ("heap_push", "heap_pop", "edge_scans"),
            "Prim (matrix)": ("matrix_cells", "key_scans", "matrix_reads")}
    theory = {"Kruskal": ("O(E log E)", lambda m: m["E"] * lg(m["E"])),
              "Prim (heap)": ("O(E) heap ops, each O(log V)", lambda m: m["E"]),
              "Prim (matrix)": ("O(V^2)", lambda m: m["V"] ** 2)}
    sizes = [100, 200, 400, 800, 1600] if kind == "sparse" else [50, 100, 200, 400, 800]

    def make(V, rng):
        E = 2 * V if kind == "sparse" else V * (V - 1) // 4
        edges = G.random_connected_graph(V, E, rng)
        return (V, edges), {"V": V, "E": len(edges)}

    def run(g, ctr):
        funcs[algo](g[0], g[1], ctr)
    label, fn = theory[algo]
    dens = "sparse E=2V" if kind == "sparse" else "dense E~V^2/4"
    return Experiment(F2, f"{algo} on {dens} graphs", sizes, make, run, label, fn, ops_keys=keys[algo])


def family2():
    return [_mst_exp(k, a) for k in ("sparse", "dense") for a in ("Kruskal", "Prim (heap)", "Prim (matrix)")]


# ===================================================================== Family 3
F3 = "3. Knapsack"


def family3():
    def items_make(n, rng):
        items = G.knapsack_items(n, rng)
        return (items, sum(w for _, w in items) // 2), {}

    frac = Experiment(F3, "Fractional knapsack (greedy) as n grows", [1000, 4000, 16000, 64000], items_make,
                      lambda inp, ctr: K.fractional_knapsack(inp[0], inp[1], ctr),
                      "O(n log n)", lambda m: m["n"] * lg(m["n"]), ops_keys=("sort_comparisons",))

    def dp_n_make(n, rng):
        return (G.knapsack_items(n, rng), 2000), {"W": 2000}
    dp_n = Experiment(F3, "0/1 knapsack (DP), n grows, W=2000", [50, 100, 200, 400, 800], dp_n_make,
                      lambda inp, ctr: K.knapsack_01_dp(inp[0], inp[1], ctr),
                      "O(nW) time and space", lambda m: m["n"] * (m["W"] + 1), ops_keys=("cells",),
                      state_limit=10_000_000)

    def dp_w_make(W, rng):
        return (G.knapsack_items(100, rng), W), {"W": W}
    dp_w = Experiment(F3, "0/1 knapsack (DP), n=100, CAPACITY W grows", [500, 2000, 8000, 32000, 128000], dp_w_make,
                      lambda inp, ctr: K.knapsack_01_dp(inp[0], inp[1], ctr),
                      "O(nW): pseudo-polynomial in W", lambda m: 101 * (m["W"] + 1), ops_keys=("cells",),
                      state_limit=5_000_000)
    return [frac, dp_n, dp_w]


def knapsack_demo():
    """Matched dataset: same items, two problems. Shows why greedy works for fractional but not 0/1."""
    items, W = [(60, 10), (100, 20), (120, 30)], 50
    c = Counter
    frac = K.fractional_knapsack(items, W, c())
    greedy = K.greedy_01_by_ratio(items, W)
    best, chosen = K.knapsack_01_dp(items, W, c())
    return {"items(value,weight)": items, "capacity": W, "fractional_greedy_value": frac,
            "greedy_on_0/1_value": greedy, "0/1_DP_optimal_value": best, "0/1_DP_items": chosen}


# ===================================================================== Family 4
F4 = "4. Dynamic programming"


def family4():
    fw = Experiment(F4, "Floyd-Warshall as vertex count grows", [25, 50, 100, 150],
                    lambda V, rng: (G.complete_weight_matrix(V, rng), {"V": V}),
                    lambda d, ctr: D.floyd_warshall(d, ctr),
                    "Theta(V^3) time, Theta(V^2) space", lambda m: m["V"] ** 3, ops_keys=("inner_iterations",))
    mcm = Experiment(F4, "Matrix-chain multiplication as chain length grows", [25, 50, 100, 200],
                     lambda n, rng: (G.chain_dims(n, rng), {}),
                     lambda dims, ctr: D.matrix_chain(dims, ctr),
                     "Theta(n^3) time, Theta(n^2) space", lambda m: m["n"] ** 3 / 6, ops_keys=("inner_iterations",))
    return [fw, mcm]


# ===================================================================== Family 5
F5 = "5. Backtracking / Branch & Bound"


def family5():
    factorial = lambda m: math.factorial(m["n"])
    nq_all = Experiment(F5, "N-Queens: enumerate ALL solutions", [6, 7, 8, 9, 10, 11, 12],
                        lambda n, rng: (n, {}), lambda n, ctr: Q.nqueens(n, ctr, find_all=True),
                        "O(n!) worst case, pruned by diagonals", factorial, "exp", ops_keys=("states",),
                        state_limit=3_000_000)
    nq_one = Experiment(F5, "N-Queens: find the FIRST solution", [8, 12, 16, 20, 24],
                        lambda n, rng: (n, {}), lambda n, ctr: Q.nqueens(n, ctr, find_all=False),
                        "O(n!) worst case", factorial, "exp", ops_keys=("states",), state_limit=3_000_000)

    ham_hard = Experiment(F5, "Hamiltonian: no-cycle graph (K_{n-1}+pendant), plain backtracking", [6, 7, 8, 9, 10, 11, 12],
                          lambda n, rng: (G.hamiltonian_hard(n), {}),
                          lambda adj, ctr: Q.hamiltonian_cycle(adj, ctr),
                          "O(n!) worst case", factorial, "exp", ops_keys=("states",), state_limit=2_000_000)
    ham_fix = Experiment(F5, "Hamiltonian: SAME graphs + degree>=2 pruning", [6, 8, 10, 12, 20, 40],
                         lambda n, rng: (G.hamiltonian_hard(n), {}),
                         lambda adj, ctr: Q.hamiltonian_cycle(adj, ctr, degree_prune=True),
                         "O(n) pre-check", lambda m: m["n"], "poly", ops_keys=("states", "pruned"))
    ham_sparse = Experiment(F5, "Hamiltonian: sparse random graph WITH a cycle (n extra chords)", [10, 14, 18, 22, 26],
                            lambda n, rng: (G.hamiltonian_planted(n, n, rng), {}),
                            lambda adj, ctr: Q.hamiltonian_cycle(adj, ctr),
                            "O(n!) worst case", factorial, "exp", ops_keys=("states",), state_limit=2_000_000)

    def tsp_make(kind):
        return lambda n, rng: (G.tsp_matrix(n, rng, kind), {})
    tsp_brute = Experiment(F5, "TSP: brute-force backtracking (no bound)", [5, 6, 7, 8, 9, 10, 11],
                           tsp_make("euclid"), lambda d, ctr: Q.tsp_bruteforce(d, ctr),
                           "O((n-1)!)", lambda m: math.factorial(m["n"] - 1), "exp",
                           ops_keys=("states",), state_limit=3_000_000)
    tsp_bb_e = Experiment(F5, "TSP: Branch & Bound, Euclidean instances", [8, 10, 12, 14, 16, 18],
                          tsp_make("euclid"), lambda d, ctr: Q.tsp_branch_and_bound(d, ctr),
                          "exponential worst case", lambda m: math.factorial(m["n"] - 1), "exp",
                          ops_keys=("states",), state_limit=1_500_000)
    tsp_bb_u = Experiment(F5, "TSP: Branch & Bound, random-weight instances (weaker bound)", [8, 10, 12, 14, 16],
                          tsp_make("uniform"), lambda d, ctr: Q.tsp_branch_and_bound(d, ctr),
                          "exponential worst case", lambda m: math.factorial(m["n"] - 1), "exp",
                          ops_keys=("states",), state_limit=1_500_000)
    return [nq_all, nq_one, ham_hard, ham_fix, ham_sparse, tsp_brute, tsp_bb_e, tsp_bb_u]


# ===================================================================== registry
FAMILIES = {1: family1, 2: family2, 3: family3, 4: family4, 5: family5}   # family 6 = complexity.py
