"""The plug-in interface of the lab:  generate -> prepare -> run -> measure -> (risk.py) classify.

To test a new algorithm, create one Experiment(...) - nothing else in the framework changes."""
import random
import time
import tracemalloc
from dataclasses import dataclass, field
from typing import Callable, Optional

from metrics import BudgetExceeded, Counter

MEM_RERUN_MAX_SECONDS = 1.0     # re-run under tracemalloc (slow) only if the timed run was quick


@dataclass
class Experiment:
    family: str                      # e.g. "1. Advanced data structures"
    name: str                        # e.g. "Fibonacci heap: insert + extract-min"
    sizes: list                      # increasing size parameter n
    make_input: Callable             # (size, rng) -> (input, meta dict)      [GENERATE]
    run: Callable                    # (state, ctr) -> None | dict            [EXECUTE]
    theory_label: str                # e.g. "O(n log n)"
    theory_fn: Callable              # meta -> predicted number of counted ops
    theory_class: str = "poly"       # 'poly' or 'exp' (decides how growth is judged)
    ops_keys: Optional[tuple] = None  # counters summed into the primary 'ops' measure
    prepare: Optional[Callable] = None  # input -> state (setup that must NOT be timed/counted)
    state_limit: Optional[int] = None   # budget: max states/cells before declaring infeasible
    time_limit: float = 20.0            # budget in seconds (checked by Counter.tick)
    seed: int = 42
    note: str = ""


@dataclass
class Result:
    size: int
    meta: dict
    ops: int
    counters: dict
    time_s: float
    peak_kb: Optional[float]
    status: str            # "OK" or "BUDGET"
    note: str = ""
    info: dict = field(default_factory=dict)


@dataclass
class Series:
    exp: Experiment
    results: list = field(default_factory=list)

    @property
    def ok(self):
        return [r for r in self.results if r.status == "OK"]


def _run_once(exp, inp, meta, size):
    state = exp.prepare(inp) if exp.prepare else inp
    ctr = Counter(exp.state_limit, exp.time_limit)
    status, note, info = "OK", "", {}
    t0 = time.perf_counter()
    try:
        out = exp.run(state, ctr)
        if isinstance(out, dict):
            info = out
    except BudgetExceeded as e:
        status, note = "BUDGET", str(e)
    elapsed = time.perf_counter() - t0
    peak = None
    if status == "OK" and elapsed < MEM_RERUN_MAX_SECONDS:
        state2 = exp.prepare(inp) if exp.prepare else inp
        ctr2 = Counter(exp.state_limit, exp.time_limit)
        tracemalloc.start()
        try:
            exp.run(state2, ctr2)
            peak = tracemalloc.get_traced_memory()[1] / 1024
        finally:
            tracemalloc.stop()
    return Result(size, meta, ctr.total(exp.ops_keys), dict(ctr.counts), elapsed, peak, status, note, info)


def run_experiment(exp, verbose=True, quick=False):
    sizes = exp.sizes[:max(3, len(exp.sizes) - 2)] if quick else exp.sizes
    series = Series(exp)
    for size in sizes:
        rng = random.Random(exp.seed + size)
        inp, meta = exp.make_input(size, rng)
        meta = dict(meta)
        meta["n"] = size
        res = _run_once(exp, inp, meta, size)
        series.results.append(res)
        if verbose:
            flag = "" if res.status == "OK" else f"  <-- {res.status}: {res.note}"
            print(f"    n={size:<8} ops={res.ops:<12,} time={res.time_s:8.4f}s{flag}")
        if res.status != "OK":
            break          # no point testing larger sizes once the budget is blown
    return series
