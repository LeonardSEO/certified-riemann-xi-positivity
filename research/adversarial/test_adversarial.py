#!/usr/bin/env python3
"""Regression tests for the independent higher-degree audit harness."""

from fractions import Fraction
import unittest

from flint import arb, ctx

import higher_degree_audit as audit


class HigherDegreeAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        ctx.prec = 320

    def test_required_cap_tracks_highest_xi_derivative(self) -> None:
        self.assertEqual(audit.required_series_cap(2), 13)
        self.assertEqual(audit.required_series_cap(6), 29)
        with self.assertRaisesRegex(ValueError, "series cap"):
            audit.endpoint_moments(2, cap=12)

    def test_two_derivative_indexing_paths_overlap(self) -> None:
        direct = audit.endpoint_moments(3, cap=audit.required_series_cap(3))
        formal = audit.endpoint_moments_formal(3, cap=audit.required_series_cap(3) + 5)
        for endpoint in ("zero", "half"):
            for left, right in zip(direct[endpoint], formal[endpoint], strict=True):
                self.assertTrue((left - right).contains(arb(0)))

    def test_degree_ten_normalization_and_root(self) -> None:
        moments = audit.endpoint_moments(2)
        coefficients = audit.cross_endpoint_coefficients(moments, 2)
        # Published degree-10 normalization: coefficient of x^2 is -B2/2!.
        b2 = moments["half"][1] / moments["zero"][0]
        self.assertTrue((coefficients[1] + b2 / 2).contains(arb(0)))
        self.assertTrue(
            audit.evaluate_even_polynomial(coefficients, arb(70362433) / 10_000_000) > 0
        )
        self.assertTrue(
            audit.evaluate_even_polynomial(coefficients, arb(70362434) / 10_000_000) < 0
        )
        bracket = audit.initial_positive_root(coefficients, Fraction(7), Fraction(8))
        self.assertLess(float(bracket[0]), 7.036244)
        self.assertGreater(float(bracket[1]), 7.036243)

    def test_endpoint_ratio_bounds_contain_endpoint_normalized_moments(self) -> None:
        moments = audit.endpoint_moments(4)
        failures = audit.endpoint_normalization_failures(moments)
        self.assertEqual(failures, [])

    def test_polynomial_evaluator_does_not_overflow_at_large_argument(self) -> None:
        moments = audit.endpoint_moments(4)
        coefficients = audit.cross_endpoint_coefficients(moments, 4)
        value = audit.evaluate_even_polynomial(coefficients, arb("1e100"))
        self.assertTrue(value.is_finite())

    def test_caps_agree_and_derivative_has_no_positive_root_through_m6(self) -> None:
        for m in range(7):
            comparison = audit.cap_stability(m, extra=7)
            self.assertEqual(comparison, [])
            moments = audit.endpoint_moments(m)
            coefficients = audit.cross_endpoint_coefficients(moments, m)
            structure = audit.certify_root_structure(coefficients)
            self.assertEqual(structure["positive_polynomial_roots"], 1)
            self.assertEqual(structure["positive_derivative_roots"], 0)
            self.assertEqual(structure["derivative_at_zero_negative"], 1)

    def test_epsilon_cancellation_loss_is_reported(self) -> None:
        old_precision = ctx.prec
        try:
            ctx.prec = 128
            loss = audit.epsilon_enclosure_loss(6, Fraction(1, 10**40))
            self.assertGreater(loss, 0)
        finally:
            ctx.prec = old_precision


if __name__ == "__main__":
    unittest.main()
