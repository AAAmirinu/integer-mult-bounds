"""Differential rank/RREF tests and source-bound real-frame coverage."""
from copy import deepcopy
from fractions import Fraction
import gzip
import json
from pathlib import Path
import random
import tempfile
import unittest

from common import ROOT, SOURCE, reference_functions, sha, verify_source
from exact_rows import key_of, rank_q

REFERENCE = reference_functions()


class ExactRowsTests(unittest.TestCase):
    def compare(self, matrix):
        before = deepcopy(matrix)
        self.assertEqual(rank_q(matrix), REFERENCE.rank_q(matrix))
        self.assertEqual(key_of(matrix), REFERENCE.key_of(matrix))
        self.assertEqual(matrix, before)

    def test_edge_cases(self):
        for matrix in ([], [[]], [[], []], [[0]], [[1]], [[-1]], [[0, 1], [1, 0]],
                       [[1, 2], [2, 4]], [[0, 0, 0], [0, 0, 0]],
                       [[10**80+1, 10**80], [10**80+2, 10**80+1]],
                       [[Fraction(1, 1000000007), Fraction(1, 1000000009)], [1, 1]]):
            with self.subTest(matrix=matrix):
                self.compare(matrix)

    def test_seeded_rational_and_singular_matrices(self):
        rng = random.Random(364358)
        for i in range(600):
            m, n = rng.randrange(1, 22), rng.randrange(1, 22)
            matrix = [[rng.randrange(-9, 10) if rng.random() < .6 else 0 for _ in range(n)] for _ in range(m)]
            if m > 1 and rng.random() < .5:
                matrix[-1] = [3*x for x in matrix[0]]
            if rng.random() < .3:
                matrix = [[Fraction(x, rng.randrange(1, 10)) for x in row] for row in matrix]
            with self.subTest(case=i):
                self.compare(matrix)

    def test_row_space_invariance(self):
        rng = random.Random(358364)
        for _ in range(150):
            matrix = [[rng.randrange(-20, 21) for _ in range(12)] for _ in range(8)]
            changed = deepcopy(matrix)
            rng.shuffle(changed)
            changed[0] = [Fraction(-7, 13)*x for x in changed[0]]
            changed[1] = [x+9*y for x,y in zip(changed[1],changed[0])]
            changed += [[0]*12, list(changed[2])]
            self.assertEqual(key_of(matrix), key_of(changed))
            self.assertEqual(rank_q(matrix), rank_q(changed))

    def test_generators_and_ragged_rejection(self):
        matrix = [[0, 2, 4], [1, 3, 5]]
        self.assertEqual(rank_q((iter(row) for row in matrix)), 2)
        self.assertEqual(key_of((iter(row) for row in matrix)), key_of(matrix))
        for function in (rank_q, key_of):
            with self.assertRaises(ValueError):
                function([[1, 2], [3]])

    def test_pivot_cancellation_and_rejection_cases(self):
        for matrix, expected in (([[1,2],[2,4]],1), ([[1,2],[2,5]],2),
                                 ([[0,1,2],[0,2,4],[0,0,0]],1),
                                 ([[0,1,2],[0,2,4],[1,0,0]],2)):
            self.assertEqual(rank_q(matrix), expected)
            self.compare(matrix)

    def test_all_distinct_real_frame_matrices(self):
        fixture = ROOT/SOURCE['fixture']['path']
        self.assertEqual(sha(fixture), SOURCE['fixture']['sha256'])
        frames = json.loads(gzip.decompress(fixture.read_bytes()))
        self.assertEqual(len(frames), SOURCE['fixture']['unique_frame_pairs'])
        ranks, keys = set(), set()
        for frame in frames:
            B, A = frame['B'], frame['A']
            d = len(B); sums = [sum(row) for row in B]
            gram = [[9*sum(x*y for x,y in zip(B[i],B[j]))-sums[i]*sums[j]
                     for j in range(d)] for i in range(d)]
            for matrix in (B,A,gram):
                signature = tuple(map(tuple,matrix))
                if signature not in ranks:
                    self.assertEqual(rank_q(matrix), REFERENCE.rank_q(matrix))
                    ranks.add(signature)
            signature = tuple(map(tuple,B))
            if signature not in keys:
                self.assertEqual(key_of(B), REFERENCE.key_of(B))
                keys.add(signature)
        self.assertEqual(len(ranks), SOURCE['fixture']['rank_matrices'])
        self.assertEqual(len(keys), SOURCE['fixture']['key_matrices'])

    def test_incomplete_or_symlinked_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary)
            with self.assertRaises(ValueError):
                verify_source(path)
            (path/'reference').symlink_to(ROOT/'reference/stagelib.py')
            with self.assertRaises(ValueError):
                verify_source(path)


if __name__ == '__main__':
    unittest.main()
