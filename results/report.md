# DAA Algorithm Vulnerability and Stress-Testing Report

Generated 2026-10-14 14:38. Risk thresholds: time > 0.5s moderate, > 5.0s high; peak memory > 48 MB moderate; fitted exponent >= 1.8 moderate; budget exceeded = high.

## Risk summary

| Fam | Experiment | Theory | Max n | Ops @max | Time(s) max | Peak MB | Fit exp | RISK | Reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Binomial heap: n inserts + n extract-mins | O(n log n) for n inserts + n extract-mins | 16000 | 474,036 | 0.167 | 1.1 | 1.15 | Low | practical up to n=16000 and follows O(n log n) for n inserts + n extract-mins |
| 1 | Fibonacci heap: n inserts + n extract-mins | O(n log n) for n inserts + n extract-mins | 16000 | 475,042 | 0.145 | 1.5 | 1.15 | Low | practical up to n=16000 and follows O(n log n) for n inserts + n extract-mins |
| 1 | Binomial heap: n/2 decrease-keys | O(log n) per decrease-key | 16000 | 48,560 | 0.008 | 0.2 | 1.15 | Low | practical up to n=16000 and follows O(log n) per decrease-key |
| 1 | Fibonacci heap: n/2 decrease-keys | O(1) amortised per decrease-key | 16000 | 8,957 | 0.007 | 0.2 | 1.00 | Low | practical up to n=16000 and follows O(1) amortised per decrease-key |
| 1 | Binomial heap: merge two heaps | O(log n) | 64000 | 12 | 0.000 | 0.0 | 0.00 | Low | practical up to n=64000 and follows O(log n) |
| 1 | Fibonacci heap: merge two heaps | O(1) | 64000 | 1 | 0.000 | 0.0 | 0.00 | Low | practical up to n=64000 and follows O(1) |
| 1 | Red-Black tree: random inserts | O(n log n) | 32000 | 479,939 | 0.118 | 2.2 | 1.12 | Low | practical up to n=32000 and follows O(n log n) |
| 1 | Red-Black tree: SORTED inserts | O(n log n) | 32000 | 846,082 | 0.118 | 2.2 | 1.14 | Low | practical up to n=32000 and follows O(n log n) |
| 1 | Naive BST: random inserts | O(n log n) expected | 16000 | 272,344 | 0.020 | 1.2 | 1.13 | Low | practical up to n=16000 and follows O(n log n) expected |
| 1 | Naive BST: SORTED inserts (degenerate) | O(n^2) | 8000 | 31,996,000 | 1.329 | 0.3 | 2.00 | Moderate | 1.33s at the largest size; super-linear growth, fitted exponent n^2.00 (doubling n multiplies ops by 4.0) |
| 1 | B-Tree (t=2): random inserts | O(n log_2 n) node accesses | 32000 | 339,071 | 0.136 | 3.9 | 1.14 | Low | practical up to n=32000 and follows O(n log_2 n) node accesses |
| 1 | B-Tree (t=32): random inserts | O(n log_32 n) node accesses | 32000 | 92,955 | 0.097 | 0.4 | 1.13 | Low | practical up to n=32000 and follows O(n log_32 n) node accesses |
| 2 | Kruskal on sparse E=2V graphs | O(E log E) | 1600 | 38,542 | 0.006 | 0.2 | 1.16 | Low | practical up to n=1600 and follows O(E log E) |
| 2 | Prim (heap) on sparse E=2V graphs | O(E) heap ops, each O(log V) | 1600 | 12,802 | 0.003 | 0.4 | 1.00 | Low | practical up to n=1600 and follows O(E) heap ops, each O(log V) |
| 2 | Prim (matrix) on sparse E=2V graphs | O(V^2) | 1600 | 7,680,000 | 0.146 | 19.7 | 2.00 | Moderate | super-linear growth, fitted exponent n^2.00 (doubling n multiplies ops by 4.0) |
| 2 | Kruskal on dense E~V^2/4 graphs | O(E log E) | 800 | 2,557,558 | 0.364 | 11.0 | 2.24 | Moderate | super-linear growth, fitted exponent n^2.24 (doubling n multiplies ops by 4.7) |
| 2 | Prim (heap) on dense E~V^2/4 graphs | O(E) heap ops, each O(log V) | 800 | 639,202 | 0.283 | 20.8 | 2.01 | Moderate | super-linear growth, fitted exponent n^2.01 (doubling n multiplies ops by 4.0) |
| 2 | Prim (matrix) on dense E~V^2/4 graphs | O(V^2) | 800 | 1,920,000 | 0.069 | 4.9 | 2.00 | Moderate | super-linear growth, fitted exponent n^2.00 (doubling n multiplies ops by 4.0) |
| 3 | Fractional knapsack (greedy) as n grows | O(n log n) | 64000 | 936,600 | 0.159 | 4.4 | 1.13 | Low | practical up to n=64000 and follows O(n log n) |
| 3 | 0/1 knapsack (DP), n grows, W=2000 | O(nW) time and space | 800 | 1,600,800 | 0.156 | 24.1 | 1.00 | Low | practical up to n=800 and follows O(nW) time and space |
| 3 | 0/1 knapsack (DP), n=100, CAPACITY W grows | O(nW): pseudo-polynomial in W | 128000 | 0 | 0.323 | 119.3 | 1.00 | High | budget exceeded at n=128000 (DP table needs 12,928,101 cells (> budget 5,000,000)); peak memory 119 MB |
| 4 | Floyd-Warshall as vertex count grows | Theta(V^3) time, Theta(V^2) space | 150 | 3,375,000 | 0.124 | 0.2 | 3.00 | Moderate | super-linear growth, fitted exponent n^3.00 (doubling n multiplies ops by 8.0) |
| 4 | Matrix-chain multiplication as chain length grows | Theta(n^3) time, Theta(n^2) space | 200 | 1,333,300 | 0.149 | 1.2 | 3.00 | Moderate | super-linear growth, fitted exponent n^3.00 (doubling n multiplies ops by 8.0) |
| 5 | N-Queens: enumerate ALL solutions | O(n!) worst case, pruned by diagonals | 12 | 856,189 | 1.144 | 0.0 | 12.35 | Moderate | 1.14s at the largest size; exponential-class: ops grew x5,596 over n=6..12 |
| 5 | N-Queens: find the FIRST solution | O(n!) worst case | 24 | 411,609 | 0.976 | 0.0 | 8.27 | Moderate | 0.98s at the largest size; exponential-class: ops grew x3,611 over n=8..24 |
| 5 | Hamiltonian: no-cycle graph (K_{n-1}+pendant), plain backtracking | O(n!) worst case | 12 | 2,000,001 | 1.860 | 0.0 | 15.79 | High | budget exceeded at n=12 (states exceeded budget of 2,000,000); 1.86s at the largest size; exponential-class: ops grew x14,946 over n=6..11 |
| 5 | Hamiltonian: SAME graphs + degree>=2 pruning | O(n) pre-check | 40 | 1 | 0.000 | 0.0 | 0.00 | Low | practical up to n=40 and follows O(n) pre-check |
| 5 | Hamiltonian: sparse random graph WITH a cycle (n extra chords) | O(n!) worst case | 26 | 19,744 | 0.009 | 0.0 | 6.88 | Low | practical up to n=26 and follows O(n!) worst case |
| 5 | TSP: brute-force backtracking (no bound) | O((n-1)!) | 11 | 3,000,001 | 1.103 | 0.0 | 13.80 | High | budget exceeded at n=11 (states exceeded budget of 3,000,000); 1.10s at the largest size; exponential-class: ops grew x15,176 over n=5..10 |
| 5 | TSP: Branch & Bound, Euclidean instances | exponential worst case | 16 | 1,500,001 | 1.671 | 34.8 | 11.80 | High | budget exceeded at n=16 (states exceeded budget of 1,500,000); 1.67s at the largest size |
| 5 | TSP: Branch & Bound, random-weight instances (weaker bound) | exponential worst case | 16 | 622,176 | 0.355 | 20.1 | 10.39 | Moderate | exponential-class: ops grew x1,773 over n=8..16 |

## Measurements per experiment

### 1. Advanced data structures: Binomial heap: n inserts + n extract-mins
Theory: O(n log n) for n inserts + n extract-mins. Risk: **Low** (practical up to n=16000 and follows O(n log n) for n inserts + n extract-mins)

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 1000 | 19,540 | 0.0050 | 71 | OK | comparisons=12,239, extract_min_calls=1,000, insert_calls=1,000, links=7,301 |
| 2000 | 44,500 | 0.0106 | 141 | OK | comparisons=27,685, extract_min_calls=2,000, insert_calls=2,000, links=16,815 |
| 4000 | 98,434 | 0.0237 | 282 | OK | comparisons=61,084, extract_min_calls=4,000, insert_calls=4,000, links=37,350 |
| 8000 | 217,250 | 0.1666 | 563 | OK | comparisons=134,356, extract_min_calls=8,000, insert_calls=8,000, links=82,894 |
| 16000 | 474,036 | 0.1066 | 1125 | OK | comparisons=292,477, extract_min_calls=16,000, insert_calls=16,000, links=181,559 |

### 1. Advanced data structures: Fibonacci heap: n inserts + n extract-mins
Theory: O(n log n) for n inserts + n extract-mins. Risk: **Low** (practical up to n=16000 and follows O(n log n) for n inserts + n extract-mins)

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 1000 | 19,674 | 0.0060 | 96 | OK | comparisons=12,303, extract_min_calls=1,000, insert_calls=1,000, links=7,371 |
| 2000 | 44,494 | 0.0137 | 189 | OK | comparisons=27,679, extract_min_calls=2,000, insert_calls=2,000, links=16,815 |
| 4000 | 98,696 | 0.0321 | 378 | OK | comparisons=61,212, extract_min_calls=4,000, insert_calls=4,000, links=37,484 |
| 8000 | 217,352 | 0.0668 | 755 | OK | comparisons=134,404, extract_min_calls=8,000, insert_calls=8,000, links=82,948 |
| 16000 | 475,042 | 0.1453 | 1511 | OK | comparisons=292,977, extract_min_calls=16,000, insert_calls=16,000, links=182,065 |

### 1. Advanced data structures: Binomial heap: n/2 decrease-keys
Theory: O(log n) per decrease-key. Risk: **Low** (practical up to n=16000 and follows O(log n) per decrease-key)

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 1000 | 2,027 | 0.0003 | 13 | OK | decrease_key_calls=500, swaps=2,027 |
| 2000 | 4,485 | 0.0008 | 26 | OK | decrease_key_calls=1,000, swaps=4,485 |
| 4000 | 10,066 | 0.0018 | 53 | OK | decrease_key_calls=1,999, swaps=10,066 |
| 8000 | 22,245 | 0.0039 | 105 | OK | decrease_key_calls=4,000, swaps=22,245 |
| 16000 | 48,560 | 0.0078 | 210 | OK | decrease_key_calls=7,999, swaps=48,560 |

### 1. Advanced data structures: Fibonacci heap: n/2 decrease-keys
Theory: O(1) amortised per decrease-key. Risk: **Low** (practical up to n=16000 and follows O(1) amortised per decrease-key)

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 1000 | 560 | 0.0004 | 16 | OK | comparisons=1,060, cuts=560, decrease_key_calls=500 |
| 2000 | 1,108 | 0.0007 | 31 | OK | comparisons=2,108, cuts=1,108, decrease_key_calls=1,000 |
| 4000 | 2,215 | 0.0015 | 63 | OK | comparisons=4,214, cuts=2,215, decrease_key_calls=1,999 |
| 8000 | 4,470 | 0.0034 | 125 | OK | comparisons=8,470, cuts=4,470, decrease_key_calls=4,000 |
| 16000 | 8,957 | 0.0068 | 250 | OK | comparisons=16,956, cuts=8,957, decrease_key_calls=7,999 |

### 1. Advanced data structures: Binomial heap: merge two heaps
Theory: O(log n). Risk: **Low** (practical up to n=64000 and follows O(log n))

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 2000 | 12 | 0.0000 | 0 | OK | comparisons=6, links=6, merge_calls=1 |
| 8000 | 12 | 0.0000 | 0 | OK | comparisons=6, links=6, merge_calls=1 |
| 32000 | 12 | 0.0000 | 0 | OK | comparisons=6, links=6, merge_calls=1 |
| 64000 | 12 | 0.0000 | 0 | OK | comparisons=6, links=6, merge_calls=1 |

### 1. Advanced data structures: Fibonacci heap: merge two heaps
Theory: O(1). Risk: **Low** (practical up to n=64000 and follows O(1))

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 2000 | 1 | 0.0000 | 0 | OK | comparisons=1, merge_calls=1, splices=1 |
| 8000 | 1 | 0.0000 | 0 | OK | comparisons=1, merge_calls=1, splices=1 |
| 32000 | 1 | 0.0000 | 0 | OK | comparisons=1, merge_calls=1, splices=1 |
| 64000 | 1 | 0.0000 | 0 | OK | comparisons=1, merge_calls=1, splices=1 |

### 1. Advanced data structures: Red-Black tree: random inserts
Theory: O(n log n). Risk: **Low** (practical up to n=32000 and follows O(n log n))

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 1000 | 9,951 | 0.0018 | 72 | OK | comparisons=8,834, final_height=12, insert_calls=1,000, recolors=512, rotations=605, search_calls=100, search_comparisons=911 |
| 2000 | 21,954 | 0.0045 | 143 | OK | comparisons=19,729, final_height=14, insert_calls=2,000, recolors=1,019, rotations=1,206, search_calls=200, search_comparisons=2,080 |
| 4000 | 47,639 | 0.0082 | 285 | OK | comparisons=43,294, final_height=15, insert_calls=4,000, recolors=2,055, rotations=2,290, search_calls=400, search_comparisons=4,502 |
| 8000 | 103,448 | 0.0200 | 570 | OK | comparisons=94,708, final_height=16, insert_calls=8,000, recolors=4,083, rotations=4,657, search_calls=800, search_comparisons=9,907 |
| 16000 | 223,270 | 0.0390 | 1138 | OK | comparisons=205,685, final_height=17, insert_calls=16,000, recolors=8,178, rotations=9,407, search_calls=1,600, search_comparisons=21,295 |
| 32000 | 479,939 | 0.1180 | 2276 | OK | comparisons=444,922, final_height=19, insert_calls=32,000, recolors=16,447, rotations=18,570, search_calls=3,200, search_comparisons=46,027 |

### 1. Advanced data structures: Red-Black tree: SORTED inserts
Theory: O(n log n). Risk: **Low** (practical up to n=32000 and follows O(n log n))

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 1000 | 16,442 | 0.0026 | 72 | OK | comparisons=14,481, final_height=17, insert_calls=1,000, recolors=978, rotations=983, search_calls=100, search_comparisons=1,036 |
| 2000 | 36,882 | 0.0057 | 143 | OK | comparisons=32,925, final_height=19, insert_calls=2,000, recolors=1,976, rotations=1,981, search_calls=200, search_comparisons=2,275 |
| 4000 | 81,762 | 0.0126 | 285 | OK | comparisons=73,809, final_height=21, insert_calls=4,000, recolors=3,974, rotations=3,979, search_calls=400, search_comparisons=4,953 |
| 8000 | 179,522 | 0.0262 | 570 | OK | comparisons=163,573, final_height=23, insert_calls=8,000, recolors=7,972, rotations=7,977, search_calls=800, search_comparisons=10,709 |
| 16000 | 391,042 | 0.0682 | 1138 | OK | comparisons=359,097, final_height=25, insert_calls=16,000, recolors=15,970, rotations=15,975, search_calls=1,600, search_comparisons=23,022 |
| 32000 | 846,082 | 0.1180 | 2277 | OK | comparisons=782,141, final_height=27, insert_calls=32,000, recolors=31,968, rotations=31,973, search_calls=3,200, search_comparisons=49,249 |

### 1. Advanced data structures: Naive BST: random inserts
Theory: O(n log n) expected. Risk: **Low** (practical up to n=16000 and follows O(n log n) expected)

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 1000 | 11,402 | 0.0010 | 75 | OK | comparisons=11,402, final_height=23, insert_calls=1,000 |
| 2000 | 28,300 | 0.0022 | 154 | OK | comparisons=28,300, final_height=29, insert_calls=2,000 |
| 4000 | 57,360 | 0.0044 | 312 | OK | comparisons=57,360, final_height=31, insert_calls=4,000 |
| 8000 | 121,541 | 0.0090 | 627 | OK | comparisons=121,541, final_height=31, insert_calls=8,000 |
| 16000 | 272,344 | 0.0195 | 1259 | OK | comparisons=272,344, final_height=33, insert_calls=16,000 |

### 1. Advanced data structures: Naive BST: SORTED inserts (degenerate)
Theory: O(n^2). Risk: **Moderate** (1.33s at the largest size; super-linear growth, fitted exponent n^2.00 (doubling n multiplies ops by 4.0))

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 500 | 124,750 | 0.0045 | 36 | OK | comparisons=124,750, final_height=500, insert_calls=500 |
| 1000 | 499,500 | 0.0267 | 75 | OK | comparisons=499,500, final_height=1,000, insert_calls=1,000 |
| 2000 | 1,999,000 | 0.1144 | 154 | OK | comparisons=1,999,000, final_height=2,000, insert_calls=2,000 |
| 4000 | 7,998,000 | 0.3070 | 312 | OK | comparisons=7,998,000, final_height=4,000, insert_calls=4,000 |
| 8000 | 31,996,000 | 1.3295 |  | OK | comparisons=31,996,000, final_height=8,000, insert_calls=8,000 |

### 1. Advanced data structures: B-Tree (t=2): random inserts
Theory: O(n log_2 n) node accesses. Risk: **Low** (practical up to n=32000 and follows O(n log_2 n) node accesses)

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 1000 | 6,562 | 0.0027 | 122 | OK | comparisons=8,336, final_height=8, insert_calls=1,000, node_accesses=6,562, search_calls=100, search_comparisons=511, search_node_accesses=737, splits=563 |
| 2000 | 14,812 | 0.0060 | 247 | OK | comparisons=18,752, final_height=9, insert_calls=2,000, node_accesses=14,812, search_calls=200, search_comparisons=1,118, search_node_accesses=1,699, splits=1,134 |
| 4000 | 32,140 | 0.0197 | 502 | OK | comparisons=41,369, final_height=9, insert_calls=4,000, node_accesses=32,140, search_calls=400, search_comparisons=2,500, search_node_accesses=3,350, splits=2,302 |
| 8000 | 72,444 | 0.0288 | 994 | OK | comparisons=91,119, final_height=10, insert_calls=8,000, node_accesses=72,444, search_calls=800, search_comparisons=5,186, search_node_accesses=7,565, splits=4,534 |
| 16000 | 161,105 | 0.0636 | 1991 | OK | comparisons=198,444, final_height=11, insert_calls=16,000, node_accesses=161,105, search_calls=1,600, search_comparisons=11,792, search_node_accesses=16,694, splits=9,072 |
| 32000 | 339,071 | 0.1365 | 3998 | OK | comparisons=432,050, final_height=12, insert_calls=32,000, node_accesses=339,071, search_calls=3,200, search_comparisons=24,823, search_node_accesses=36,534, splits=18,231 |

### 1. Advanced data structures: B-Tree (t=32): random inserts
Theory: O(n log_32 n) node accesses. Risk: **Low** (practical up to n=32000 and follows O(n log_32 n) node accesses)

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 1000 | 1,937 | 0.0019 | 11 | OK | comparisons=27,808, final_height=2, insert_calls=1,000, node_accesses=1,937, search_calls=100, search_comparisons=3,297, search_node_accesses=198, splits=20 |
| 2000 | 3,937 | 0.0044 | 23 | OK | comparisons=70,411, final_height=2, insert_calls=2,000, node_accesses=3,937, search_calls=200, search_comparisons=8,816, search_node_accesses=394, splits=41 |
| 4000 | 9,096 | 0.0097 | 51 | OK | comparisons=162,816, final_height=3, insert_calls=4,000, node_accesses=9,096, search_calls=400, search_comparisons=17,532, search_node_accesses=1,188, splits=90 |
| 8000 | 21,105 | 0.0217 | 105 | OK | comparisons=358,687, final_height=3, insert_calls=8,000, node_accesses=21,105, search_calls=800, search_comparisons=36,590, search_node_accesses=2,385, splits=180 |
| 16000 | 45,175 | 0.0455 | 212 | OK | comparisons=743,787, final_height=3, insert_calls=16,000, node_accesses=45,175, search_calls=1,600, search_comparisons=75,724, search_node_accesses=4,772, splits=361 |
| 32000 | 92,955 | 0.0971 | 430 | OK | comparisons=1,612,645, final_height=3, insert_calls=32,000, node_accesses=92,955, search_calls=3,200, search_comparisons=164,076, search_node_accesses=9,537, splits=736 |

### 2. MST algorithms: Kruskal on sparse E=2V graphs
Theory: O(E log E). Risk: **Low** (practical up to n=1600 and follows O(E log E))

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 100 | 1,556 | 0.0002 | 13 | OK | sort_comparisons=1,275, uf_finds=342, uf_steps=281, uf_unions=99 |
| 200 | 3,518 | 0.0005 | 29 | OK | sort_comparisons=2,942, uf_finds=696, uf_steps=576, uf_unions=199 |
| 400 | 7,979 | 0.0012 | 57 | OK | sort_comparisons=6,666, uf_finds=1,590, uf_steps=1,313, uf_unions=399 |
| 800 | 17,663 | 0.0026 | 113 | OK | sort_comparisons=14,909, uf_finds=3,196, uf_steps=2,754, uf_unions=799 |
| 1600 | 38,542 | 0.0056 | 225 | OK | sort_comparisons=33,030, uf_finds=6,366, uf_steps=5,512, uf_unions=1,599 |

### 2. MST algorithms: Prim (heap) on sparse E=2V graphs
Theory: O(E) heap ops, each O(log V). Risk: **Low** (practical up to n=1600 and follows O(E) heap ops, each O(log V))

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 100 | 802 | 0.0001 | 8 | OK | adj_build=400, edge_scans=400, heap_pop=201, heap_push=201, stale_pops=101 |
| 200 | 1,602 | 0.0003 | 21 | OK | adj_build=800, edge_scans=800, heap_pop=401, heap_push=401, stale_pops=201 |
| 400 | 3,202 | 0.0006 | 45 | OK | adj_build=1,600, edge_scans=1,600, heap_pop=801, heap_push=801, stale_pops=401 |
| 800 | 6,402 | 0.0013 | 160 | OK | adj_build=3,200, edge_scans=3,200, heap_pop=1,601, heap_push=1,601, stale_pops=801 |
| 1600 | 12,802 | 0.0028 | 434 | OK | adj_build=6,400, edge_scans=6,400, heap_pop=3,201, heap_push=3,201, stale_pops=1,601 |

### 2. MST algorithms: Prim (matrix) on sparse E=2V graphs
Theory: O(V^2). Risk: **Moderate** (super-linear growth, fitted exponent n^2.00 (doubling n multiplies ops by 4.0))

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 100 | 30,000 | 0.0005 | 82 | OK | key_scans=10,000, matrix_cells=10,000, matrix_reads=10,000 |
| 200 | 120,000 | 0.0019 | 324 | OK | key_scans=40,000, matrix_cells=40,000, matrix_reads=40,000 |
| 400 | 480,000 | 0.0080 | 1278 | OK | key_scans=160,000, matrix_cells=160,000, matrix_reads=160,000 |
| 800 | 1,920,000 | 0.0350 | 5059 | OK | key_scans=640,000, matrix_cells=640,000, matrix_reads=640,000 |
| 1600 | 7,680,000 | 0.1458 | 20123 | OK | key_scans=2,560,000, matrix_cells=2,560,000, matrix_reads=2,560,000 |

### 2. MST algorithms: Kruskal on dense E~V^2/4 graphs
Theory: O(E log E). Risk: **Moderate** (super-linear growth, fitted exponent n^2.24 (doubling n multiplies ops by 4.7))

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 50 | 5,090 | 0.0007 | 43 | OK | sort_comparisons=4,862, uf_finds=258, uf_steps=228, uf_unions=49 |
| 100 | 25,030 | 0.0034 | 174 | OK | sort_comparisons=24,682, uf_finds=406, uf_steps=348, uf_unions=99 |
| 200 | 120,361 | 0.0163 | 700 | OK | sort_comparisons=119,208, uf_finds=1,268, uf_steps=1,153, uf_unions=199 |
| 400 | 559,613 | 0.0772 | 2806 | OK | sort_comparisons=557,573, uf_finds=2,214, uf_steps=2,040, uf_unions=399 |
| 800 | 2,557,558 | 0.3637 | 11236 | OK | sort_comparisons=2,553,686, uf_finds=4,240, uf_steps=3,872, uf_unions=799 |

### 2. MST algorithms: Prim (heap) on dense E~V^2/4 graphs
Theory: O(E) heap ops, each O(log V). Risk: **Moderate** (super-linear growth, fitted exponent n^2.01 (doubling n multiplies ops by 4.0))

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 50 | 2,450 | 0.0005 | 17 | OK | adj_build=1,224, edge_scans=1,224, heap_pop=613, heap_push=613, stale_pops=563 |
| 100 | 9,902 | 0.0020 | 227 | OK | adj_build=4,950, edge_scans=4,950, heap_pop=2,476, heap_push=2,476, stale_pops=2,376 |
| 200 | 39,802 | 0.0083 | 1240 | OK | adj_build=19,900, edge_scans=19,900, heap_pop=9,951, heap_push=9,951, stale_pops=9,751 |
| 400 | 159,602 | 0.0381 | 5293 | OK | adj_build=79,800, edge_scans=79,800, heap_pop=39,901, heap_push=39,901, stale_pops=39,501 |
| 800 | 639,202 | 0.2832 | 21343 | OK | adj_build=319,600, edge_scans=319,600, heap_pop=159,801, heap_push=159,801, stale_pops=159,001 |

### 2. MST algorithms: Prim (matrix) on dense E~V^2/4 graphs
Theory: O(V^2). Risk: **Moderate** (super-linear growth, fitted exponent n^2.00 (doubling n multiplies ops by 4.0))

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 50 | 7,500 | 0.0002 | 21 | OK | key_scans=2,500, matrix_cells=2,500, matrix_reads=2,500 |
| 100 | 30,000 | 0.0008 | 82 | OK | key_scans=10,000, matrix_cells=10,000, matrix_reads=10,000 |
| 200 | 120,000 | 0.0024 | 324 | OK | key_scans=40,000, matrix_cells=40,000, matrix_reads=40,000 |
| 400 | 480,000 | 0.0108 | 1278 | OK | key_scans=160,000, matrix_cells=160,000, matrix_reads=160,000 |
| 800 | 1,920,000 | 0.0688 | 5059 | OK | key_scans=640,000, matrix_cells=640,000, matrix_reads=640,000 |

### 3. Knapsack: Fractional knapsack (greedy) as n grows
Theory: O(n log n). Risk: **Low** (practical up to n=64000 and follows O(n log n))

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 1000 | 8,650 | 0.0018 | 71 | OK | greedy_steps=617, sort_comparisons=8,650 |
| 4000 | 42,506 | 0.0072 | 281 | OK | greedy_steps=2,494, sort_comparisons=42,506 |
| 16000 | 202,195 | 0.0370 | 1126 | OK | greedy_steps=9,974, sort_comparisons=202,195 |
| 64000 | 936,600 | 0.1593 | 4500 | OK | greedy_steps=39,864, sort_comparisons=936,600 |

### 3. Knapsack: 0/1 knapsack (DP), n grows, W=2000
Theory: O(nW) time and space. Risk: **Low** (practical up to n=800 and follows O(nW) time and space)

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 50 | 100,050 | 0.0096 | 3131 | OK | cells=100,050 |
| 100 | 200,100 | 0.0194 | 5567 | OK | cells=200,100 |
| 200 | 400,200 | 0.0380 | 8988 | OK | cells=400,200 |
| 400 | 800,400 | 0.0780 | 13796 | OK | cells=800,400 |
| 800 | 1,600,800 | 0.1562 | 24662 | OK | cells=1,600,800 |

### 3. Knapsack: 0/1 knapsack (DP), n=100, CAPACITY W grows
Theory: O(nW): pseudo-polynomial in W. Risk: **High** (budget exceeded at n=128000 (DP table needs 12,928,101 cells (> budget 5,000,000)); peak memory 119 MB)

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 500 | 50,100 | 0.0047 | 870 | OK | cells=50,100 |
| 2000 | 200,100 | 0.0189 | 5215 | OK | cells=200,100 |
| 8000 | 800,100 | 0.0792 | 28501 | OK | cells=800,100 |
| 32000 | 3,200,100 | 0.3231 | 122118 | OK | cells=3,200,100 |
| 128000 | 0 | 0.0000 |  | BUDGET | cells=0 |

### 4. Dynamic programming: Floyd-Warshall as vertex count grows
Theory: Theta(V^3) time, Theta(V^2) space. Risk: **Moderate** (super-linear growth, fitted exponent n^3.00 (doubling n multiplies ops by 8.0))

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 25 | 15,625 | 0.0007 | 5 | OK | improvements=1,613, inner_iterations=15,625 |
| 50 | 125,000 | 0.0048 | 23 | OK | improvements=9,386, inner_iterations=125,000 |
| 100 | 1,000,000 | 0.0371 | 85 | OK | improvements=48,380, inner_iterations=1,000,000 |
| 150 | 3,375,000 | 0.1236 | 186 | OK | improvements=130,931, inner_iterations=3,375,000 |

### 4. Dynamic programming: Matrix-chain multiplication as chain length grows
Theory: Theta(n^3) time, Theta(n^2) space. Risk: **Moderate** (super-linear growth, fitted exponent n^3.00 (doubling n multiplies ops by 8.0))

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 25 | 2,600 | 0.0004 | 21 | OK | inner_iterations=2,600 |
| 50 | 20,825 | 0.0024 | 83 | OK | inner_iterations=20,825 |
| 100 | 166,650 | 0.0183 | 323 | OK | inner_iterations=166,650 |
| 200 | 1,333,300 | 0.1488 | 1271 | OK | inner_iterations=1,333,300 |

### 5. Backtracking / Branch & Bound: N-Queens: enumerate ALL solutions
Theory: O(n!) worst case, pruned by diagonals. Risk: **Moderate** (1.14s at the largest size; exponential-class: ops grew x5,596 over n=6..12)

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 6 | 153 | 0.0002 | 2 | OK | pruned=742, states=153 |
| 7 | 552 | 0.0005 | 2 | OK | pruned=3,033, states=552 |
| 8 | 2,057 | 0.0020 | 2 | OK | pruned=13,664, states=2,057 |
| 9 | 8,394 | 0.0091 | 2 | OK | pruned=63,985, states=8,394 |
| 10 | 35,539 | 0.0418 | 2 | OK | pruned=312,612, states=35,539 |
| 11 | 166,926 | 0.2055 | 2 | OK | pruned=1,639,781, states=166,926 |
| 12 | 856,189 | 1.1440 |  | OK | pruned=9,247,680, states=856,189 |

### 5. Backtracking / Branch & Bound: N-Queens: find the FIRST solution
Theory: O(n!) worst case. Risk: **Moderate** (0.98s at the largest size; exponential-class: ops grew x3,611 over n=8..24)

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 8 | 114 | 0.0001 | 2 | OK | pruned=763, states=114 |
| 12 | 262 | 0.0003 | 2 | OK | pruned=2,805, states=262 |
| 16 | 10,053 | 0.0167 | 3 | OK | pruned=150,660, states=10,053 |
| 20 | 199,636 | 0.3982 | 3 | OK | pruned=3,792,875, states=199,636 |
| 24 | 411,609 | 0.9756 | 4 | OK | pruned=9,466,708, states=411,609 |

### 5. Backtracking / Branch & Bound: Hamiltonian: no-cycle graph (K_{n-1}+pendant), plain backtracking
Theory: O(n!) worst case. Risk: **High** (budget exceeded at n=12 (states exceeded budget of 2,000,000); 1.86s at the largest size; exponential-class: ops grew x14,946 over n=6..11)

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 6 | 66 | 0.0004 | 3 | OK | pruned=197, states=66 |
| 7 | 327 | 0.0002 | 6 | OK | pruned=1,306, states=327 |
| 8 | 1,958 | 0.0013 | 7 | OK | pruned=9,787, states=1,958 |
| 9 | 13,701 | 0.0130 | 8 | OK | pruned=82,202, states=13,701 |
| 10 | 109,602 | 0.0979 | 9 | OK | pruned=767,209, states=109,602 |
| 11 | 986,411 | 0.8445 | 10 | OK | pruned=7,891,282, states=986,411 |
| 12 | 2,000,001 | 1.8598 |  | BUDGET | pruned=17,999,963, states=2,000,001 |

### 5. Backtracking / Branch & Bound: Hamiltonian: SAME graphs + degree>=2 pruning
Theory: O(n) pre-check. Risk: **Low** (practical up to n=40 and follows O(n) pre-check)

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 6 | 1 | 0.0000 | 1 | OK | pruned=1, states=0 |
| 8 | 1 | 0.0000 | 1 | OK | pruned=1, states=0 |
| 10 | 1 | 0.0000 | 2 | OK | pruned=1, states=0 |
| 12 | 1 | 0.0000 | 2 | OK | pruned=1, states=0 |
| 20 | 1 | 0.0000 | 4 | OK | pruned=1, states=0 |
| 40 | 1 | 0.0000 | 13 | OK | pruned=1, states=0 |

### 5. Backtracking / Branch & Bound: Hamiltonian: sparse random graph WITH a cycle (n extra chords)
Theory: O(n!) worst case. Risk: **Low** (practical up to n=26 and follows O(n!) worst case)

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 10 | 20 | 0.0000 | 5 | OK | pruned=44, states=20 |
| 14 | 373 | 0.0002 | 8 | OK | pruned=1,043, states=373 |
| 18 | 1,141 | 0.0005 | 11 | OK | pruned=3,062, states=1,141 |
| 22 | 4,295 | 0.0021 | 11 | OK | pruned=10,882, states=4,295 |
| 26 | 19,744 | 0.0090 | 14 | OK | pruned=53,369, states=19,744 |

### 5. Backtracking / Branch & Bound: TSP: brute-force backtracking (no bound)
Theory: O((n-1)!). Risk: **High** (budget exceeded at n=11 (states exceeded budget of 3,000,000); 1.10s at the largest size; exponential-class: ops grew x15,176 over n=5..10)

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 5 | 65 | 0.0000 | 1 | OK | states=65 |
| 6 | 326 | 0.0001 | 2 | OK | states=326 |
| 7 | 1,957 | 0.0007 | 2 | OK | states=1,957 |
| 8 | 13,700 | 0.0047 | 2 | OK | states=13,700 |
| 9 | 109,601 | 0.0388 | 2 | OK | states=109,601 |
| 10 | 986,410 | 0.3528 | 2 | OK | states=986,410 |
| 11 | 3,000,001 | 1.1029 |  | BUDGET | states=3,000,001 |

### 5. Backtracking / Branch & Bound: TSP: Branch & Bound, Euclidean instances
Theory: exponential worst case. Risk: **High** (budget exceeded at n=16 (states exceeded budget of 1,500,000); 1.67s at the largest size)

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 8 | 1,454 | 0.0014 | 16 | OK | max_queue=139, pruned=876, states=1,454 |
| 10 | 37,270 | 0.0233 | 919 | OK | max_queue=4,104, pruned=23,996, states=37,270 |
| 12 | 966,319 | 0.8536 | 33604 | OK | max_queue=100,568, pruned=669,051, states=966,319 |
| 14 | 627,097 | 0.4177 | 35597 | OK | max_queue=104,196, pruned=518,490, states=627,097 |
| 16 | 1,500,001 | 1.6709 |  | BUDGET | max_queue=851,319, pruned=441,025, states=1,500,001 |

### 5. Backtracking / Branch & Bound: TSP: Branch & Bound, random-weight instances (weaker bound)
Theory: exponential worst case. Risk: **Moderate** (exponential-class: ops grew x1,773 over n=8..16)

| n | ops | time (s) | peak KB | status | counters |
|---|---|---|---|---|---|
| 8 | 351 | 0.0002 | 2 | OK | max_queue=31, pruned=223, states=351 |
| 10 | 15,472 | 0.0150 | 275 | OK | max_queue=2,510, pruned=10,783, states=15,472 |
| 12 | 4,540 | 0.0022 | 46 | OK | max_queue=750, pruned=3,665, states=4,540 |
| 14 | 319,949 | 0.2000 | 12471 | OK | max_queue=53,758, pruned=253,823, states=319,949 |
| 16 | 622,176 | 0.3554 | 20551 | OK | max_queue=82,030, pruned=524,373, states=622,176 |

## Complexity classification (family 6)

| Problem | Decision version | Class (decision) | Optimization version | Note |
|---|---|---|---|---|
| Hamiltonian Cycle | Does G contain a cycle visiting every vertex once? | NP-Complete | n/a (search version: find the cycle) - NP-Hard as a search problem | Backtracking worst case O(n!); Held-Karp style DP gives O(n^2 2^n). |
| Travelling Salesman (TSP) | Is there a tour of total cost <= k? | NP-Complete | Find the cheapest tour: NP-Hard (not known to be in NP) | Brute force O(n!); Branch & Bound is still exponential in the worst case; Held-Karp O(n^2 2^n). |
| 0/1 Knapsack | Is there a subset with weight <= W and value >= V? | NP-Complete (weakly) | Maximise value: NP-Hard | DP is O(nW): PSEUDO-polynomial (polynomial in the numeric value of W, exponential in its bit length). |
| Fractional Knapsack | Same question with divisible items | in P | in P - greedy by value/weight ratio, O(n log n) | Divisibility gives the greedy-choice property; 0/1 loses it. |
| N-Queens | Place n non-attacking queens (a solution exists for every n >= 4) | in P (constructive O(n) solution exists) | Counting all solutions is the hard part; the 'completion' variant (extend a partial board) is NP-Complete (Gent, Jefferson, Nightingale 2017) | Backtracking is only needed for enumeration or completion - N-Queens is NOT a classic NP-Complete benchmark. |

## Knapsack matched dataset

```
items(value,weight): [(60, 10), (100, 20), (120, 30)]
capacity: 50
fractional_greedy_value: 240.0
greedy_on_0/1_value: 160
0/1_DP_optimal_value: 220
0/1_DP_items: [1, 2]
```

## Gaps in older algorithms that motivated new ones

- **Fibonacci heap**: Dijkstra/Prim with a binary heap pays O(log n) per decrease-key; Fibonacci heaps make it O(1) amortised.
- **Red-Black / AVL tree**: A plain BST degrades to O(n^2) on sorted input; rotations keep height O(log n).
- **B-Tree**: Binary trees are tall and cache/disk-unfriendly; B-Trees pack many keys per node (height log_t n).
- **Johnson's algorithm**: Floyd-Warshall is Theta(V^3) even on sparse graphs; Johnson runs Dijkstra from each vertex.
- **Held-Karp DP, Branch & Bound, approximation**: Brute-force TSP is O(n!); DP gives O(n^2 2^n); bounds and heuristics prune further.
- **FPTAS for knapsack**: 0/1 DP is pseudo-polynomial in W; scaling values gives a (1-eps)-approximation in poly(n, 1/eps).
- **Degree / feasibility pruning**: The measured Hamiltonian result: a cheap necessary-condition check removes the whole search tree.
