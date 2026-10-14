"""Counters and budgets shared by every algorithm in the lab."""
import time
from collections import defaultdict


class BudgetExceeded(Exception):
    """Raised when a test blows its state/time budget. The framework treats this as 'infeasible'."""


class Counter:
    """Counts abstract operations (comparisons, links, states ...). Optional budgets stop runaway tests."""

    def __init__(self, state_limit=None, time_limit=None):
        self.counts = defaultdict(int)
        self.state_limit = state_limit
        self.time_limit = time_limit
        self._t0 = time.perf_counter()

    def inc(self, key, n=1):
        self.counts[key] += n

    def set_max(self, key, value):
        if value > self.counts[key]:
            self.counts[key] = value

    def tick(self, key="states"):
        """Count one search state and enforce the budgets (used by exponential searches)."""
        c = self.counts[key] + 1
        self.counts[key] = c
        if self.state_limit is not None and c > self.state_limit:
            raise BudgetExceeded(f"{key} exceeded budget of {self.state_limit:,}")
        if self.time_limit is not None and (c & 4095) == 0 \
                and time.perf_counter() - self._t0 > self.time_limit:
            raise BudgetExceeded(f"time exceeded {self.time_limit}s")

    def __getitem__(self, key):
        return self.counts[key]

    def total(self, keys=None):
        if keys is None:
            return sum(self.counts.values())
        return sum(self.counts[k] for k in keys)
