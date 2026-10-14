"""Family 6: NP-Hard / NP-Complete classification of the combinatorial problems in the lab."""

TABLE = [
    {"problem": "Hamiltonian Cycle",
     "decision": "Does G contain a cycle visiting every vertex once?",
     "decision_class": "NP-Complete",
     "optimization": "n/a (search version: find the cycle) - NP-Hard as a search problem",
     "note": "Backtracking worst case O(n!); Held-Karp style DP gives O(n^2 2^n)."},
    {"problem": "Travelling Salesman (TSP)",
     "decision": "Is there a tour of total cost <= k?",
     "decision_class": "NP-Complete",
     "optimization": "Find the cheapest tour: NP-Hard (not known to be in NP)",
     "note": "Brute force O(n!); Branch & Bound is still exponential in the worst case; Held-Karp O(n^2 2^n)."},
    {"problem": "0/1 Knapsack",
     "decision": "Is there a subset with weight <= W and value >= V?",
     "decision_class": "NP-Complete (weakly)",
     "optimization": "Maximise value: NP-Hard",
     "note": "DP is O(nW): PSEUDO-polynomial (polynomial in the numeric value of W, exponential in its bit length)."},
    {"problem": "Fractional Knapsack",
     "decision": "Same question with divisible items",
     "decision_class": "in P",
     "optimization": "in P - greedy by value/weight ratio, O(n log n)",
     "note": "Divisibility gives the greedy-choice property; 0/1 loses it."},
    {"problem": "N-Queens",
     "decision": "Place n non-attacking queens (a solution exists for every n >= 4)",
     "decision_class": "in P (constructive O(n) solution exists)",
     "optimization": "Counting all solutions is the hard part; the 'completion' variant (extend a partial board) is NP-Complete (Gent, Jefferson, Nightingale 2017)",
     "note": "Backtracking is only needed for enumeration or completion - N-Queens is NOT a classic NP-Complete benchmark."},
]

POLY_REFERENCE = [
    ("MST (Prim, Kruskal)", "P", "O(E log V) / O(E log E)"),
    ("Floyd-Warshall", "P", "O(V^3)"),
    ("Matrix Chain Multiplication", "P", "O(n^3)"),
]


def format_table():
    lines = ["Problem | Decision version | Class (decision) | Optimization version | Note", "-" * 100]
    for r in TABLE:
        lines.append(f"{r['problem']} | {r['decision']} | {r['decision_class']} | {r['optimization']} | {r['note']}")
    lines.append("")
    lines.append("Polynomial-time references: " + "; ".join(f"{a} ({b}, {c})" for a, b, c in POLY_REFERENCE))
    return "\n".join(lines)


def markdown_table():
    out = ["| Problem | Decision version | Class (decision) | Optimization version | Note |", "|---|---|---|---|---|"]
    for r in TABLE:
        out.append(f"| {r['problem']} | {r['decision']} | {r['decision_class']} | {r['optimization']} | {r['note']} |")
    return "\n".join(out)
