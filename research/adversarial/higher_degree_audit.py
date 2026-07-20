#!/usr/bin/env python3
"""Independent arbitrary-precision audit of cross-endpoint moment polynomials.

This implementation is derived only from equations (H), (endpoints), and
(Phat) in the paper.  It deliberately does not import the published
certificate.  Arb balls are used for every load-bearing numerical value.
"""

from __future__ import annotations

import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
import math
from typing import Iterable

from flint import acb_poly, arb, arb_series, ctx


def required_series_cap(m: int) -> int:
    """Smallest cap containing xi derivatives through order 4*m+4."""
    if m < 0:
        raise ValueError("m must be nonnegative")
    return 4 * m + 5


def _rational(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def _xi_series(center: arb, cap: int) -> arb_series:
    old_cap = ctx.cap
    try:
        ctx.cap = cap
        s = arb_series([center, arb(1)])
        return (s - 1) * (-s * arb.pi().log() / 2).exp() * (1 + s / 2).gamma() * s.zeta()
    finally:
        ctx.cap = old_cap


def _derivative_values(center: arb, highest: int, cap: int) -> list[arb]:
    if cap <= highest:
        raise ValueError(
            f"series cap {cap} cannot contain required xi derivative {highest}; "
            f"need at least {highest + 1}"
        )
    jet = _xi_series(center, cap)
    coefficients = jet.coeffs()
    if len(coefficients) <= highest:
        raise ArithmeticError("Arb returned a truncated xi jet")
    return [coefficients[k] * math.factorial(k) for k in range(highest + 1)]


def _h_derivative(values: list[arb], n: int, order: int) -> arb:
    """Evaluate d^order/ds^order H_n from the explicit Leibniz sums."""
    total = arb(0)
    for ell in range(n + 1):
        outer = (-1 if ell % 2 else 1) * math.comb(n, ell)
        for a in range(order + 1):
            total += (
                outer
                * math.comb(order, a)
                * values[ell + a]
                * values[n - ell + order - a]
            )
    return total


def endpoint_moments(m: int, cap: int | None = None) -> dict[str, list[arb]]:
    """Return A_0,...,A_(4m+2) at y=0 and y=1/2."""
    needed = required_series_cap(m)
    cap = needed if cap is None else cap
    if cap < needed:
        raise ValueError(f"series cap {cap} is too small; need at least {needed}")
    largest_n = 4 * m + 2
    at_center = _derivative_values(arb(1) / 2, largest_n + 2, cap)
    at_zero = _derivative_values(arb(0), largest_n + 2, cap)
    result_zero: list[arb] = []
    result_half: list[arb] = []
    for n in range(0, largest_n + 1, 2):
        result_zero.append(_h_derivative(at_center, n, 2))
        result_half.append(-2 * _h_derivative(at_zero, n, 1))
    return {"zero": result_zero, "half": result_half}


def endpoint_moments_formal(m: int, cap: int | None = None) -> dict[str, list[arb]]:
    """Cross-check moments by differentiating H_n as an Arb formal series."""
    needed = required_series_cap(m)
    cap = needed if cap is None else cap
    if cap < needed:
        raise ValueError(f"series cap {cap} is too small; need at least {needed}")

    def at(center: arb, endpoint: str) -> list[arb]:
        old_cap = ctx.cap
        try:
            ctx.cap = cap
            xi = _xi_series(center, cap)
            largest_n = 4 * m + 2
            derivatives = [xi]
            for _ in range(largest_n):
                derivatives.append(derivatives[-1].derivative())
            answer: list[arb] = []
            for n in range(0, largest_n + 1, 2):
                h = arb_series([arb(0)])
                for ell in range(n + 1):
                    h += (-1 if ell % 2 else 1) * math.comb(n, ell) * derivatives[ell] * derivatives[n - ell]
                if endpoint == "zero":
                    answer.append(h.derivative().derivative().coeffs()[0])
                else:
                    answer.append(-2 * h.derivative().coeffs()[0])
            return answer
        finally:
            ctx.cap = old_cap

    return {"zero": at(arb(1) / 2, "zero"), "half": at(arb(0), "half")}


def moments_at_epsilon(m: int, epsilon: Fraction, cap: int | None = None) -> list[arb]:
    """Return A_(2j)(epsilon), using -H'_(2j)(1/2-epsilon)/epsilon."""
    if epsilon <= 0 or epsilon > Fraction(1, 2):
        raise ValueError("epsilon must lie in (0, 1/2]")
    needed = required_series_cap(m)
    cap = needed if cap is None else cap
    if cap < needed:
        raise ValueError(f"series cap {cap} is too small; need at least {needed}")
    e = _rational(epsilon)
    largest_n = 4 * m + 2
    values = _derivative_values(arb(1) / 2 - e, largest_n + 1, cap)
    return [-_h_derivative(values, n, 1) / e for n in range(0, largest_n + 1, 2)]


def cross_endpoint_coefficients(
    moments: dict[str, list[arb]], m: int, epsilon_moments: list[arb] | None = None
) -> list[arb]:
    """Coefficients c_j of sum c_j*x^(2j) for Phat_m^(epsilon)."""
    low_endpoint = moments["zero"] if epsilon_moments is None else epsilon_moments
    denominator_low = low_endpoint[0]
    denominator_half = moments["half"][0]
    coefficients = [arb(1)]
    for j in range(1, 2 * m + 2):
        if j % 2 == 0:
            ratio = low_endpoint[j] / denominator_half
            sign = 1
        else:
            ratio = moments["half"][j] / denominator_low
            sign = -1
        coefficients.append(sign * ratio / math.factorial(2 * j))
    return coefficients


def evaluate_even_polynomial(coefficients: Iterable[arb], x: arb) -> arb:
    """Evaluate by Horner in t=x^2, avoiding machine-number overflow."""
    coeffs = list(coefficients)
    t = x * x
    value = arb(0)
    for coefficient in reversed(coeffs):
        value = value * t + coefficient
    return value


def initial_positive_root(
    coefficients: list[arb], lower: Fraction, upper: Fraction, iterations: int = 120
) -> tuple[Fraction, Fraction]:
    """Bisect a rigorously signed +,- bracket using exact rational points."""
    if not evaluate_even_polynomial(coefficients, _rational(lower)) > 0:
        raise ValueError("lower endpoint is not certified positive")
    if not evaluate_even_polynomial(coefficients, _rational(upper)) < 0:
        raise ValueError("upper endpoint is not certified negative")
    for _ in range(iterations):
        middle = (lower + upper) / 2
        value = evaluate_even_polynomial(coefficients, _rational(middle))
        if value > 0:
            lower = middle
        elif value < 0:
            upper = middle
        else:
            raise ArithmeticError("root bisection lost a sign enclosure; increase precision")
    return lower, upper


def endpoint_normalization_failures(
    moments: dict[str, list[arb]], lower_moments: list[arb] | None = None
) -> list[str]:
    failures: list[str] = []
    low = moments["zero"] if lower_moments is None else lower_moments
    a0_low, a0_half = low[0], moments["half"][0]
    for j in range(1, len(low)):
        lower = low[j] / a0_half
        upper = moments["half"][j] / a0_low
        normalized_zero = low[j] / a0_low
        normalized_half = moments["half"][j] / a0_half
        if not lower < normalized_zero:
            failures.append(f"j={j}: lower bound fails at lower y endpoint")
        if not normalized_half < upper:
            failures.append(f"j={j}: upper bound fails at y=1/2")
    return failures


def cap_stability(m: int, extra: int = 8) -> list[str]:
    """Compare minimal-cap moments with a deliberately overprovisioned jet."""
    minimum = endpoint_moments(m, required_series_cap(m))
    larger = endpoint_moments(m, required_series_cap(m) + extra)
    failures: list[str] = []
    for endpoint in ("zero", "half"):
        for j, (left, right) in enumerate(zip(minimum[endpoint], larger[endpoint], strict=True)):
            if not (left - right).contains(arb(0)):
                failures.append(f"{endpoint}: A_{2*j} balls from two caps are disjoint")
    return failures


def certify_root_structure(coefficients: list[arb]) -> dict[str, int]:
    """Use certified Acb root isolation for Q(t) and Q'(t), t=x^2."""
    tolerance = 2.0 ** -80
    polynomial_roots = acb_poly(coefficients).roots(tol=tolerance, maxprec=max(ctx.prec * 4, 512))
    derivative = [(j + 1) * coefficients[j + 1] for j in range(len(coefficients) - 1)]
    derivative_roots = acb_poly(derivative).roots(tol=tolerance, maxprec=max(ctx.prec * 4, 512))

    def positive_real_count(roots: Iterable[object]) -> int:
        return sum(root.imag.contains(arb(0)) and root.real > 0 for root in roots)

    return {
        "polynomial_degree": len(coefficients) - 1,
        "isolated_polynomial_roots": len(polynomial_roots),
        "positive_polynomial_roots": positive_real_count(polynomial_roots),
        "isolated_derivative_roots": len(derivative_roots),
        "positive_derivative_roots": positive_real_count(derivative_roots),
        "derivative_at_zero_negative": int(coefficients[1] < 0),
    }


def epsilon_enclosure_loss(m: int, epsilon: Fraction) -> int:
    """Count moment balls that fail to certify positivity after division by epsilon."""
    return sum(not value > 0 for value in moments_at_epsilon(m, epsilon))


def find_initial_root_bracket(coefficients: list[arb]) -> tuple[Fraction, Fraction]:
    """Find and refine the first integer +,- sign transition in x >= 0."""
    lower = Fraction(0)
    if not evaluate_even_polynomial(coefficients, arb(0)) > 0:
        raise ArithmeticError("constant term is not certified positive")
    for integer in range(1, 1001):
        upper = Fraction(integer)
        value = evaluate_even_polynomial(coefficients, arb(integer))
        if value < 0:
            return initial_positive_root(coefficients, lower, upper)
        if value > 0:
            lower = upper
        else:
            raise ArithmeticError(f"lost sign enclosure at x={integer}")
    raise ArithmeticError("no sign transition found below x=1000")


def _decimal(value: Fraction, digits: int = 40) -> str:
    with localcontext() as decimal_context:
        decimal_context.prec = digits
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=6)
    parser.add_argument("--precision", type=int, default=384, help="Arb precision in bits")
    parser.add_argument(
        "--epsilon",
        action="append",
        default=[],
        help="rational epsilon such as 0, 1/1000, 1/10, or 1/4 (repeatable)",
    )
    args = parser.parse_args()
    ctx.prec = args.precision
    epsilon_inputs = args.epsilon or ["0", "1/1000", "1/10", "1/4"]
    epsilons = [Fraction(item) for item in epsilon_inputs]
    print(f"backend=python-flint Arb precision_bits={ctx.prec}")
    print("implementation=independent equations H,endpoints,Phat; no certificate import")
    for epsilon in epsilons:
        if epsilon < 0 or epsilon > Fraction(1, 2):
            raise ValueError("each epsilon must lie in [0,1/2]")
        print(f"\nepsilon={epsilon}")
        for m in range(0, args.max_m + 1):
            moments = endpoint_moments(m)
            epsilon_moments = None if epsilon == 0 else moments_at_epsilon(m, epsilon)
            coefficients = cross_endpoint_coefficients(moments, m, epsilon_moments)
            structure = certify_root_structure(coefficients)
            lower, upper = find_initial_root_bracket(coefficients)
            print(
                f"m={m:2d} degree={4*m+2:2d} cap={required_series_cap(m):2d} "
                f"root=({_decimal(lower)},{_decimal(upper)}) "
                f"positive_Q_roots={structure['positive_polynomial_roots']} "
                f"positive_Qprime_roots={structure['positive_derivative_roots']} "
                f"cap_failures={len(cap_stability(m))} "
                f"normalization_failures={len(endpoint_normalization_failures(moments, epsilon_moments))} "
                f"epsilon_lost_moments={0 if epsilon == 0 else epsilon_enclosure_loss(m, epsilon)} "
                f"huge_x_finite={evaluate_even_polynomial(coefficients, arb('1e100')).is_finite()}"
            )


if __name__ == "__main__":
    main()
