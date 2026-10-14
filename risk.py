"""Risk classifier: turns a Series of measurements into Low / Moderate / High with a written reason.

Thresholds are constants so the team can tune them and quote them in the report."""
import math
from dataclasses import dataclass

T_MODERATE = 0.5          # seconds at the largest tested size
T_HIGH = 5.0
MEM_MODERATE_KB = 50_000  # ~50 MB peak
MEM_HIGH_KB = 500_000     # ~500 MB peak
DRIFT_MODERATE = 2.0      # measured growth > 2x faster than the theoretical bound => suspicious
EXPONENT_MODERATE = 1.8   # polynomial growth with fitted exponent >= 1.8 (doubling n => >= 3.5x ops)
EXP_GROWTH_MODERATE = 1_000   # exponential-class algorithm whose ops grew >1000x over the tested range

ORDER = {"Low": 0, "Moderate": 1, "High": 2}


@dataclass
class Assessment:
    risk: str
    reasons: list
    exponent: float      # fitted slope of log(ops) vs log(n)  (None if not computable)
    drift: float         # worst (observed growth / theoretical growth) between consecutive sizes
    max_size: int
    max_time: float
    peak_kb: float


def fitted_exponent(results):
    pts = [(math.log(r.size), math.log(r.ops)) for r in results if r.ops > 0 and r.size > 1]
    if len(pts) < 2:
        return None
    mx, my = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
    den = sum((p[0] - mx) ** 2 for p in pts)
    return None if den == 0 else sum((p[0] - mx) * (p[1] - my) for p in pts) / den


def classify(series):
    exp, res = series.exp, series.results
    ok = series.ok
    reasons, risk = [], "Low"

    def raise_to(level, why):
        nonlocal risk
        reasons.append(why)
        if ORDER[level] > ORDER[risk]:
            risk = level

    blown = [r for r in res if r.status != "OK"]
    if blown:
        raise_to("High", f"budget exceeded at n={blown[0].size} ({blown[0].note})")

    max_time = max((r.time_s for r in res), default=0.0)
    peaks = [r.peak_kb for r in ok if r.peak_kb is not None]
    peak = max(peaks, default=0.0)
    if max_time > T_HIGH:
        raise_to("High", f"{max_time:.1f}s at the largest size")
    elif max_time > T_MODERATE:
        raise_to("Moderate", f"{max_time:.2f}s at the largest size")
    if peak > MEM_HIGH_KB:
        raise_to("High", f"peak memory {peak / 1024:.0f} MB")
    elif peak > MEM_MODERATE_KB:
        raise_to("Moderate", f"peak memory {peak / 1024:.0f} MB")

    drift = 1.0
    for a, b in zip(ok, ok[1:]):
        ta, tb = exp.theory_fn(a.meta), exp.theory_fn(b.meta)
        if a.ops > 0 and ta > 0 and tb > 0:
            drift = max(drift, (b.ops / a.ops) / (tb / ta))
    if drift > DRIFT_MODERATE:
        raise_to("Moderate", f"ops grow {drift:.1f}x faster than the {exp.theory_label} model")

    expo = fitted_exponent(ok)
    if exp.theory_class == "poly" and expo is not None and expo >= EXPONENT_MODERATE:
        raise_to("Moderate", f"super-linear growth, fitted exponent n^{expo:.2f} (doubling n multiplies ops by {2 ** expo:.1f})")

    if exp.theory_class == "exp" and len(ok) >= 2 and ok[0].ops > 0:
        growth = ok[-1].ops / ok[0].ops
        if growth >= EXP_GROWTH_MODERATE:
            raise_to("Moderate", f"exponential-class: ops grew x{growth:,.0f} over n={ok[0].size}..{ok[-1].size}")

    if not reasons:
        reasons.append(f"practical up to n={ok[-1].size if ok else '-'} and follows {exp.theory_label}")
    return Assessment(risk, reasons, fitted_exponent(ok), drift,
                      max(r.size for r in res), max_time, peak)


def family_risk(assessments):
    return max((a.risk for a in assessments), key=lambda r: ORDER[r], default="Low")
