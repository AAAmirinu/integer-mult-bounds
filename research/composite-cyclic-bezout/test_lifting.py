#!/usr/bin/env python3
"""Focused ring-arithmetic and fail-closed tests for modular lifting checks."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('lifting_check', HERE / 'verify_lifting.py')
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


class LiftingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = json.loads((HERE / 'LIFTING-SEEDS.json').read_text())

    def test_excluded_primes_and_composite_moduli_are_rejected(self):
        for case, prime in zip(self.document['cases'], (3, 43, 37)):
            with self.subTest(seed=case['order'], prime=prime):
                with self.assertRaisesRegex(ValueError, 'Seed denominator vanishes'):
                    check.finite_instance(case, prime, 1)
            prime = 3 if case['order'] == 3 else 2
            with self.subTest(seed=case['order'], prime=prime):
                with self.assertRaisesRegex(ValueError, 'Prime divides the seed radix'):
                    check.finite_instance(case, prime, 1)
        for prime in (1, 4, 25, True):
            with self.subTest(prime=prime), self.assertRaisesRegex(ValueError, 'not prime'):
                check.finite_instance(self.document['cases'][0], prime, 1)

    def test_lifting_exponent_must_be_a_positive_integer(self):
        for exponent in (0, -1, True, 1.0):
            with self.subTest(exponent=exponent):
                with self.assertRaisesRegex(ValueError, 'Exponent must be positive'):
                    check.finite_instance(self.document['cases'][0], 5, exponent)

    def test_modular_power_rejects_negative_exponents_and_allows_zero(self):
        mod = check.Modular(3, 7)
        modulus = [(1,), (3,)]
        self.assertEqual(mod.zpowmod([(0,), (1,)], 0, modulus), [(1,)])
        # z = -1/3 = 2 modulo 1+3z over F_7, so z^5 = 4.
        self.assertEqual(mod.zpowmod([(0,), (1,)], 5, modulus), [(4,)])
        for exponent in (-1, True, 0.5):
            with self.subTest(exponent=exponent):
                with self.assertRaisesRegex(ValueError, 'Power exponent must be nonnegative'):
                    mod.zpowmod([(0,), (1,)], exponent, modulus)

    def test_division_works_over_reducible_cyclotomic_coefficient_ring(self):
        # Phi_3 = (u-2)(u-4) mod 7: the coefficient ring has zero divisors.
        mod = check.Modular(3, 7)
        left, right = (5, 1), (3, 1)
        self.assertNotEqual(left, (0,))
        self.assertNotEqual(right, (0,))
        self.assertEqual(mod.mul(left, right), (0,))
        # Divide (6+3u)+(5+3u)z+4z^2 by 1+3z using only scalar inversion.
        quotient, remainder = mod.zdiv([(6, 3), (5, 3), (4,)], [(1,), (3,)])
        self.assertEqual(quotient, [(2, 1), (6,)])
        self.assertEqual(remainder, [(4, 2)])
        with self.assertRaisesRegex(ValueError, 'Nonunit scalar leading coefficient'):
            mod.zdiv([(1,), (1,)], [(1,), left])
        self.assertEqual(check.finite_instance(self.document['cases'][1], 7, 1)['radix'], 21)

    def test_reciprocal_preserves_fixed_degree_before_reduction(self):
        # At s=3, p=2, r=6, reversal has three trailing zeros after reduction.
        mod = check.Modular(3, 2)
        reduced = check.literal_reduction(mod, 6)
        star = check.literal_reduction(mod, 6, reciprocal=True)
        self.assertEqual(reduced, [(0,), (0,), (0,), (1,), (0, 1), (1,)])
        self.assertEqual(star, [(1,), (1, 1), (1,), (0,), (0,), (0,)])
        self.assertEqual(check.base.ztrim(star), [(1,), (1, 1), (1,)])
        self.assertEqual(check.finite_instance(self.document['cases'][1], 2, 1)['radix'], 6)

    def test_mutated_obligations_reach_the_positive_validation_paths(self):
        mod = check.Modular(2, 5)
        f, star = [(2,), (1,)], [(1,), (2,)]
        reduced = [(0,)] * 8 + f
        reduced_star = star + [(0,)] * 8
        check.check_reductions(f, star, reduced, reduced_star, 8)
        with self.assertRaisesRegex(ValueError, 'Tail-product shift identity failed'):
            check.check_reductions(f, star, f, reduced_star, 8)
        with self.assertRaisesRegex(ValueError, 'Reciprocal reduction identity failed'):
            check.check_reductions(f, star, reduced, [(0,)] * 8 + star, 8)
        check.check_modular_identity(mod, f, star, [(2,)], [(4,)], 3)
        with self.assertRaisesRegex(ValueError, 'Modular Bezout identity failed'):
            check.check_modular_identity(mod, [(2,), (2,)], star, [(2,)], [(4,)], 3)

    def test_cli_rejects_corrupted_seed_even_under_optimization(self):
        document = deepcopy(self.document)
        a = document['cases'][0]['a'][0]
        a[0] = str(int(a[0]) + 1)
        with tempfile.TemporaryDirectory(prefix='lifting-bezout-test-') as directory:
            path = Path(directory) / 'corrupt.json'
            path.write_text(json.dumps(document))
            for flags in (['-B', '-I'], ['-B', '-I', '-O']):
                with self.subTest(flags=flags):
                    result = subprocess.run([sys.executable, *flags, str(HERE / 'verify_lifting.py'),
                                             '--seeds', str(path)], text=True, capture_output=True)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn('Bezout identity failed', result.stderr)
                    self.assertNotIn('PASS:', result.stdout)

    def test_public_receipt_is_recomputed_under_optimization(self):
        result = subprocess.run([sys.executable, '-B', '-I', '-O', str(HERE / 'verify_lifting.py'),
                                 '--check', str(HERE / 'LIFTING-EXPECTED.json')],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('PASS: 3 exact seeds, 54 modular lifts, 3 excluded-prime witnesses, 173 controls',
                      result.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
