"""Independent arithmetic identities and adverse controls for gen4 repricing."""
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "research/gen4-envelope-refinement"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pricing = load("tested_gen4_envelope_pricing", PACKAGE / "pricing.py")
verify = load("tested_gen4_envelope_verify", PACKAGE / "verify.py")


class Gen4EnvelopeRefinement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = pricing.source_inputs()
        cls.coarse = Q(724095528834925876331, 10**24)
        cls.envelope = pricing.envelope("disjoint")
        cls.candidate = pricing.build_candidate(
            cls.coarse, cls.envelope, 7, Q(1, 10**24),
            headline_grid=10**24, inputs=cls.inputs)

    def test_selected_baseline_reproduces_without_new_physical_claim(self):
        baseline = pricing.build_candidate(
            pricing.BASE_COARSE, pricing.envelope("legacy"), 3,
            Q(1, 10**12), inputs=self.inputs)
        self.assertEqual(baseline["kappa"], pricing.BASE_KAPPA)
        self.assertEqual(pricing.serial(baseline["assembly"]),
                         self.inputs["certificate"]["assembly"])

    def test_full_fallback_keeps_swaps_and_diagonal_scalings(self):
        # Independently sum the explicit list of allocations, not the
        # polynomial used by the production envelope constructor.
        dimension = 240
        additions = sum(6 for row in range(dimension)
                        for col in range(dimension) if row != col)
        swaps = sum(3 for _ in range(dimension))
        diagonal_pairs = sum(6 for _ in range(dimension-1))
        self.assertEqual(additions + swaps + diagonal_pairs, 346314)
        self.assertEqual(self.envelope["fallback_count"], 346314)
        for missing in (swaps, diagonal_pairs, 1):
            altered = dict(self.envelope)
            altered["fallback_count"] -= missing
            with self.assertRaisesRegex(ValueError, "Unproved envelope"):
                pricing.validate_envelope(altered)

    def test_gl_conditioning_against_complete_small_matrix_census(self):
        # GL_2(F_p) is small enough to enumerate every matrix. This tests
        # conditioning, not the nonzero-polynomial hypothesis of the proof.
        for prime in (3, 5, 7):
            with self.subTest(prime=prime):
                invertible = sum((a*d-b*c) % prime != 0
                    for a, b, c, d in product(range(prime), repeat=4))
                probability = Q(invertible, prime**4)
                expected = (1-Q(1, prime))*(1-Q(1, prime**2))
                self.assertEqual(probability, expected)
                self.assertGreater(probability, 1-Q(1, prime-1))

    def test_tighter_conditioning_is_monotone_and_keeps_positive_bad_mass(self):
        threshold = 2**80
        conditioning = lambda value: Q(value-1, value*(value-2))
        for value in (3, 5, 17, threshold):
            self.assertEqual(conditioning(value),
                             (Q(1, value)+Q(1, value-2))/2)
            self.assertLess(conditioning(value+1), conditioning(value))
        bad = 120**3*conditioning(threshold)
        self.assertEqual(bad, self.envelope["bad_fraction"])
        self.assertGreater(bad, 0)
        self.assertLess(bad, Q(2*120**3, threshold))
        for field, value in (("bad_fraction", Q(0)),
                             ("prime_lower_bound", 2**79)):
            altered = dict(self.envelope)
            altered[field] = value
            with self.assertRaisesRegex(ValueError, "Unproved envelope"):
                pricing.validate_envelope(altered)

    def test_disjoint_bound_for_endpoints_and_interior_probability(self):
        # tau=1/2 and square ranks make these power costs rational.
        # Divide out the shared m^(-tau); then g=sqrt(r), f=F.
        upper_bad = Q(1, 7)
        for rank, good in ((1, Q(1)), (4, Q(2)), (9, Q(3))):
            fallback = Q(12)
            pricing.validate_dominance(rank, int(fallback), Q(1, 2))
            bound = (1-upper_bad)*good+upper_bad*fallback
            for actual_bad in (Q(0), upper_bad/2, upper_bad):
                actual = (1-actual_bad)*good+actual_bad*fallback
                self.assertLessEqual(actual, bound)

    def test_cheap_fallback_reverses_the_required_probability_inequality(self):
        # A concrete counterexample to dropping the dominance hypothesis:
        # r=9,tau=1/2 gives good=3, whereas a two-child fallback costs 2.
        actual_at_zero = Q(3)
        incorrectly_substituted = Q(3, 4)*3+Q(1, 4)*2
        self.assertLess(incorrectly_substituted, actual_at_zero)
        with self.assertRaises(ValueError):
            pricing.validate_dominance(9, 2, Q(1, 2))

    def test_finite_closed_form_and_detached_step_control(self):
        chain, gaps = pricing.finite_chain(self.coarse, 8, self.inputs)
        for depth, ordinary in enumerate(chain):
            self.assertEqual(self.coarse-ordinary,
                self.coarse**depth*(self.coarse-pricing.BASE_LEAF))
        self.assertTrue(all(row["minimum_gap"] > 0 for row in gaps))
        with self.assertRaises(ValueError):
            pricing.validate_ordinary_saving(self.coarse, self.coarse)
        with self.assertRaises(ValueError):
            pricing.validate_ordinary_step(self.coarse, chain[0], chain[2])
        for depth in (0, float("inf"), True):
            with self.assertRaises(ValueError):
                pricing.finite_chain(self.coarse, depth, self.inputs)

    def test_strict_grid_floor_handles_exact_integer_boundary(self):
        # Ordinary floor would incorrectly admit the boundary in the first
        # case. The second case is already between adjacent grid points.
        self.assertEqual(pricing.strict_grid_below(Q(1, 2), 10), Q(2, 5))
        self.assertEqual(pricing.strict_grid_below(Q(51, 100), 10), Q(1, 2))
        for denominator in (0, -1, True):
            with self.assertRaises(ValueError):
                pricing.strict_grid_below(Q(1, 2), denominator)

    def test_selected_witness_and_all_strict_constraints(self):
        self.assertEqual(self.candidate["kappa"],
                         Q(361785796939503063587, 500000000000000000000000))
        constraints = self.candidate["assembly"]["strict_constraints"]
        self.assertEqual(len(constraints), 47)
        self.assertEqual(len(self.candidate["assembly"]["margins"]), 7)
        self.assertGreater(min(constraints.values()), 0)
        self.assertGreater(self.candidate["kappa"], pricing.BASE_KAPPA)
        ordinary = self.candidate["ordinary_bootstrap_chain"][-1]
        self.assertLess(self.candidate["kappa"], ordinary/(1+ordinary))
        self.assertLess(ordinary, self.coarse)

    def test_next_coarse_point_and_zero_backoff_rejected_by_real_entry_point(self):
        with self.assertRaisesRegex(ValueError, "Uncertified coarse saving"):
            pricing.build_candidate(self.coarse+Q(1, 10**24), self.envelope,
                                    7, Q(1, 10**24), inputs=self.inputs)
        with self.assertRaisesRegex(ValueError, "Positive exact eta"):
            pricing.build_candidate(self.coarse, self.envelope, 7, Q(0),
                                    inputs=self.inputs)

    def test_next_headline_rejected_by_retained_outer_constraints(self):
        candidate = self.candidate
        with self.assertRaises(AssertionError):
            pricing.engines()["outer"].assembly(
                candidate["ordinary_bootstrap_chain"][-1],
                Q(self.inputs["certificate"]["complex_coarse"]),
                self.inputs["bridge"], candidate["kappa"]+Q(1, 10**24),
                eta=Q(1, 10**24), beta=pricing.DEFAULT_BETA)

    def test_tampered_source_and_histogram_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"source.py"
            path.write_bytes(b"pinned source\n")
            expected = sha256(path.read_bytes()).hexdigest()
            path.write_bytes(b"changed source\n")
            with self.assertRaisesRegex(ValueError, "Source pin mismatch"):
                pricing.pinned_bytes(path, expected)
        profile = deepcopy(self.inputs["bit_profile"])
        profile["histogram"]["1"] += 1
        with self.assertRaisesRegex(ValueError, "Child count mismatch"):
            pricing.validate_profile(profile)

    def test_replay_validation_requires_every_stage_and_current_manifest(self):
        # A copied historical receipt is only a validation fixture; these
        # tests do not claim to have freshly executed the physical stages.
        historical = ROOT/"research/community-pr279-audit"
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            for name in ("verification.json", "certificate.json", "finite.json"):
                shutil.copyfile(historical/name, destination/name)
            receipt = json.loads((destination/"verification.json").read_text())
            inventory = {"manifest_sha256": receipt["manifest_sha256"]}
            verify.validate_replay(destination, inventory)
            altered = deepcopy(receipt)
            altered["fresh_stages"].remove("banks")
            (destination/"verification.json").write_text(json.dumps(altered))
            with self.assertRaisesRegex(ValueError, "Missing physical proof stage"):
                verify.validate_replay(destination, inventory)
            altered = deepcopy(receipt)
            altered["manifest_sha256"] = "0"*64
            (destination/"verification.json").write_text(json.dumps(altered))
            with self.assertRaisesRegex(ValueError, "Detached replay"):
                verify.validate_replay(destination, inventory)

    def test_optimized_interpreter_is_refused(self):
        result = subprocess.run([sys.executable, "-B", "-O", str(PACKAGE/"pricing.py")],
                                capture_output=True, text=True, timeout=30)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Assertions required", result.stdout+result.stderr)

    def test_certificate_bytes_are_canonical_lf_on_every_platform(self):
        value = {"z": "bound", "a": [1, 2]}
        expected = (json.dumps(value, indent=2, sort_keys=True)+"\n").encode("utf-8")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"certificate.json"
            verify.write_json(path, value)
            self.assertEqual(path.read_bytes(), expected)
            self.assertNotIn(b"\r", path.read_bytes())
        committed = (PACKAGE/"EXPECTED.json").read_bytes()
        self.assertEqual(committed, (json.dumps(json.loads(committed), indent=2,
                                               sort_keys=True)+"\n").encode("utf-8"))
        summary = json.loads((PACKAGE/"SUMMARY.json").read_bytes())
        self.assertEqual(summary["full_certificate_sha256"], sha256(committed).hexdigest())


if __name__ == "__main__":
    unittest.main()
