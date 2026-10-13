#!/usr/bin/env python3
"""Check exact equivalence and optionally benchmark the isolated log replacement.

Python 3.10+, standard library only. No repository files are overwritten.
Checks remain active under -O. No supplier or complete assembly replay is claimed.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import random
import statistics
import sys
import time
import types

HERE = Path(__file__).resolve().parent
REFERENCE_BLOB = "14a90fa0e788217856f070382c9e61bd7c603c61"
REFERENCE_SHA256 = "aee70c242a2f1d225528fabe2002e1564d1dc884797c07d28a831c7878ee9098"
SEED = 89


class VerificationError(RuntimeError):
    pass


def check(condition, message):
    if not condition:
        raise VerificationError(message)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    check(spec is not None and spec.loader is not None, "module loader unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_check(reference_path):
    data = reference_path.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    check(blob == REFERENCE_BLOB, "reference git blob mismatch")
    check(hashlib.sha256(data).hexdigest() == REFERENCE_SHA256, "reference SHA256 mismatch")


def inventory_check():
    manifest_path = HERE / "MANIFEST.json"
    check(manifest_path.is_file(), "missing MANIFEST.json")
    manifest = json.loads(manifest_path.read_text())
    actual = {str(p.relative_to(HERE)) for p in HERE.rglob("*")
              if p.is_file() and "__pycache__" not in p.parts and p.name != "MANIFEST.json"}
    check(actual == set(manifest), "package file inventory mismatch")
    for name, wanted in manifest.items():
        check(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == wanted,
              "package hash mismatch: " + name)


def update_digest(digest, value):
    """Canonical integer/fraction encoding without decimal digit-limit changes."""
    value = Q(value)
    for n in (value.numerator, value.denominator):
        digest.update(b"-" if n < 0 else b"+")
        data = abs(n).to_bytes(max(1, (abs(n).bit_length() + 7) // 8), "big")
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)


def equal_case(ref, fast, name, x, digest):
    wanted = getattr(ref, name)(x)
    actual = getattr(fast, name)(x)
    check(actual == wanted, name + " exact endpoint mismatch")
    check(wanted[0] <= wanted[1], "reversed interval")
    update_digest(digest, x)
    for endpoint in actual:
        update_digest(digest, endpoint)


def priced(module, profile, saving, surcharge):
    m, W, entries = profile["m"], profile["W"], profile["entries"]
    lo, hi = module.moment(m, W, entries, saving)
    if surcharge:
        count = 32 * m * m * sum(n for _, n in entries)
        fl, fu = module.moment(m, W, [(1, count)], saving)
        lo += fl / 10**16
        hi += fu / 10**16
    return lo, hi


def moment_suite(module, fixture):
    out = []
    for case in fixture["cases"]:
        profile = fixture["profiles"][case["profile"]]
        lower = Q(case["lower"])
        for saving in (lower, lower + Q(fixture["next_grid_step"])):
            out.append(priced(module, profile, saving, case["surcharge"]))
    return out


def rejection_check(call, exc_type, text):
    try:
        call()
    except exc_type as exc:
        check(str(exc) == text, "unexpected rejection reason: " + str(exc))
    else:
        raise VerificationError("missing rejection: " + text)


def mutation_checks(ref, optimized_source):
    # Mutate the evaluated implementation, not the expected answers.
    changes = {
        "drop_last_series_term": ("TERMS = 80", "TERMS = 79"),
        "erase_remainder_bound": ("return lower, lower + tail", "return lower, lower"),
        "wrong_homogeneous_denominator": ("denominator_power = b_power // b", "denominator_power = b_power"),
        "wrong_horner_multiplier": ("numerator = a2 * numerator + coefficient * b_power", "numerator = b2 * numerator + coefficient * b_power"),
        "freeze_denominator_power": ("b_power *= b2", "b_power *= 1"),
        "damage_one_series_coefficient": ("_COEFFICIENTS = tuple(_COMMON // odd for odd in _ODDS)", "_COEFFICIENTS = tuple(_COMMON // odd + (odd == 75) for odd in _ODDS)"),
        "wrong_tail_exponent": ("2 * a**161", "2 * a**159"),
        "lossy_float_input_roundtrip": ("x = Fraction(x)", "x = Fraction(float(x))"),
    }
    probes = (Q(2), Q(7, 5), Q(9, 5), Q(1) + Q(1, 2**80))
    rejected = []
    for name, (old, new) in changes.items():
        check(optimized_source.count(old) == 1, "mutation target missing or ambiguous: " + name)
        module = types.ModuleType("mutant_" + name)
        exec(compile(optimized_source.replace(old, new), name, "exec"), module.__dict__)
        # Every listed mutant must return a numerically wrong interval on a probe;
        # syntax/import/runtime exceptions are NOT credited as rejection evidence.
        mismatch = any(module.log_unit(x) != ref.log_unit(x) for x in probes)
        check(mismatch, "mutation escaped exact comparison: " + name)
        rejected.append(name)
    return rejected


def verify(ref, fast, optimized, fixture):
    digest = hashlib.sha256()
    groups = {}
    unit = sorted({Q(n, d) for d in range(1, 65) for n in range(d, 2 * d + 1)})
    for x in unit:
        equal_case(ref, fast, "log_unit", x, digest)
    groups["unit_grid_denominator_at_most_64"] = len(unit)

    rng = random.Random(SEED)
    difficult = []
    for bits in (17, 53, 80, 127, 256):
        tiny = Q(1, 2**bits)
        difficult.extend((1 + tiny, 2 - tiny))
        for _ in range(4):
            d = rng.getrandbits(bits) | 1
            difficult.append(1 + Q(rng.randrange(d + 1), d))
    for x in difficult:
        equal_case(ref, fast, "log_unit", x, digest)
    groups["unit_adversarial_and_seeded_large_rationals"] = len(difficult)

    count = 0
    for m in range(2, 97):
        for t in range(1, m):
            equal_case(ref, fast, "log_bounds", Q(m, t), digest)
            count += 1
    groups["range_reduction_all_children_m_2_through_96"] = count

    boundaries = []
    for k in (1, 2, 3, 8, 16, 32, 64):
        p = Q(2**k)
        boundaries.extend((p, p - Q(1, 2**80), p + Q(1, 2**80)))
    for x in boundaries:
        equal_case(ref, fast, "log_bounds", x, digest)
    groups["range_reduction_power_of_two_boundaries"] = len(boundaries)

    for profile in fixture["profiles"].values():
        m, W, H = profile["m"], profile["W"], profile["entries"]
        check(m * W - sum(t * n for t, n in H) == profile["deficit"], "fixture rank mass mismatch")
        check(m * m > 2 * max(t for t, _ in H)**2, "fixture halving inequality mismatch")
    wanted, actual = moment_suite(ref, fixture), moment_suite(fast, fixture)
    check(actual == wanted, "complete charged moment suite differs")
    moments = []
    for index, ((lo, hi), case) in enumerate(zip(actual, [c for c in fixture["cases"] for _ in range(2)])):
        accept = index % 2 == 0
        check(hi < 1 if accept else lo > 1, "adjacent endpoint decision differs: " + case["name"])
        for v in (lo, hi):
            update_digest(digest, v)
        moments.append({"name": case["name"], "accept": accept, "surcharge": case["surcharge"],
                        "interval_minus_one": [str(lo - 1), str(hi - 1)]})
    groups["charged_moment_endpoints"] = len(moments)

    # Controls for the actual physical pricing distinction, not merely agreement.
    bit = fixture["cases"][2]
    bp = fixture["profiles"][bit["profile"]]
    bit_next = Q(bit["lower"]) + Q(fixture["next_grid_step"])
    native = fixture["cases"][0]
    cp = fixture["profiles"][native["profile"]]
    for module in (ref, fast):
        check(priced(module, bp, bit_next, False)[1] < 1, "omitted-bit-surcharge control not reproduced")
        check(priced(module, cp, Q(native["lower"]), True)[0] > 1, "conservative-complex-surcharge control not reproduced")
        for case in fixture["cases"]:
            profile = fixture["profiles"][case["profile"]]
            damaged = dict(profile, entries=[[t, n + (t == 1)] for t, n in profile["entries"]])
            check(priced(module, damaged, Q(case["lower"]), case["surcharge"])[0] > 1,
                  "extra-child mutation was not rejected")
    groups["pricing_negative_controls_per_engine"] = 5

    domain_count = 0
    for module in (ref, fast):
        for x in (Q(-1), Q(0), Q(1, 2), Q(2001, 1000)):
            rejection_check(lambda: module.log_unit(x), ValueError, "logarithm range")
            domain_count += 1
        for x in (Q(-1, 100), Q(1), Q(2)):
            rejection_check(lambda: module.exp_bounds(x), ValueError, "exponential range")
            domain_count += 1
        for entry in ((0, 1), (73, 1), (74, 1), (1, 0), (1, -1)):
            rejection_check(lambda: module.moment(73, 7168, [entry], Q(native["lower"])), ValueError, "improper child")
            domain_count += 1
    groups["inherited_domain_rejections_both_engines"] = domain_count
    for x in (1.5, "3/2", None):
        rejection_check(lambda: optimized.log_unit(x), TypeError, "an exact Fraction or integer is required")
    check(optimized.log_unit(1) == ref.log_unit(Q(1)), "integer endpoint 1")
    check(optimized.log_unit(2) == ref.log_unit(Q(2)), "integer endpoint 2")
    groups["new_exact_input_type_rejections"] = 3
    groups["exact_integer_endpoints"] = 2

    mutants = mutation_checks(ref, (HERE / "log_horner.py").read_text())
    groups["implementation_mutations_detected"] = len(mutants)
    return {"groups": groups, "exact_comparison_digest_sha256": digest.hexdigest(),
            "moments": moments, "mutations_detected": mutants}


def benchmark(ref, fast, fixture, repeats):
    # Same deterministic inputs and same original outer code. No result caches.
    # Match the reference's strict x > 2 reduction, including log(2), which
    # it evaluates for every ratio. Powers of two therefore reduce to 2.
    reduced = {Q(2)}
    for profile in fixture["profiles"].values():
        for t, _ in profile["entries"]:
            x = Q(profile["m"], t)
            while x > 2:
                x /= 2
            reduced.add(x)
    unit_inputs = sorted(reduced)
    check(all(1 <= x <= 2 for x in unit_inputs), "benchmark reduction range")
    tasks = {
        "log_unit_selected_ratios": lambda m: [m.log_unit(x) for _ in range(20) for x in unit_inputs],
        "complex626_native_endpoint_pair": lambda m: [priced(m, fixture["profiles"]["complex626"], z, False)
            for z in (Q(fixture["cases"][0]["lower"]), Q(fixture["cases"][0]["lower"]) + Q(fixture["next_grid_step"]))],
        "selected_three_charged_endpoint_pairs": lambda m: moment_suite(m, fixture),
    }
    result = {}
    for name, task in tasks.items():
        check(task(ref) == task(fast), "benchmark warmup outputs differ")
        samples = {"reference": [], "optimized": []}
        for iteration in range(repeats):
            order = (("reference", ref), ("optimized", fast))
            if iteration % 2:
                order = tuple(reversed(order))
            outputs = []
            for label, module in order:
                start = time.perf_counter_ns()
                output = task(module)
                elapsed = time.perf_counter_ns() - start
                samples[label].append(elapsed / 10**9)
                outputs.append(output)
            check(outputs[0] == outputs[1], "timed outputs differ")
        medians = {label: statistics.median(values) for label, values in samples.items()}
        result[name] = {"seconds": samples, "median_seconds": medians,
                        "speedup": medians["reference"] / medians["optimized"]}
    return {"repeats": repeats, "timer": "perf_counter_ns", "alternating_order": True,
            "input_dependent_caching": False, "unit_batch_repetitions": 20,
            "unit_inputs": [str(x) for x in unit_inputs],
            "workloads": result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark", action="store_true")
    parser.add_argument("--repeats", type=int, default=7)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    check(args.repeats >= 3, "at least three benchmark repetitions required")
    if args.output is not None:
        check(not args.output.exists(), "output already exists")
        check(HERE not in args.output.resolve().parents, "output must be outside immutable package")
    inventory_check()
    reference_path = HERE / "reference" / "base_two_moment.py"
    source_check(reference_path)
    ref = load("reference_engine", reference_path)
    fast = load("optimized_engine", reference_path)
    optimized = load("log_horner", HERE / "log_horner.py")
    # This private experiment rebinds just one function. No shared import or
    # repository file is modified, and all other reference code stays identical.
    fast.log_unit = optimized.log_unit
    fixture = json.loads((HERE / "fixtures.json").read_text())
    start = time.perf_counter()
    report = {"status": "PASS_EXACT_LOG_HORNER", "seed": SEED,
              "base_commit": fixture["base_commit"], "reference_git_blob_sha1": REFERENCE_BLOB,
              "executed_input_sha256": {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                                        for name in ("verify.py", "log_horner.py", "fixtures.json", "reference/base_two_moment.py")},
              "environment": {"python": sys.version, "implementation": platform.python_implementation(),
                              "platform": platform.platform(), "machine": platform.machine(),
                              "optimization_level": sys.flags.optimize, "cpu_count": os.cpu_count()},
              "verification": verify(ref, fast, optimized, fixture)}
    report["verification_seconds"] = time.perf_counter() - start
    if args.benchmark:
        report["benchmark"] = benchmark(ref, fast, fixture, args.repeats)
    report["scope"] = "Exact arithmetic-kernel equivalence and extracted profile pricing only; no full supplier, assembly, repository, CI, or Lean replay. No new kappa."
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(encoded)
    print(report["status"])
    print(json.dumps(report["verification"]["groups"], sort_keys=True))
    if args.benchmark:
        for name, row in report["benchmark"]["workloads"].items():
            print(name, "median speedup", format(row["speedup"], ".3f"))
    if args.output:
        print("receipt:", args.output)


if __name__ == "__main__":
    try:
        main()
    except (VerificationError, ValueError, TypeError, OSError, KeyError) as exc:
        print("FAIL:", str(exc), file=sys.stderr)
        sys.exit(1)
