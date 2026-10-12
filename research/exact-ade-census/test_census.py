"""Regression controls for the exceptional-root census (standard library only)."""
import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location("census", Path(__file__).with_name("census.py"))
census = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(census)


class CensusTests(unittest.TestCase):
    def test_e6_is_not_the_orthogonal_pair_complement(self):
        # Catches the archived E6() predicate: A1+A1 gives D6, not E6.
        self.assertEqual(len(census.exceptional_lines("E6")), 36)
        self.assertEqual(len(census.exceptional_lines("D6-control")), 30)

    def test_cartan_types_and_binary_decoder_ranks(self):
        # Cartan determinants and trivalent arm lengths distinguish E6 from D6.
        fixtures = {
            "E6": (36, 6, 3, [1, 2, 2], 7, "7/6"),
            "E7": (63, 7, 2, [1, 2, 3], 7, "7/9"),
            "E8": (120, 8, 1, [1, 2, 4], 9, "3/5"),
            "D6-control": (30, 6, 4, [1, 1, 3], 5, "1"),
        }
        for name, expected in fixtures.items():
            with self.subTest(name=name):
                row = census.analyze(census.exceptional_lines(name))
                actual = tuple(row[k] for k in (
                    "lines", "dimension", "cartan_determinant", "dynkin_arms",
                    "binary_decoder_rank", "full_rank_totals_proxy"))
                self.assertEqual(actual, expected)

    def test_broken_root_sets_are_rejected(self):
        roots = census.exceptional_lines("E6")
        for bad in (roots[:-1], roots + [roots[0]], [(0,) * 8] + roots[1:]):
            with self.subTest(size=len(bad)):
                with self.assertRaises(ValueError):
                    census.analyze(bad)

    def test_exact_rank_distinguishes_characteristic_two(self):
        triangle = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]
        self.assertEqual(census.rational_rank(triangle), 3)
        self.assertEqual(census.binary_rank(triangle), 2)


if __name__ == "__main__":
    unittest.main()
