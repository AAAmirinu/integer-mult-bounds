#!/usr/bin/env python3
"""Independent small-matrix references and proof-bound regression checks."""

import importlib.util
from itertools import permutations
from math import gcd
from pathlib import Path
import random
import unittest


spec = importlib.util.spec_from_file_location("crt_verifier", Path(__file__).with_name("verify.py"))
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def leibniz(matrix):
    total, size = 0, len(matrix)
    for order in permutations(range(size)):
        inversions = sum(order[i] > order[j] for i in range(size) for j in range(i + 1, size))
        product = (-1) ** inversions
        for i, j in enumerate(order):
            product *= matrix[i][j]
        total += product
    return total


class MathematicalChecks(unittest.TestCase):
    def test_determinants_against_permutation_formula(self):
        rng = random.Random(83)
        for size in range(6):
            for trial in range(16):
                matrix = [[rng.randrange(-4, 5) for _ in range(size)] for _ in range(size)]
                with self.subTest(size=size, trial=trial):
                    exact = leibniz(matrix)
                    self.assertEqual(v.bareiss(matrix), exact)
                    self.assertEqual(v.elimination(matrix, 101)[0], exact % 101)

    def test_adjugate_against_literal_minor_expansion(self):
        # Includes nonsingular, row-swap, corank-one, and lower-rank cases.
        matrices = [[[0, 1], [1, 0]], [[0, 0], [0, 1]],
                    [[0, 0, 0], [1, 2, 3], [2, 4, 6]],
                    [[1, 2, 3], [2, 5, 4], [1, 0, 6]],
                    [[1, 2, 3], [2, 4, 6], [0, 1, 0]]]
        for matrix in matrices:
            with self.subTest(matrix=matrix):
                determinant, column = v.determinant_and_adjugate(matrix, 101)
                self.assertEqual(determinant, leibniz(matrix) % 101)
                expected = [(-1) ** col * leibniz([[value for j, value in enumerate(row) if j != col]
                                                 for row in matrix[1:]]) % 101
                            for col in range(len(matrix))]
                self.assertEqual(column, expected)
        # Exercise the singular branch with a nonzero adjugate column.
        self.assertEqual(v.determinant_and_adjugate([[0, 0], [0, 1]], 101), (0, [1, 0]))

    def test_trace_dual_basis_for_the_entire_radix_domain(self):
        for radix in v.RADICES:
            ell = v.prime_power(radix)
            step, degree = radix // ell, radix - radix // ell
            powers = [k for k in range(1, radix) if gcd(k, radix) == 1]

            def trace(exponent):
                coefficients = [0] * radix
                for power in powers:
                    coefficients[exponent * power % radix] += 1
                actual = v.reduce_integer(coefficients, radix)
                self.assertEqual(actual[1:], [0] * (degree - 1))
                return actual[0]

            traces = [trace(exponent) for exponent in range(radix)]
            for i in range(degree):
                omitted = i % step + (ell - 1) * step
                for monomial in range(degree):
                    with self.subTest(radix=radix, i=i, monomial=monomial):
                        self.assertEqual(traces[(monomial - i) % radix]
                                         - traces[(monomial - omitted) % radix],
                                         radix if monomial == i else 0)

    def test_crt_uniqueness_boundary_and_corrupt_residue(self):
        # M=2C is insufficient: +C and -C have the same residue.
        with self.assertRaisesRegex(ValueError, "uniqueness"):
            v.center([4], 8, 4)
        self.assertEqual(v.center([4, 5], 9, 4), [4, -4])
        value = v.crt_update([2, 3], 5, [2, 3], 7)
        self.assertEqual(v.center(value, 35, 4), [2, 3])
        # Altering one split-prime residue creates a large centered coefficient.
        bad = v.crt_update([2, 3], 5, [3, 3], 7)
        with self.assertRaisesRegex(ValueError, "coefficient bound"):
            v.center(bad, 35, 4)

    def test_lagrange_roundtrip_and_duplicate_points(self):
        self.assertEqual(v.interpolate([1, 2, 3], [6, 17, 34], 101), [1, 2, 3])
        with self.assertRaisesRegex(ValueError, "interpolation data"):
            v.interpolate([1, 1], [1, 2], 101)

    def test_source_pin_corruption_is_rejected(self):
        # Check the failure mode without changing any repository input.
        original = v.hashlib.sha256

        class WrongDigest:
            def hexdigest(self):
                return "0" * 64

        v.hashlib.sha256 = lambda _: WrongDigest()
        try:
            with self.assertRaisesRegex(ValueError, "source pin mismatch"):
                v.source_bindings()
        finally:
            v.hashlib.sha256 = original


if __name__ == "__main__":
    unittest.main(verbosity=2)
