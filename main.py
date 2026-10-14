"""DAA Algorithm Vulnerability and Stress-Testing Framework - runs every test family.

Usage:
    python main.py                 # all families, full sizes (~2 minutes)
    python main.py --quick         # smaller sizes (~30 s)
    python main.py --family 2 5    # only some families (1-5 run experiments, 6 prints the NP table)
    python main.py --no-plots      # skip matplotlib
Outputs go to ./results (report.md, results.csv, one PNG per family)."""
import argparse
import csv
import os
import time

import complexity
import experiments as E
import framework
import risk

GAPS = [
    ("Fibonacci heap", "Dijkstra/Prim with a binary heap pays O(log n) per decrease-key; Fibonacci heaps make it O(1) amortised."),
    ("Red-Black / AVL tree", "A plain BST degrades to O(n^2) on sorted input; rotations keep height O(log n)."),
    ("B-Tree", "Binary trees are tall and cache/disk-unfriendly; B-Trees pack many keys per node (height log_t n)."),
    ("Johnson's algorithm", "Floyd-Warshall is Theta(V^3) even on sparse graphs; Johnson runs Dijkstra from each vertex."),
    ("Held-Karp DP, Branch & Bound, approximation", "Brute-force TSP is O(n!); DP gives O(n^2 2^n); bounds and heuristics prune further."),
    ("FPTAS for knapsack", "0/1 DP is pseudo-polynomial in W; scaling values gives a (1-eps)-approximation in poly(n, 1/eps)."),
    ("Degree / feasibility pruning", "The measured Hamiltonian result: a cheap necessary-condition check removes the whole search tree."),
]


def run_families(families, quick):
    all_series = {}
    for fam in families:
        exps = E.FAMILIES[fam]()
        print(f"\n=== Family {exps[0].family} ===")
        out = []
        for exp in exps:
            print(f"  -> {exp.name}   [theory: {exp.theory_label}]")
            s = framework.run_experiment(exp, verbose=True, quick=quick)
            out.append((s, risk.classify(s)))
        all_series[fam] = out
    return all_series


def summary_rows(all_series):
    rows = []
    for fam, items in all_series.items():
        for s, a in items:
            last = s.results[-1]
            expo = "-" if a.exponent is None else f"{a.exponent:.2f}"
            rows.append([s.exp.family.split('.')[0], s.exp.name, s.exp.theory_label, a.max_size, f"{last.ops:,}",
                         f"{a.max_time:.3f}", f"{a.peak_kb / 1024:.1f}" if a.peak_kb else "-", expo, a.risk,
                         "; ".join(a.reasons)])
    return rows


HEAD = ["Fam", "Experiment", "Theory", "Max n", "Ops @max", "Time(s) max", "Peak MB", "Fit exp", "RISK", "Reason"]


def print_summary(rows):
    print("\n" + "=" * 110 + "\nRISK SUMMARY\n" + "=" * 110)
    for r in rows:
        print(f"[{r[8]:8}] F{r[0]} {r[1]}\n           theory {r[2]} | max n={r[3]} | ops={r[4]} | time={r[5]}s | {r[9]}")


def save_csv(all_series, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["family", "experiment", "theory", "n", "ops", "time_s", "peak_kb", "status", "counters", "note"])
        for items in all_series.values():
            for s, _ in items:
                for r in s.results:
                    w.writerow([s.exp.family, s.exp.name, s.exp.theory_label, r.size, r.ops, f"{r.time_s:.6f}",
                                "" if r.peak_kb is None else f"{r.peak_kb:.1f}", r.status,
                                ";".join(f"{k}={v}" for k, v in sorted(r.counters.items())), r.note])


def save_report(rows, all_series, path, include_np):
    L = ["# DAA Algorithm Vulnerability and Stress-Testing Report", "",
         f"Generated {time.strftime('%Y-%m-%d %H:%M')}. Risk thresholds: time > {risk.T_MODERATE}s moderate, > {risk.T_HIGH}s high; "
         f"peak memory > {risk.MEM_MODERATE_KB // 1024} MB moderate; fitted exponent >= {risk.EXPONENT_MODERATE} moderate; "
         "budget exceeded = high.", "",
         "## Risk summary", "", "| " + " | ".join(HEAD) + " |", "|" + "---|" * len(HEAD)]
    L += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    L += ["", "## Measurements per experiment"]
    for items in all_series.values():
        for s, a in items:
            L += ["", f"### {s.exp.family}: {s.exp.name}", f"Theory: {s.exp.theory_label}. Risk: **{a.risk}** ({'; '.join(a.reasons)})", "",
                  "| n | ops | time (s) | peak KB | status | counters |", "|---|---|---|---|---|---|"]
            for r in s.results:
                c = ", ".join(f"{k}={v:,}" for k, v in sorted(r.counters.items()))
                L.append(f"| {r.size} | {r.ops:,} | {r.time_s:.4f} | {'' if r.peak_kb is None else f'{r.peak_kb:.0f}'} | {r.status} | {c} |")
    if include_np:
        L += ["", "## Complexity classification (family 6)", "", complexity.markdown_table()]
    L += ["", "## Knapsack matched dataset", "", "```"] + [f"{k}: {v}" for k, v in E.knapsack_demo().items()] + ["```"]
    L += ["", "## Gaps in older algorithms that motivated new ones", ""] + [f"- **{a}**: {b}" for a, b in GAPS]
    with open(path, "w") as f:
        f.write("\n".join(L) + "\n")


def save_plots(all_series, outdir):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed - skipping plots (pip install matplotlib)")
        return
    for fam, items in all_series.items():
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        for s, a in items:
            ok = s.ok
            if len(ok) < 2:
                continue
            xs = [r.size for r in ok]
            line, = ax1.plot(xs, [max(r.ops, 1) for r in ok], marker="o", label=s.exp.name)
            t0 = s.exp.theory_fn(ok[0].meta)
            if t0 > 0 and ok[0].ops > 0:
                ax1.plot(xs, [ok[0].ops * s.exp.theory_fn(r.meta) / t0 for r in ok], "--", color=line.get_color(), alpha=0.5)
            ax2.plot(xs, [max(r.time_s, 1e-6) for r in ok], marker="o", color=line.get_color())
        for ax, title, yl in ((ax1, "Counted operations vs size (dashed = theoretical shape)", "operations"),
                              (ax2, "Wall-clock time vs size", "seconds")):
            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.set_xlabel("size parameter n")
            ax.set_ylabel(yl)
            ax.set_title(title)
            ax.grid(True, which="both", alpha=0.3)
        ax1.legend(fontsize=7)
        fig.suptitle(items[0][0].exp.family)
        fig.tight_layout()
        p = os.path.join(outdir, f"family{fam}.png")
        fig.savefig(p, dpi=130)
        plt.close(fig)
        print("saved", p)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--family", type=int, nargs="*", choices=range(1, 7))
    ap.add_argument("--out", default="results")
    ap.add_argument("--no-plots", action="store_true")
    args = ap.parse_args()
    fams = args.family or [1, 2, 3, 4, 5, 6]
    os.makedirs(args.out, exist_ok=True)
    t0 = time.time()
    all_series = run_families([f for f in fams if f in E.FAMILIES], args.quick)
    rows = summary_rows(all_series)
    print_summary(rows)
    if 3 in fams:
        print("\nKnapsack matched dataset:")
        for k, v in E.knapsack_demo().items():
            print(f"  {k}: {v}")
    if 6 in fams:
        print("\n=== Family 6: complexity classification ===\n" + complexity.format_table())
    save_csv(all_series, os.path.join(args.out, "results.csv"))
    save_report(rows, all_series, os.path.join(args.out, "report.md"), 6 in fams)
    if not args.no_plots:
        save_plots(all_series, args.out)
    print(f"\nDone in {time.time() - t0:.0f}s. See {args.out}/report.md and {args.out}/results.csv")


if __name__ == "__main__":
    main()
