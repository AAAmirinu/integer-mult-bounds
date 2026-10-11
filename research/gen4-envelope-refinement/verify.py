#!/usr/bin/env python3
"""Reproduce the conditional gen4 envelope refinement and its source binding.

Default: replay the unchanged physical construction before refined arithmetic.
--arithmetic-only: reuse explicitly pinned historical finite evidence.
Prepared with substantial OpenAI Codex assistance; Apache-2.0.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from fractions import Fraction
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / "research/five-stage-gen4-banks"
REQUIRED = {"virtual", "raw", "bit", "scalar", "primes", "banks", "complex", "math", "finite"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_pricing():
    spec = importlib.util.spec_from_file_location("gen4_envelope_pricing", HERE / "pricing.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.write_bytes((json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def compact_summary(report, report_hash):
    """A separately labelled bounded index; the complete certificate is retained."""
    selected = report["selected"]
    cycles = []
    for cycle in report["cycles"]:
        admitted = [attempt for attempt in cycle["attempts"] if attempt["status"] == "PASS_EXACT_ARITHMETIC"]
        rejected = [attempt for attempt in cycle["attempts"] if attempt["status"] == "REJECTED"]
        cycles.append({"cycle": cycle["cycle"], "hypothesis": cycle["hypothesis"],
                       "predecessor": cycle["predecessor"],
                       "incumbent_before": cycle["incumbent_before"],
                       "incumbent_after": cycle["incumbent_after"], "improved": cycle["improved"],
                       "admitted_trials": len(admitted), "rejected_trials": len(rejected),
                       "best_trial_kappa": max((trial["kappa"] for trial in admitted), key=Fraction, default=None)})
    return {"schema": "gen4-envelope-summary/v1", "derived_from": "EXPECTED.json",
            "full_certificate_sha256": report_hash,
            "base_commit": "12a4934d15006e8c10f9b2264f13f8f341be802b",
            "baseline_kappa": report["baseline"]["kappa"],
            "selected_kappa": selected["kappa"], "selected_decimal": selected["kappa_decimal"],
            "gain_over_selected": selected["gain_over_selected"],
            "parameters": {key: str(value) for key, value in selected["parameters"].items()},
            "envelope": {key: str(value) for key, value in selected["envelope"].items()},
            "strict_constraints": len(selected["assembly"]["strict_constraints"]),
            "margins": len(selected["assembly"]["margins"]),
            "negative_controls": report["negative_controls"], "cycles": cycles,
            "scope": report["scope"],
            "evidence_scope": "This is a derived index of the full arithmetic certificate. Forge JSON assessments check captured field values, not the mathematical proof or external execution."}


def check_source_inventory(pricing):
    """A saved hash never admits edited code or an altered physical profile."""
    for relative, expected in pricing.SOURCE_PINS.items():
        path = ROOT / relative
        require(path.is_file() and not path.is_symlink(), "Missing source: " + relative)
        require(digest(path) == expected, "Changed source: " + relative)
    manifest = read_json(BASE / "MANIFEST.json")
    require(all(not p.is_symlink() for p in BASE.rglob("*")), "Symlink in inherited package")
    actual = {p.relative_to(BASE).as_posix(): digest(p)
              for p in BASE.rglob("*") if p.is_file() and p != BASE / "MANIFEST.json"}
    require(actual == manifest["files"], "Changed or unpinned inherited package file")
    return {"manifest_sha256": digest(BASE / "MANIFEST.json"), "files": len(actual)}


def validate_replay(directory, inventory):
    """Called only after this process launched and awaited the complete replay."""
    verification = read_json(directory / "verification.json")
    require(set(verification["fresh_stages"]) == REQUIRED, "Missing physical proof stage")
    require(verification["inputs_unchanged"] is True, "Replay changed its inputs")
    require(verification["manifest_sha256"] == inventory["manifest_sha256"], "Detached replay")
    require(verification["status"] == "PASS_IMMUTABLE_PARITY_FUSED_GEN4_FIVE_STAGE_BANKED_CONSTRUCTION",
            "Inherited replay did not pass")
    historical = read_json(ROOT / "research/community-pr279-audit/certificate.json")
    fresh = read_json(directory / "certificate.json")
    require(fresh == historical, "Fresh inherited certificate differs from pinned baseline")
    fresh_finite = read_json(directory / "finite.json")
    historical_finite = read_json(ROOT / "research/community-pr279-audit/finite.json")
    require(fresh_finite == historical_finite, "Fresh finite bill differs from pinned baseline")
    return verification


def main():
    require(not sys.flags.optimize, "Assertions must remain enabled; refusing -O")
    sys.dont_write_bytecode = True
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="New directory outside source packages")
    parser.add_argument("--arithmetic-only", action="store_true",
                        help="Recompute arithmetic from pinned historical evidence; no fresh physical replay")
    args = parser.parse_args()
    output = args.output.resolve()
    require(not output.exists(), "Output must be a new directory")
    require(not output.is_relative_to(BASE) and not output.is_relative_to(HERE),
            "Output must be outside the immutable source packages")
    pricing = load_pricing()
    inventory = check_source_inventory(pricing)
    output.mkdir(parents=True)
    start = time.monotonic()
    execution = {"schema": "gen4-envelope-execution/v1", "source_inventory": inventory,
                 "mode": "arithmetic-only" if args.arithmetic_only else "fresh-physical-replay",
                 "physical_replay_fresh": False, "status": "RUNNING"}
    try:
        if not args.arithmetic_only:
            subprocess.run([sys.executable, "-B", str(BASE / "verify.py"),
                            "--output", str(output / "baseline")], check=True, cwd=ROOT, timeout=3600,
                           env={**os.environ, "PYTHONUTF8": "1"})
            replay = validate_replay(output / "baseline", inventory)
            execution["physical_replay_fresh"] = True
            execution["inherited_replay_seconds"] = replay["seconds"]
        report = pricing.analyze()
        require(report == read_json(HERE / "EXPECTED.json"), "Refined arithmetic differs from expected certificate")
        require(check_source_inventory(pricing) == inventory, "Sources changed during verification")
        write_json(output / "certificate.json", report)
        summary = compact_summary(report, digest(output / "certificate.json"))
        require(summary == read_json(HERE / "SUMMARY.json"), "Bounded summary differs from full certificate")
        write_json(output / "summary.json", summary)
        execution.update(status="PASS", seconds=time.monotonic() - start,
                         certificate_sha256=digest(output / "certificate.json"))
        write_json(output / "execution.json", execution)
        print(json.dumps(execution, sort_keys=True), flush=True)
    except BaseException as exc:
        execution.update(status="FAIL", seconds=time.monotonic() - start,
                         error_type=type(exc).__name__, error=str(exc))
        write_json(output / "execution.json", execution)
        raise


if __name__ == "__main__":
    main()
