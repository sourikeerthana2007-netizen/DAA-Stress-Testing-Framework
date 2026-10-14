"""Correctness tests (run: python -m unittest tests -v). Quote 'tests passed N / N' on the submission form."""
import itertools
import random
import unittest

import dp
import generators as G
import knapsack as K
import mst
import search as Q
import structures as S
from metrics import BudgetExceeded, Counter

INF = float("inf")


class TestHeaps(unittest.TestCase):
    def test_extract_sorted(self):
        for cls in (S.BinomialHeap, S.FibonacciHeap):
            rng = random.Random(1)
            ks = G.shuffled_keys(500, rng)
            h = cls()
            for k in ks:
                h.insert(k)
            self.assertEqual([h.extract_min() for _ in ks], sorted(ks), cls.__name__)
            self.assertIsNone(h.extract_min())          # empty heap

    def test_decrease_key(self):
        for cls in (S.BinomialHeap, S.FibonacciHeap):
            rng = random.Random(2)
            ks = G.shuffled_keys(300, rng)
            h = cls()
            nodes = {k: h.insert(k) for k in ks}
            h.extract_min()
            live = dict(nodes)
            live.pop(0)
            expected = set(ks) - {0}
            for j, k in enumerate(rng.sample(sorted(live), 100)):
                node = live[k]
                expected.discard(node.key)      # binomial heap swaps keys, so use the node's CURRENT key
                h.decrease_key(node, -(j + 1))
                expected.add(-(j + 1))
            out = [h.extract_min() for _ in range(len(expected))]
            self.assertEqual(out, sorted(expected), cls.__name__)

    def test_merge(self):
        for cls in (S.BinomialHeap, S.FibonacciHeap):
            a, b = cls(), cls()
            for k in range(0, 100, 2):
                a.insert(k)
            for k in range(1, 100, 2):
                b.insert(k)
            a.merge(b)
            self.assertEqual([a.extract_min() for _ in range(100)], list(range(100)), cls.__name__)

    def test_empty_and_single(self):
        for cls in (S.BinomialHeap, S.FibonacciHeap):
            h = cls()
            h.insert(7)
            self.assertEqual(h.extract_min(), 7)
            self.assertEqual(h.size, 0)


class TestTrees(unittest.TestCase):
    def test_red_black(self):
        for order in ("random", "sorted", "reverse"):
            ks = list(range(1000))
            if order == "random":
                random.Random(3).shuffle(ks)
            if order == "reverse":
                ks.reverse()
            t = S.RedBlackTree()
            for k in ks:
                t.insert(k)
            self.assertEqual(t.inorder(), sorted(ks))
            self.assertTrue(t.check_invariants(), order)
            self.assertLessEqual(t.height(), 2 * 10 + 1)  # 2*log2(n+1)
            self.assertTrue(all(t.search(k) for k in ks[:50]))
            self.assertFalse(t.search(-5))

    def test_btree(self):
        for t_deg in (2, 3, 16):
            ks = G.shuffled_keys(2000, random.Random(4))
            t = S.BTree(t_deg)
            for k in ks:
                t.insert(k)
            self.assertEqual(t.inorder(), sorted(ks))
            self.assertTrue(t.check_invariants(), t_deg)
            self.assertTrue(all(t.search(k) for k in ks[:100]))
            self.assertFalse(t.search(10 ** 9))
        with self.assertRaises(ValueError):
            S.BTree(1)

    def test_naive_bst_degenerates(self):
        c = Counter()
        t = S.NaiveBST(c)
        for k in range(300):
            t.insert(k)
        self.assertEqual(t.height(), 300)
        self.assertEqual(c["comparisons"], 300 * 299 // 2)


class TestMST(unittest.TestCase):
    def test_known_graph(self):
        edges = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4), (3, 4, 2), (4, 5, 6)]
        for f in (mst.kruskal, mst.prim_heap, mst.prim_matrix):
            self.assertEqual(f(6, edges, Counter()), (14, 5), f.__name__)

    def test_algorithms_agree(self):
        rng = random.Random(5)
        for V, E in [(2, 1), (10, 20), (50, 300), (80, 79), (40, 780)]:
            e = G.random_connected_graph(V, E, rng)
            res = {f.__name__: f(V, e, Counter()) for f in (mst.kruskal, mst.prim_heap, mst.prim_matrix)}
            self.assertEqual(len(set(res.values())), 1, res)

    def test_edge_cases(self):
        for f in (mst.kruskal, mst.prim_heap, mst.prim_matrix):
            self.assertEqual(f(0, [], Counter())[0], 0)
            self.assertEqual(f(1, [], Counter())[0], 0)
        # disconnected: Kruskal gives a forest, Prim spans vertex 0's component only
        e = [(0, 1, 5), (2, 3, 7)]
        self.assertEqual(mst.kruskal(4, e, Counter()), (12, 2))
        self.assertEqual(mst.prim_heap(4, e, Counter()), (5, 1))
        self.assertEqual(mst.prim_matrix(4, e, Counter()), (5, 1))


class TestKnapsack(unittest.TestCase):
    ITEMS, W = [(60, 10), (100, 20), (120, 30)], 50

    def test_matched_dataset(self):
        self.assertAlmostEqual(K.fractional_knapsack(self.ITEMS, self.W, Counter()), 240.0)
        self.assertEqual(K.greedy_01_by_ratio(self.ITEMS, self.W), 160)       # greedy FAILS on 0/1
        best, chosen = K.knapsack_01_dp(self.ITEMS, self.W, Counter())
        self.assertEqual((best, chosen), (220, [1, 2]))

    def test_dp_matches_bruteforce(self):
        rng = random.Random(6)
        for _ in range(30):
            items = G.knapsack_items(rng.randint(0, 9), rng, 50, 20)
            W = rng.randint(0, 60)
            brute = max(sum(items[i][0] for i in s) for r in range(len(items) + 1)
                        for s in itertools.combinations(range(len(items)), r)
                        if sum(items[i][1] for i in s) <= W)
            best, chosen = K.knapsack_01_dp(items, W, Counter())
            self.assertEqual(best, brute)
            self.assertEqual(sum(items[i][0] for i in chosen), best)
            self.assertLessEqual(sum(items[i][1] for i in chosen), W)
            self.assertGreaterEqual(K.fractional_knapsack(items, W, Counter()) + 1e-9, best)

    def test_edge_cases(self):
        self.assertEqual(K.knapsack_01_dp([], 10, Counter())[0], 0)
        self.assertEqual(K.knapsack_01_dp([(5, 3)], 0, Counter())[0], 0)       # W = 0
        self.assertEqual(K.knapsack_01_dp([(5, 30)], 10, Counter())[0], 0)     # item too heavy
        self.assertEqual(K.knapsack_01_dp([(5, 0), (1, 1)], 0, Counter())[0], 5)  # zero-weight item
        self.assertEqual(K.fractional_knapsack([(10, 0)], 5, Counter()), 10)
        with self.assertRaises(ValueError):
            K.knapsack_01_dp([(1, -1)], 5, Counter())

    def test_budget(self):
        with self.assertRaises(BudgetExceeded):
            K.knapsack_01_dp([(1, 1)] * 100, 10 ** 6, Counter(state_limit=1000))


class TestDP(unittest.TestCase):
    def test_floyd_warshall(self):
        rng = random.Random(7)
        n = 12
        d = [[0 if i == j else (rng.randint(1, 20) if rng.random() < 0.4 else INF) for j in range(n)] for i in range(n)]
        out = dp.floyd_warshall(d, c := Counter())
        self.assertEqual(c["inner_iterations"], n ** 3)
        # Bellman-Ford reference
        for s in range(n):
            dist = [INF] * n
            dist[s] = 0
            for _ in range(n):
                for u in range(n):
                    for v in range(n):
                        if dist[u] + d[u][v] < dist[v]:
                            dist[v] = dist[u] + d[u][v]
            self.assertEqual(out[s], dist)

    def test_matrix_chain(self):
        cost, par = dp.matrix_chain([30, 35, 15, 5, 10, 20, 25], c := Counter())
        self.assertEqual(cost, 15125)
        self.assertEqual(par, "((A1(A2A3))((A4A5)A6))")
        n = 40
        dp.matrix_chain([5] * (n + 1), c2 := Counter())
        self.assertEqual(c2["inner_iterations"], (n ** 3 - n) // 6)
        self.assertEqual(dp.matrix_chain([10], Counter())[0], 0)               # zero matrices


class TestSearch(unittest.TestCase):
    def test_nqueens_counts(self):
        known = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92}
        for n, cnt in known.items():
            self.assertEqual(Q.nqueens(n, Counter(), find_all=True)[0], cnt, n)
        count, sol = Q.nqueens(8, Counter())
        self.assertEqual(count, 1)
        self.assertTrue(all(abs(sol[i] - sol[j]) != j - i for i in range(8) for j in range(i + 1, 8)))

    def test_hamiltonian(self):
        K5 = [set(range(5)) - {i} for i in range(5)]
        cyc = Q.hamiltonian_cycle(K5, Counter())
        self.assertEqual(sorted(cyc), list(range(5)))
        self.assertIsNone(Q.hamiltonian_cycle(G.hamiltonian_hard(8), Counter()))
        self.assertIsNone(Q.hamiltonian_cycle(G.hamiltonian_hard(8), Counter(), degree_prune=True))
        star = [{1, 2, 3}, {0}, {0}, {0}]
        self.assertIsNone(Q.hamiltonian_cycle(star, Counter()))
        self.assertIsNone(Q.hamiltonian_cycle([set(), set()], Counter()))      # too small
        rng = random.Random(8)
        for n in (6, 9, 12):
            adj = G.hamiltonian_planted(n, 2, rng)
            c = Q.hamiltonian_cycle(adj, Counter())
            self.assertIsNotNone(c)
            self.assertTrue(all(c[(i + 1) % n] in adj[c[i]] for i in range(n)))

    def test_tsp_bruteforce_equals_bb(self):
        rng = random.Random(9)
        for n in (2, 3, 5, 7, 8):
            for kind in ("euclid", "uniform"):
                d = G.tsp_matrix(n, rng, kind)
                a, ta = Q.tsp_bruteforce(d, Counter())
                b, tb = Q.tsp_branch_and_bound(d, Counter())
                self.assertEqual(a, b, (n, kind))
                self.assertEqual(sum(d[tb[i]][tb[(i + 1) % n]] for i in range(n)), b)

    def test_bb_prunes(self):
        d = G.tsp_matrix(10, random.Random(10))
        cb, cbb = Counter(), Counter()
        Q.tsp_bruteforce(d, cb)
        Q.tsp_branch_and_bound(d, cbb)
        self.assertLess(cbb["states"], cb["states"])
        self.assertGreater(cbb["pruned"], 0)

    def test_budget_stops_search(self):
        with self.assertRaises(BudgetExceeded):
            Q.tsp_bruteforce(G.tsp_matrix(10, random.Random(1)), Counter(state_limit=1000))


if __name__ == "__main__":
    unittest.main(verbosity=2)
