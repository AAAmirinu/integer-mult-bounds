#!/usr/bin/env python3
"""Focused mathematical and fail-closed tests for the certificate checker."""
from copy import deepcopy
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('composite_check', HERE / 'verify.py')
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


class CertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = json.loads((HERE / 'CERTIFICATE.json').read_text())
        cls.receipt = json.loads((HERE / 'EXPECTED.json').read_text())

    def test_cyclotomic_moduli_against_explicit_formulas(self):
        known = {
            6: (1, -1, 1), 10: (1, -1, 1, -1, 1),
            12: (1, 0, -1, 0, 1), 14: (1, -1, 1, -1, 1, -1, 1),
            15: (1, -1, 0, 1, -1, 1, 0, -1, 1),
            18: (1, 0, 0, -1, 0, 0, 1),
        }
        for order, coefficients in known.items():
            with self.subTest(order=order):
                self.assertEqual(check.cyclotomic(order), coefficients)

    def test_conjugation_and_primitive_root_relation(self):
        ring = check.Ring(6)
        self.assertEqual(ring.conjugate(ring.u), (1, -1))
        self.assertEqual(ring.mul(ring.u, ring.conjugate(ring.u)), (1,))
        for order in check.ORDERS:
            ring = check.Ring(order)
            for power in ring.powers:
                self.assertEqual(ring.conjugate(ring.conjugate(power)), power)
                self.assertEqual(ring.mul(power, ring.conjugate(power)), (1,))

    def test_constant_and_wrapped_polynomial_division(self):
        # (x^4 + 1)/(x^2 + 1) = x^2 - 1 + 2/(x^2 + 1).
        self.assertEqual(check.monic_divide((1, 0, 0, 0, 1), (1, 0, 1)),
                         ((-1, 0, 1), (2,)))
        self.assertEqual(check.monic_divide((0,), (1,)), ((0,), (0,)))
        with self.assertRaises(ValueError):
            check.monic_divide((1, 2), (2,))

    def test_alternative_valid_scaled_certificate_is_accepted(self):
        # Admission checks the identity, not equality to generator bytes.
        case = deepcopy(self.document['cases'][0])
        expected = check.check_case(case)
        case['denominator'] = str(7 * int(case['denominator']))
        for name in ('a', 'b'):
            case[name] = [[str(7 * int(c)) for c in row] for row in case[name]]
        actual = check.check_case(case)
        self.assertEqual(actual['circle_lower_bound'], expected['circle_lower_bound'])
        self.assertEqual(actual['inverse_infinity_upper_bound'], expected['inverse_infinity_upper_bound'])

    def test_outward_dyadic_bounds_and_fourier_constant(self):
        for row in self.receipt['cases']:
            delta = Fraction(row['circle_lower_bound'])
            bound = Fraction(row['inverse_infinity_upper_bound'])
            circle = Fraction(2) ** row['circle_lower_bound_dyadic_exponent']
            inverse = Fraction(2) ** row['inverse_infinity_upper_bound_dyadic_exponent']
            self.assertLessEqual(circle, delta)
            self.assertLess(delta, 2 * circle)
            self.assertLessEqual(bound, inverse)
            self.assertGreater(bound, inverse / 2)
            r = row['order']
            self.assertEqual(bound, 1 / delta + Fraction(2 * (r - 1) * (2 ** r - 1), r) / delta ** 2)

    def test_certificate_cli_rejects_corruption_even_under_optimization(self):
        document = deepcopy(self.document)
        a = document['cases'][0]['a'][0]
        a[0] = str(int(a[0]) + 1)
        with tempfile.TemporaryDirectory(prefix='composite-bezout-test-') as directory:
            path = Path(directory) / 'corrupt.json'
            path.write_text(json.dumps(document))
            for flags in (['-B', '-I'], ['-B', '-I', '-O']):
                result = subprocess.run([sys.executable, *flags, str(HERE / 'verify.py'),
                                         '--certificate', str(path)], text=True, capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Bezout identity failed', result.stderr)
                self.assertNotIn('PASS:', result.stdout)

    def test_complete_domain_and_integer_encoding_fail_closed(self):
        bad = deepcopy(self.document)
        bad['cases'][0]['order'] = True
        with self.assertRaises(ValueError):
            check.verify(bad)
        for value in ('01', '-0', 1.0, True, '1/2'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                check.integer(value)

    def test_public_receipt_is_recomputed(self):
        result = subprocess.run([sys.executable, '-B', '-I', '-O', str(HERE / 'verify.py'),
                                 '--check', str(HERE / 'EXPECTED.json')], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('PASS: 6 identities, 30 primitive embeddings, 39 negative controls', result.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
