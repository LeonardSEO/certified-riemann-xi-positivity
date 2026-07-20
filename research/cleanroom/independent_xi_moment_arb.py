#!/usr/bin/env python3
"""Independent Arb certificate for the degree-10 Xi moment minorant.

This implementation intentionally does not import or execute the repository's
published certificate.  It evaluates derivatives of H_n directly from the
Leibniz formula, rather than constructing H_n as a power series.

Run (assertions are proof obligations; do not use Python -O):

    uv run --with python-flint==0.9.0 \
      python research/cleanroom/independent_xi_moment_arb.py
"""

from __future__ import annotations

import math
import platform

import flint
from flint import arb, arb_series, ctx


PRECISION_DIGITS = 90
SERIES_LENGTH = 16
MAX_MOMENT_INDEX = 10


def exact_ratio(numerator: int, denominator: int) -> arb:
    return arb(numerator) / arb(denominator)


def xi_derivatives(center: str, last_order: int) -> list[arb]:
    """Enclose xi^(k)(center), 0 <= k <= last_order.

    Gamma(1+s/2) removes the apparent s=0 singularity before Arb sees it:

      xi(s) = (s-1) pi^(-s/2) Gamma(1+s/2) zeta(s).
    """
    s = arb_series([arb(center), arb(1)])
    xi = (
        (s - 1)
        * (-s * arb.pi().log() / 2).exp()
        * (1 + s / 2).gamma()
        * s.zeta()
    )
    coefficients = xi.coeffs()
    assert len(coefficients) > last_order
    return [coefficients[k] * math.factorial(k) for k in range(last_order + 1)]


def h_derivative(xi_d: list[arb], n: int, r: int) -> arb:
    """Compute H_n^(r) from xi derivatives at one common center.

    H_n(s) = sum_l (-1)^l C(n,l) xi^(l)(s) xi^(n-l)(s).
    A second Leibniz expansion gives the expression evaluated here.
    """
    total = arb(0)
    for ell in range(n + 1):
        alternating_binomial = (-1) ** ell * math.comb(n, ell)
        for a in range(r + 1):
            total += (
                alternating_binomial
                * math.comb(r, a)
                * xi_d[ell + a]
                * xi_d[n - ell + r - a]
            )
    return total


def endpoint_vector(center: str) -> list[arb]:
    """Return [A_0,A_2,...,A_10] at y=0 or y=1/2."""
    derivatives = xi_derivatives(center, MAX_MOMENT_INDEX + 2)
    answer: list[arb] = []
    for n in range(0, MAX_MOMENT_INDEX + 1, 2):
        if center == "0.5":
            answer.append(h_derivative(derivatives, n, 2))
        elif center == "0":
            answer.append(-2 * h_derivative(derivatives, n, 1))
        else:
            raise ValueError("only the two analytic endpoints are supported")
    return answer


def evaluate_power(coefficients: list[arb], t: arb) -> arb:
    value = arb(0)
    for coefficient in reversed(coefficients):
        value = value * t + coefficient
    return value


def certify_global_decrease(q: list[arb]) -> tuple[list[arb], list[arb]]:
    """Prove Q'(t)<0 for every t>=0, using an independent split at t=50."""
    dq = [(k + 1) * q[k + 1] for k in range(len(q) - 1)]
    degree = len(dq) - 1
    split = 50

    # Convert Q'(50*s) from powers of s to degree-4 Bernstein coefficients.
    scaled_power = [dq[k] * split**k for k in range(degree + 1)]
    bernstein: list[arb] = []
    for j in range(degree + 1):
        b_j = sum(
            (
                scaled_power[k]
                * math.comb(j, k)
                / math.comb(degree, k)
                for k in range(j + 1)
            ),
            arb(0),
        )
        assert b_j < 0
        bernstein.append(b_j)

    # Expand Q'(50+r).  Negative coefficients imply negativity for r>=0.
    shifted: list[arb] = []
    for j in range(degree + 1):
        c_j = sum(
            (
                dq[k] * math.comb(k, j) * split ** (k - j)
                for k in range(j, degree + 1)
            ),
            arb(0),
        )
        assert c_j < 0
        shifted.append(c_j)
    return bernstein, shifted


def main() -> None:
    assert flint.__version__ == "0.9.0"
    ctx.dps = PRECISION_DIGITS
    ctx.cap = SERIES_LENGTH

    # Basic normalization checks on the pole-free formula.
    xi_at_zero = xi_derivatives("0", 1)
    xi_at_center = xi_derivatives("0.5", 1)
    assert xi_at_zero[0].contains(exact_ratio(1, 2))
    assert xi_at_center[1].contains(arb(0))

    at_y_zero = endpoint_vector("0.5")
    at_y_half = endpoint_vector("0")
    assert all(value > 0 for value in at_y_zero + at_y_half)
    assert all(right > left for left, right in zip(at_y_zero, at_y_half))

    # Alternating signs dictate which cross-endpoint normalized bounds enter.
    b2 = at_y_half[1] / at_y_zero[0]
    b4 = at_y_zero[2] / at_y_half[0]
    b6 = at_y_half[3] / at_y_zero[0]
    b8 = at_y_zero[4] / at_y_half[0]
    b10 = at_y_half[5] / at_y_zero[0]
    bounds = [b2, b4, b6, b8, b10]

    # Q(t)=P_theta(sqrt(t)).
    q = [
        arb(1),
        -b2 / math.factorial(2),
        b4 / math.factorial(4),
        -b6 / math.factorial(6),
        b8 / math.factorial(8),
        -b10 / math.factorial(10),
    ]
    bernstein, shifted = certify_global_decrease(q)

    x_lo = exact_ratio(70362433, 10_000_000)
    x_hi = exact_ratio(70362434, 10_000_000)
    p_lo = evaluate_power(q, x_lo * x_lo)
    p_hi = evaluate_power(q, x_hi * x_hi)
    assert p_lo > 0
    assert p_hi < 0

    print("CLEAN-ROOM ARB CERTIFICATE: XI DEGREE-10 MOMENT MINORANT")
    print("python", platform.python_version())
    print("python-flint", flint.__version__)
    print("FLINT", flint.__FLINT_VERSION__)
    print("decimal digits", ctx.dps, "binary bits", ctx.prec, "series cap", ctx.cap)
    print("normalization xi(0) encloses 1/2:", xi_at_zero[0])
    print("functional-equation check xi'(1/2) encloses 0:", xi_at_center[1])

    print("\nENDPOINT MOMENTS A_2j(0) = H_2j''(1/2)")
    for j, value in enumerate(at_y_zero):
        print(f"A_{2*j}(0) = {value}")
    print("\nENDPOINT MOMENTS A_2j(1/2) = -2 H_2j'(0)")
    for j, value in enumerate(at_y_half):
        print(f"A_{2*j}(1/2) = {value}")

    print("\nCROSS-ENDPOINT COEFFICIENT BALLS B_2,...,B_10")
    for j, value in enumerate(bounds, start=1):
        print(f"B_{2*j} = {value}")

    print("\nBERNSTEIN BALLS FOR Q'(50*s), 0<=s<=1")
    for value in bernstein:
        print(value)
    print("\nPOWER COEFFICIENT BALLS FOR Q'(50+r), r>=0")
    for value in shifted:
        print(value)

    print("\nROOT SIGN CERTIFICATES")
    print("P(7.0362433) =", p_lo, "> 0")
    print("P(7.0362434) =", p_hi, "< 0")
    print("Q'(t) < 0 for every t >= 0: CERTIFIED")
    print("unique positive root R_10 in (7.0362433, 7.0362434): CERTIFIED")
    print(
        "boundary strictness at |x|=R_10 follows analytically from "
        "cos(r)>T_10(r) off r=0 on positive measure"
    )
    print("ALL CLEAN-ROOM ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
