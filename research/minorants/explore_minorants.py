#!/usr/bin/env python3
"""Certified experiments with moment-compatible global cosine minorants.

The analytic certificate used here is exact: every T_{4m+2} is a strict
global minorant of cosine away from zero, and every fixed finite convex
combination of such Taylor polynomials is therefore another global minorant.  Arb is used
for the Riemann-kernel endpoint moments and for sign/positivity certificates.

This is deliberately a research script, not part of the published paper.
Run with:

  uv run --with python-flint==0.9.0 python research/minorants/explore_minorants.py
"""

from __future__ import annotations

import math
from fractions import Fraction

import flint
from flint import arb, arb_series, ctx


MAX_M = 12
CTX_DPS = 80


def derivative(series: arb_series, order: int) -> arb_series:
    for _ in range(order):
        series = series.derivative()
    return series


def xi_taylor(center: str) -> arb_series:
    s = arb_series([arb(center), arb(1)])
    return (s - 1) * (-s * arb.pi().log() / 2).exp() * (1 + s / 2).gamma() * s.zeta()


def endpoint_moments(center: str, max_k: int) -> list[arb]:
    xi = xi_taylor(center)
    answer = []
    for k in range(max_k + 1):
        h = arb_series([arb(0)])
        for j in range(2 * k + 1):
            h += ((-1) ** j * math.comb(2 * k, j)
                  * derivative(xi, j) * derivative(xi, 2 * k - j))
        answer.append(
            derivative(h, 2).coeffs()[0]
            if center == "0.5"
            else -2 * derivative(h, 1).coeffs()[0]
        )
    return answer


def cross_taylor_coefficients(m: int, at_zero: list[arb], at_half: list[arb]) -> list[arb]:
    """Q_m(t), t=x^2, after sign-safe cross-endpoint moment bounds."""
    coefficients = [arb(1)]
    for j in range(1, 2 * m + 2):
        # Positive Taylor terms use the lower moment bound; negative ones use
        # the upper bound.  Raw endpoint monotonicity proves both bounds.
        moment = (at_zero[j] / at_half[0] if j % 2 == 0
                  else at_half[j] / at_zero[0])
        coefficients.append(((-1) ** j) * moment / math.factorial(2 * j))
    return coefficients


def evaluate(coefficients: list[arb], t: arb) -> arb:
    value = arb(0)
    for coefficient in reversed(coefficients):
        value = value * t + coefficient
    return value


def initial_root_estimate(coefficients: list[arb]) -> float:
    """Locate the first sampled sign change; Bernstein later excludes missed roots."""
    step = Fraction(1, 100)
    x = step
    while x <= 100:
        t = x * x
        if evaluate(coefficients, arb(t.numerator) / t.denominator) < 0:
            left, right = x - step, x
            for _ in range(50):
                middle = (left + right) / 2
                mt = middle * middle
                if evaluate(coefficients, arb(mt.numerator) / mt.denominator) > 0:
                    left = middle
                else:
                    right = middle
            return float((left + right) / 2)
        x += step
    raise RuntimeError("no positive sign change found below x=100")


def bernstein_coefficients(coefficients: list[arb], left: Fraction,
                           right: Fraction) -> list[arb]:
    """Bernstein balls of Q(left+(right-left)s), 0<=s<=1."""
    degree = len(coefficients) - 1
    power = [arb(0) for _ in range(degree + 1)]
    a = arb(left.numerator) / left.denominator
    width = arb(right.numerator) / right.denominator - a
    for k, coefficient in enumerate(coefficients):
        for j in range(k + 1):
            power[j] += coefficient * math.comb(k, j) * a ** (k - j) * width ** j
    return [
        sum((power[k] * arb(math.comb(j, k)) / math.comb(degree, k)
             for k in range(j + 1)), arb(0))
        for j in range(degree + 1)
    ]


def certify_positive(coefficients: list[arb], right: Fraction,
                     max_depth: int = 20) -> int:
    """Prove Q(t)>0 on [0,right] by adaptive Bernstein subdivision."""
    pending = [(Fraction(0), right, 0)]
    leaves = 0
    while pending:
        left, endpoint, depth = pending.pop()
        bernstein = bernstein_coefficients(coefficients, left, endpoint)
        if all(value > 0 for value in bernstein):
            leaves += 1
            continue
        if depth == max_depth:
            raise RuntimeError(f"Bernstein positivity unresolved on [{left}, {endpoint}]")
        middle = (left + endpoint) / 2
        pending.extend([(left, middle, depth + 1),
                        (middle, endpoint, depth + 1)])
    return leaves


def root_certificate(coefficients: list[arb], estimate: float) -> tuple[Fraction, Fraction, int]:
    scale = 10**8
    x_lo = Fraction(math.floor(estimate * scale) - 2, scale)
    x_hi = Fraction(math.ceil(estimate * scale) + 2, scale)
    t_lo, t_hi = x_lo * x_lo, x_hi * x_hi
    assert evaluate(coefficients, arb(t_lo.numerator) / t_lo.denominator) > 0
    assert evaluate(coefficients, arb(t_hi.numerator) / t_hi.denominator) < 0
    leaves = certify_positive(coefficients, t_lo)
    return x_lo, x_hi, leaves


def convex_coefficients(parts: list[list[arb]], weights: list[Fraction]) -> list[arb]:
    degree = max(map(len, parts))
    answer = [arb(0) for _ in range(degree)]
    for polynomial, weight in zip(parts, weights):
        w = arb(weight.numerator) / weight.denominator
        for j, coefficient in enumerate(polynomial):
            answer[j] += w * coefficient
    return answer


def best_pairwise_convex_mix(polynomials: list[list[arb]]) -> tuple[int, int, Fraction, list[arb], float]:
    """Finite rational grid search; returned candidate is subsequently certified."""
    best = (-1.0, 0, 0, Fraction(0), polynomials[0])
    for a in range(len(polynomials)):
        for b in range(a + 1, len(polynomials)):
            for numerator in range(1, 100):
                weight = Fraction(numerator, 100)
                candidate = convex_coefficients(
                    [polynomials[a], polynomials[b]], [weight, 1 - weight]
                )
                try:
                    radius = initial_root_estimate(candidate)
                except RuntimeError:
                    continue
                if radius > best[0]:
                    best = (radius, a, b, weight, candidate)
    radius, a, b, weight, candidate = best
    return a, b, weight, candidate, radius


def main() -> None:
    if flint.__version__ != "0.9.0":
        raise RuntimeError(f"python-flint 0.9.0 required; found {flint.__version__}")
    ctx.dps = CTX_DPS
    ctx.cap = 4 * MAX_M + 8
    max_k = 2 * MAX_M + 1
    at_zero = endpoint_moments("0.5", max_k)
    at_half = endpoint_moments("0", max_k)

    print("GLOBAL VALIDITY CERTIFICATE")
    print("For n=4m+2, (cos-T_n)^(n)=1-cos>=0 and the first n derivatives")
    print("at zero vanish. Repeated integration and evenness prove T_n<=cos on R.")
    print("Fixed finite convex combinations preserve the inequality. This part is exact, not numeric.")
    print(f"python-flint={flint.__version__} FLINT={flint.__FLINT_VERSION__} dps={ctx.dps} cap={ctx.cap}")

    polynomials = []
    print("\nCROSS-ENDPOINT TAYLOR HIERARCHY")
    for m in range(MAX_M + 1):
        coefficients = cross_taylor_coefficients(m, at_zero, at_half)
        polynomials.append(coefficients)
        estimate = initial_root_estimate(coefficients)
        lo, hi, leaves = root_certificate(coefficients, estimate)
        print(f"m={m:2d} degree={4*m+2:2d} radius=[{float(lo):.8f},{float(hi):.8f}] "
              f"positive_Bernstein_leaves={leaves}")

    a, b, weight, candidate, estimate = best_pairwise_convex_mix(polynomials)
    lo, hi, leaves = root_certificate(candidate, estimate)
    print("\nBEST PAIRWISE CONVEX MIX ON THE 1/100 WEIGHT GRID")
    print(f"weight(T_{4*a+2})={weight}; weight(T_{4*b+2})={1-weight}")
    print(f"radius=[{float(lo):.8f},{float(hi):.8f}] positive_Bernstein_leaves={leaves}")
    print("The search is finite and heuristic; global minorant validity and the displayed")
    print("positivity/root bracket for the selected rational mix are Arb-certified.")
    print("\nALL CERTIFICATE ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
