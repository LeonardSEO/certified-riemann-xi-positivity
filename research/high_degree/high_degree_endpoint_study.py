#!/usr/bin/env python3
"""Independent high-degree endpoint-moment / first-root experiment.

The certified path uses only python-flint/Arb balls.  The separately labelled
ordinary path converts coefficient midpoints to IEEE binary64 and uses NumPy.
No value from the ordinary path is used by a certificate assertion.
"""

from __future__ import annotations

import argparse
import json
import math
import platform
import resource
import sys
import time
from fractions import Fraction
from pathlib import Path

import flint
from flint import arb, arb_series, ctx


EPSILONS = ("0", "1/4", "1/8", "1/16", "1/32", "1e-2", "1e-3")
DEFAULT_M = tuple(range(21)) + (25, 30, 40, 50)


def parse_rational(text: str) -> Fraction:
    if "/" in text:
        a, b = text.split("/", 1)
        return Fraction(int(a), int(b))
    return Fraction(text)


def aball(q: Fraction) -> arb:
    return arb(q.numerator) / q.denominator


def xi_derivatives(center: Fraction, order: int) -> list[arb]:
    """Return xi^(k)(center), independently from endpoint formulas."""
    s = arb_series([aball(center), arb(1)])
    xi = (s - 1) * (-s * arb.pi().log() / 2).exp() * (1 + s / 2).gamma() * s.zeta()
    cs = xi.coeffs()
    return [cs[k] * math.factorial(k) for k in range(order + 1)]


def h_prime(d: list[arb], n: int) -> arb:
    total = arb(0)
    for ell in range(n + 1):
        total += (-1) ** ell * math.comb(n, ell) * (
            d[ell + 1] * d[n - ell] + d[ell] * d[n - ell + 1]
        )
    return total


def h_second(d: list[arb], n: int) -> arb:
    total = arb(0)
    for ell in range(n + 1):
        total += (-1) ** ell * math.comb(n, ell) * (
            d[ell + 2] * d[n - ell]
            + 2 * d[ell + 1] * d[n - ell + 1]
            + d[ell] * d[n - ell + 2]
        )
    return total


def moments(epsilon: Fraction, max_j: int) -> list[arb]:
    center = Fraction(1, 2) - epsilon
    d = xi_derivatives(center, 2 * max_j + 2)
    out = []
    for j in range(max_j + 1):
        n = 2 * j
        a = h_second(d, n) if epsilon == 0 else -h_prime(d, n) / aball(epsilon)
        if not a > 0:
            raise ArithmeticError(f"A_{n}({epsilon}) not certified positive: {a}")
        out.append(a)
    return out


def polynomial(eps_mom: list[arb], half_mom: list[arb], m: int) -> list[arb]:
    """Coefficients q_j in Phat(sqrt(t)) = sum q_j t^j."""
    q = [arb(1)]
    for j in range(1, 2 * m + 2):
        ratio = (eps_mom[j] / half_mom[0]) if j % 2 == 0 else (half_mom[j] / eps_mom[0])
        q.append((ratio if j % 2 == 0 else -ratio) / math.factorial(2 * j))
    return q


def horner(coeff: list[arb], x: arb) -> arb:
    y = arb(0)
    for c in reversed(coeff):
        y = y * x + c
    return y


def interval_dyadic(a: int, b: int, exponent: int) -> arb:
    den = 1 << exponent
    return arb(a + b) / (2 * den), arb(b - a) / (2 * den)


def certify_negative_on(coeff: list[arb], right_num: int, exponent: int) -> tuple[bool, int, int]:
    """Adaptive interval-Horner proof on [0,right_num/2^exponent]."""
    stack = [(0, right_num, 0)]
    leaves = 0
    max_depth = 0
    while stack:
        a, b, depth = stack.pop()
        mid, rad = interval_dyadic(a, b, exponent)
        value = horner(coeff, arb(mid, rad))
        if value < 0:
            leaves += 1
            max_depth = max(max_depth, depth)
            continue
        if depth >= 24 or b - a <= 1:
            return False, leaves, max_depth
        c = (a + b) // 2
        stack.append((c, b, depth + 1))
        stack.append((a, c, depth + 1))
    return True, leaves, max_depth


def certified_first_root(q: list[arb], bisect_bits: int) -> dict:
    # A power-of-two search gives an exact dyadic sign-changing interval in t.
    hi = 1
    while not horner(q, arb(hi)) < 0:
        hi *= 2
        if hi > (1 << 30):
            raise ArithmeticError("no sign change found below t=2^30")
    lo_num, hi_num, exponent = 0, hi, 0
    for _ in range(bisect_bits):
        lo_num *= 2
        hi_num *= 2
        exponent += 1
        mid = (lo_num + hi_num) // 2
        v = horner(q, arb(mid) / (1 << exponent))
        if v > 0:
            lo_num = mid
        elif v < 0:
            hi_num = mid
        else:
            raise ArithmeticError("root bisection sign indeterminate; increase precision")
    assert horner(q, arb(lo_num) / (1 << exponent)) > 0
    assert horner(q, arb(hi_num) / (1 << exponent)) < 0
    derivative = [(j + 1) * q[j + 1] for j in range(len(q) - 1)]
    monotone, leaves, depth = certify_negative_on(derivative, hi_num, exponent)
    # If monotonicity is certified, this sign-changing bracket is necessarily
    # the first positive root, and q is positive throughout [0,t_lo].
    certified_first = monotone
    tlo, thi = arb(lo_num) / (1 << exponent), arb(hi_num) / (1 << exponent)
    return {
        "certified_first_root": certified_first,
        "certified_strictly_decreasing_before_root": monotone,
        "t_lower_dyadic_numerator": str(lo_num),
        "t_upper_dyadic_numerator": str(hi_num),
        "t_dyadic_exponent": exponent,
        "x_lower_arb": str(tlo.sqrt()),
        "x_upper_arb": str(thi.sqrt()),
        "derivative_interval_leaves": leaves,
        "derivative_max_subdivision_depth": depth,
    }


def ordinary_roots(q: list[arb]) -> dict:
    """Non-rigorous binary64 sign-search/bisection on midpoint coefficients."""
    c = [float(x.mid()) for x in q]
    def ev(t: float) -> float:
        y = 0.0
        for a in reversed(c):
            y = y * t + a
        return y
    hi = 1.0
    while ev(hi) >= 0.0 and hi < 2.0**30:
        hi *= 2.0
    if hi >= 2.0**30:
        return {"method": "midpoint-binary64-bisection", "first_sign_change_t": None,
                "first_sign_change_x": None}
    lo = 0.0
    for _ in range(100):
        mid = (lo + hi) / 2.0
        if ev(mid) > 0.0:
            lo = mid
        else:
            hi = mid
    t = (lo + hi) / 2.0
    return {
        "method": "midpoint-binary64-bisection",
        "first_sign_change_t": t,
        "first_sign_change_x": math.sqrt(t),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", nargs="*", type=int, default=list(DEFAULT_M))
    ap.add_argument("--eps", nargs="*", default=list(EPSILONS))
    ap.add_argument("--dps", type=int, default=180)
    ap.add_argument("--bisect-bits", type=int, default=90)
    ap.add_argument("--output", type=Path, required=True)
    ns = ap.parse_args()
    if flint.__version__ != "0.9.0":
        raise RuntimeError(f"requires python-flint 0.9.0, got {flint.__version__}")
    epsilons = [parse_rational(x) for x in ns.eps]
    if any(e < 0 or e > Fraction(1, 2) for e in epsilons):
        raise ValueError("eps must lie in [0,1/2]")
    max_m, max_j = max(ns.m), 2 * max(ns.m) + 1
    ctx.dps = ns.dps
    ctx.cap = 2 * max_j + 3
    ns.output.parent.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    header = {
        "record": "metadata", "python": platform.python_version(),
        "python_flint": flint.__version__, "flint": flint.__FLINT_VERSION__,
        "arb_dps": ctx.dps, "arb_bits": ctx.prec,
        "series_cap": ctx.cap, "max_m": max_m, "max_j": max_j,
        "epsilon_inputs": ns.eps, "m_inputs": ns.m,
    }
    with ns.output.open("w", encoding="utf-8") as f:
        f.write(json.dumps(header, sort_keys=True) + "\n"); f.flush()
        t0 = time.perf_counter()
        half = moments(Fraction(1, 2), max_j)
        f.write(json.dumps({"record":"moment_batch", "epsilon":"1/2", "seconds":time.perf_counter()-t0,
                            "moments":[{"j":j, "order":2*j, "arb":str(a)} for j,a in enumerate(half)]},
                           sort_keys=True)+"\n"); f.flush()
        for eps_text, eps in zip(ns.eps, epsilons):
            t0 = time.perf_counter()
            em = moments(eps, max_j)
            moment_seconds = time.perf_counter() - t0
            f.write(json.dumps({"record":"moment_batch", "epsilon":eps_text, "seconds":moment_seconds,
                                "moments":[{"j":j, "order":2*j, "arb":str(a)} for j,a in enumerate(em)]},
                               sort_keys=True)+"\n"); f.flush()
            for m in ns.m:
                case_start = time.perf_counter()
                q = polynomial(em, half, m)
                try:
                    cert = certified_first_root(q, ns.bisect_bits)
                    failure = None
                except Exception as exc:
                    cert = {"certified_first_root":False, "certified_strictly_decreasing_before_root":False}
                    failure = f"{type(exc).__name__}: {exc}"
                ordinary = ordinary_roots(q)
                rec = {"record":"case", "epsilon":eps_text, "m":m, "degree_x":4*m+2,
                       "moment_seconds_shared":moment_seconds, "case_seconds":time.perf_counter()-case_start,
                       "certified":cert, "ordinary":ordinary, "failure":failure,
                       "max_rss_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform=='darwin' else 1024)}
                f.write(json.dumps(rec, sort_keys=True)+"\n"); f.flush()
        f.write(json.dumps({"record":"complete", "total_seconds":time.perf_counter()-start,
                            "max_rss_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform=='darwin' else 1024)}, sort_keys=True)+"\n")


if __name__ == "__main__":
    main()
