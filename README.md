# DAA Algorithm Vulnerability and Stress-Testing Framework (Assignment 3)

B.Tech (AI and ML), Section Leopards, Woxsen University

Team: Joshitha Chintakrinda (25WU0102109), Souri Keerthana (25WU0104026), Teja Sri Sowmya (25WU0102173),
Vaibhav Chandra (25WU0102209), Nikhelish Chandra (25WU0102206)

A laboratory that generates hard inputs for syllabus algorithms, counts operations, time and memory, and
classifies each test as Low / Moderate / High risk. It covers all six mandatory families: advanced data
structures, MST, knapsack, dynamic programming, backtracking / Branch & Bound, and NP classification.

## Contents
- Python framework (this folder) and sample output in `results/`
- `demo/index.html`: interactive in-browser demo (open the file in any browser, no install needed). It runs typical-vs-crafted
  input scenarios with a service time limit. Live link (if GitHub Pages is enabled): see the repository's Pages URL.
- `docs/`: project report (PDF) and submission form


Pure Python 3.9+ (stdlib only). `matplotlib` is optional, for the plots: `pip install matplotlib`.

## Run
```
python main.py                # everything, ~2 min  -> results/report.md, results.csv, family1..5.png
python main.py --quick        # smaller sizes, ~30 s
python main.py --family 2 5   # only some families (6 = NP table)
python -m unittest tests -v   # 21 correctness tests
```

## Files
| File | Role |
|---|---|
| `metrics.py` | `Counter` (operation counts + state/time budgets), `BudgetExceeded` |
| `structures.py` | Binomial heap, Fibonacci heap, Red-Black tree, B-Tree, naive BST baseline |
| `mst.py` | Prim (heap), Prim (matrix), Kruskal |
| `knapsack.py` | Fractional (greedy), greedy-on-0/1, 0/1 DP |
| `dp.py` | Floyd-Warshall, Matrix Chain |
| `search.py` | N-Queens, Hamiltonian cycle, TSP brute force, TSP Branch & Bound |
| `generators.py` | Input families (sparse/dense graphs, K_{n-1}+pendant, sorted keys, ...) |
| `framework.py` | `Experiment` interface: generate -> prepare -> run -> measure |
| `risk.py` | Low / Moderate / High classifier (thresholds at the top of the file) |
| `complexity.py` | NP-Hard / NP-Complete table (family 6) |
| `experiments.py` | All experiments, grouped by the 6 mandatory families |
| `main.py`, `tests.py` | Runner + report/plots, correctness tests |

## Add a new algorithm
Create one `Experiment(...)` in `experiments.py` with an input generator, a runner that increments a `Counter`,
and a theoretical bound. Measurement, risk classification, plots and report pick it up automatically.

## Risk rules (risk.py)
- High: budget exceeded (states/cells), or > 5 s, or > 500 MB peak.
- Moderate: > 0.5 s, > 50 MB, fitted exponent >= 1.8, ops growing > 2x faster than theory,
  or an exponential-class algorithm whose ops grew > 1000x over the tested range.
- Low: otherwise.
