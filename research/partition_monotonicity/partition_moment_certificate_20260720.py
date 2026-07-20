#!/usr/bin/env python3
"""Arb certificate for y-variation of normalized Riemann-kernel moments.

Required dependency: python-flint==0.9.0.  Do not run with ``python -O``:
assertions are the certificate.  All decisions are strict Arb ball comparisons.

For h_k(y) = H_{2k}(1/2-y), one has A_{2k}(y)=h_k'(y)/y and hence

    m_{2k}(y) = h_k'(y)/h_0'(y)                    (y > 0).

On cells bounded away from zero, formal Arb differentiation with an interval
constant term encloses m', m'', and (log m)''.  The zero cell is handled by a
Taylor-remainder enclosure for A and A'/y, avoiding division by an interval
containing zero.
"""

from __future__ import annotations

import argparse
import math
import platform

import flint
from flint import arb, arb_series, ctx


REQUIRED_FLINT = "0.9.0"
DEFAULT_DPS = 80
DEFAULT_MOMENTS = 6
DEFAULT_CELLS = 1000
ZERO_RADIUS = "0.01"
ZERO_DENOMINATOR = 100
ZERO_TAYLOR_K = 14


def derivative(series: arb_series, order: int = 1) -> arb_series:
    result = series
    for _ in range(order):
        result = result.derivative()
    return result


def xi_from_s(s: arb_series) -> arb_series:
    log_pi = arb.pi().log()
    return (s - 1) * (-s * log_pi / 2).exp() * (1 + s / 2).gamma() * s.zeta()


def h_series_from_y(y: arb_series, max_k: int) -> list[arb_series]:
    """Return H_{0}, H_{2}, ..., H_{2 max_k} at s=1/2-y."""
    s = arb("0.5") - y
    xi = xi_from_s(s)
    xi_y_derivatives = [derivative(xi, ell) for ell in range(2 * max_k + 1)]
    result = []
    for k in range(max_k + 1):
        h = arb_series([arb(0)])
        # xi_y^(ell)=(-1)^ell xi_s^(ell).  Since the product of the two
        # conversion signs is (-1)^(2k)=1, the defining (-1)^ell remains.
        for ell in range(2 * k + 1):
            h += (
                (-1) ** ell
                *
                math.comb(2 * k, ell)
                * xi_y_derivatives[ell]
                * xi_y_derivatives[2 * k - ell]
            )
        result.append(h)
    return result


def rational_interval_parts(
    mid_numerator: int, denominator: int, radius_numerator: int
) -> tuple[arb, arb, arb]:
    mid = arb(mid_numerator) / denominator
    radius = arb(radius_numerator) / denominator
    cell = arb(mid, radius)
    return mid, radius, cell


def regular_cell(
    midpoint: arb, radius: arb, cell: arb, max_k: int, taylor_order: int = 12
) -> tuple[arb, list[arb]]:
    """Enclose h_0' and the sign numerators of m' on a positive cell.

    Special functions are evaluated at the point midpoint.  Taylor's theorem
    with an interval enclosure of the final derivative supplies the remainder;
    this is substantially sharper than direct dependency-heavy interval zeta.
    """
    # N_k=h_k''h_0'-h_k'h_0'' has the sign of m_k'.  Constructing N_k
    # before interval evaluation preserves the cancellation that a quotient
    # of independently widened derivative balls would destroy.
    needed = 2 + taylor_order
    old_cap = ctx.cap
    ctx.cap = max(ctx.cap, 2 * max_k + needed + 6)
    try:
        point_hs = h_series_from_y(arb_series([midpoint, arb(1)]), max_k)
        interval_hs = h_series_from_y(arb_series([cell, arb(1)]), max_k)
        t = arb(0, radius)
        def taylor_enclosure(point_function: arb_series, interval_function: arb_series) -> arb:
            value = arb(0)
            for n in reversed(range(taylor_order)):
                value = value * t + point_function.coeffs()[n]
            remainder_derivative = abs(
                math.factorial(taylor_order)
                * interval_function.coeffs()[taylor_order]
            )
            error = (
                remainder_derivative.upper()
                * radius ** taylor_order
                / math.factorial(taylor_order)
            )
            return value + arb(0, error.upper())

        h01 = taylor_enclosure(derivative(point_hs[0]), derivative(interval_hs[0]))
        numerators = []
        for k in range(1, max_k + 1):
            point_numerator = (
                derivative(point_hs[k], 2) * derivative(point_hs[0])
                - derivative(point_hs[k]) * derivative(point_hs[0], 2)
            )
            interval_numerator = (
                derivative(interval_hs[k], 2) * derivative(interval_hs[0])
                - derivative(interval_hs[k]) * derivative(interval_hs[0], 2)
            )
            numerators.append(taylor_enclosure(point_numerator, interval_numerator))
    finally:
        ctx.cap = old_cap
    return h01, numerators


def point_h_derivatives(max_k: int, max_order: int) -> list[list[arb]]:
    old_cap = ctx.cap
    ctx.cap = max(ctx.cap, 2 * max_k + max_order + 6)
    try:
        y = arb_series([arb(0), arb(1)])
        hs = h_series_from_y(y, max_k)
        return [
            [math.factorial(n) * h.coeffs()[n] for n in range(max_order + 1)]
            for h in hs
        ]
    finally:
        ctx.cap = old_cap


def interval_h_derivative_sup(max_k: int, radius: str, order: int) -> list[arb]:
    old_cap = ctx.cap
    ctx.cap = max(ctx.cap, 2 * max_k + order + 6)
    try:
        y_cell = arb(f"0 +/- {radius}")
        y = arb_series([y_cell, arb(1)])
        hs = h_series_from_y(y, max_k)
        return [abs(math.factorial(order) * h.coeffs()[order]) for h in hs]
    finally:
        ctx.cap = old_cap


def zero_cell_aprime_over_y(
    max_k: int, radius_text: str, taylor_k: int
) -> tuple[list[arb], list[arb], list[arb]]:
    """Enclose A, A'/y, and m'/y on 0 <= y <= radius.

    Taylor's theorem is applied to the even entire h.  If N=taylor_k,

      A=h'/y = sum_{k=1}^N h^(2k)(0)y^(2k-2)/(2k-1)! + R_A,

    |R_A| <= sup |h^(2N+2)| r^(2N)/(2N+1)!.

    Expanding y h''-h' similarly gives D=A'/y and

    |R_D| <= sup |h^(2N+2)| r^(2N-2)
               * (1/(2N)! + 1/(2N+1)!).
    """
    n = taylor_k
    order = 2 * n + 2
    derivs = point_h_derivatives(max_k, order)
    sup_last = interval_h_derivative_sup(max_k, radius_text, order)
    r = arb(radius_text)
    z = arb(r * r / 2, r * r / 2)
    # z is [0,r^2], formed without relying on a binary float.
    avals: list[arb] = []
    dvals: list[arb] = []
    for j in range(max_k + 1):
        a = arb(0)
        d = arb(0)
        zpow = arb(1)
        for k in range(1, n + 1):
            a += derivs[j][2 * k] * zpow / math.factorial(2 * k - 1)
            if k >= 2:
                d += (
                    (2 * k - 2)
                    * derivs[j][2 * k]
                    * z ** (k - 2)
                    / math.factorial(2 * k - 1)
                )
            zpow *= z
        a_error = sup_last[j] * r ** (2 * n) / math.factorial(2 * n + 1)
        d_error = sup_last[j] * r ** (2 * n - 2) * (
            arb(1) / math.factorial(2 * n) + arb(1) / math.factorial(2 * n + 1)
        )
        a += arb(0, a_error.upper())
        d += arb(0, d_error.upper())
        avals.append(a)
        dvals.append(d)

    ratios = [
        (dvals[k] * avals[0] - avals[k] * dvals[0]) / avals[0] ** 2
        for k in range(1, max_k + 1)
    ]
    return avals, dvals, ratios


def zero_log_second(max_k: int) -> list[arb]:
    """Exact-point enclosure of (log m)''(0)."""
    derivs = point_h_derivatives(max_k, 4)
    result = []
    for k in range(1, max_k + 1):
        # A(0)=h''(0), A''(0)=h''''(0)/3, while A'(0)=0.
        result.append(derivs[k][4] / (3 * derivs[k][2]) - derivs[0][4] / (3 * derivs[0][2]))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cells", type=int, default=DEFAULT_CELLS)
    parser.add_argument("--moments", type=int, default=DEFAULT_MOMENTS)
    parser.add_argument("--dps", type=int, default=DEFAULT_DPS)
    args = parser.parse_args()
    assert flint.__version__ == REQUIRED_FLINT
    assert not __debug__ is False
    assert args.cells >= 2 and args.moments >= 1
    ctx.dps = args.dps
    ctx.cap = max(24, 2 * args.moments + 8)

    print("CERTIFICATE normalized moment y-variation 2026-07-20")
    print("python", platform.python_version())
    print("python-flint", flint.__version__)
    print("dps", ctx.dps, "cells", args.cells, "moments", args.moments)

    avals, dvals, near_zero = zero_cell_aprime_over_y(
        args.moments, ZERO_RADIUS, ZERO_TAYLOR_K
    )
    for k, value in enumerate(near_zero, 1):
        print(f"m_{2*k}'(y)/y on (0,{ZERO_RADIUS}] =", value)
        assert value < 0
    assert all(value > 0 for value in avals)

    log0 = zero_log_second(args.moments)
    for k, value in enumerate(log0, 1):
        print(f"(log m_{2*k})''(0) =", value)
        assert value < 0

    # Rational cells cover [1/Z,1/2] exactly, where Z=ZERO_DENOMINATOR.
    assert ZERO_RADIUS == "0.01" and ZERO_DENOMINATOR == 100
    half_span_numerator = (ZERO_DENOMINATOR - 2) // 2
    denominator = 2 * ZERO_DENOMINATOR * args.cells
    widest_numerator = [None] * args.moments
    for index in range(args.cells):
        midpoint_numerator = 2 * args.cells + half_span_numerator * (2 * index + 1)
        midpoint, radius, cell = rational_interval_parts(
            midpoint_numerator, denominator, half_span_numerator
        )
        h01, numerators = regular_cell(
            midpoint, radius, cell, args.moments
        )
        assert h01 > 0
        for k in range(args.moments):
            assert numerators[k] < 0
            if (
                widest_numerator[k] is None
                or numerators[k].upper() > widest_numerator[k].upper()
            ):
                widest_numerator[k] = numerators[k]

    for k in range(args.moments):
        print(
            f"largest cell upper bound sign numerator for m_{2*(k+1)}' =",
            widest_numerator[k].upper(),
        )
    print("ALL PARTITION MOMENT CERTIFICATE ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
