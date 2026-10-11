#!/usr/bin/env python3
"""Format obstructions: run every exact check behind PROOF.md, offline, from pinned inputs.

usage: python3 -B research/format-obstructions/verify.py [--output DIR] [--jobs N]

Requires Python 3.11+ (tested: 3.12) and the pinned packages of requirements.txt (python-sat for the CaDiCaL checks,
networkx, mpmath, numpy). Assertions must stay enabled (-O is refused). No network. The independent stages run in
a process pool; the result facts are compared with expected.json (every number below is pinned there).

Stages (see README.md for what each one establishes):
  certificates  gx.check1 (Sussman's reference checker, vendored unchanged) on three gcert/1 programs, then Thm A (taint
                replay, every gate), Cor A1, Thm B data (neighbourhood rank), Thm C (copy lower bound vs. paid);
                negative controls on the small program.
  toy_p3        the one read-discipline gain (cst 18 -> 16) and its exhaustive optimum; control.
  pivots        Theorem P (cross-Gram forced to zero), the copy count and the contamination scan of PROOF.md section 7.
  mutable_425   PR #425's mutable-basis word: Thm A/B/C replays, exact scalar identity, Theorem S conversion; controls.
  pricing       the pinned pricer on the p = 10 bit histogram (pivot-free variants, copy and descent units).
  families      neighbourhood ranks and copy bounds for the port families, clique numbers, the explicit 20-clique.
  e8_labels     SAT: uniqueness of the h = 9 labelling, k = 2 planes UNSAT at r = 16, 17; calibrations and controls.
"""
import argparse
import hashlib
import importlib
import importlib.metadata as md
import json
import multiprocessing as mp
import os
import sys
import tempfile
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

if sys.flags.optimize:
    raise SystemExit("Assertions must remain enabled: run without -O")
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "checks"))
sys.path.insert(0, str(ROOT / "gx"))

PINNED_PACKAGES = {"python-sat": "1.9.dev15", "networkx": "3.7", "mpmath": "1.3.0", "numpy": "2.3.5"}
P10 = str(ROOT / "inputs" / "gcert1-p10-anneal-mw-flow.json.gz")
P11 = str(ROOT / "inputs" / "gcert1-p11-pr193.json.gz")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def package_files():
    return sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and "__pycache__" not in p.parts)


def integrity():
    pins = json.loads((ROOT / "SOURCE.json").read_text())["files"]
    for rel, want in pins.items():
        assert sha(ROOT / rel) == want, "pinned input changed: " + rel
    return len(pins)


def tasks():
    """(id, module, function, args). Long tasks first."""
    t = [
        ("cert_p11", "certs", "stage", ("p11",)),
        ("cert_p10", "certs", "stage", ("p10",)),
        ("overlap_p10", "pivots", "overlap_scan", (P10,)),
        ("copy_count_p10", "pivots", "copy_count", (P10,)),
        ("omega_cx_7", "families", "incap_omega", (7, "cx")),
        ("thmP_p11", "pivots", "thm_P", (P11,)),
        ("thmP_p10", "pivots", "thm_P", (P10,)),
        ("cert_p3", "certs", "stage", ("p3",)),
        ("toy_p3", "toy", "run", ()),
        ("mutable_425", "mutable425", "run", ()),
        ("pricing", "pricing", "run", ()),
        ("e8_bitdual", "families", "e8_bitdual", ()),
        ("p10_clique", "families", "p10_clique", (P10,)),
        ("h9_unique", "sat_e8", "uniqueness_h9", ()),
        ("calibrations", "sat_e8", "calibrations", ()),
        ("e8_cliques", "sat_e8", "e8_clique_facts", ()),
    ]
    for p in (4, 5, 10, 11):
        t.append((f"bit_p{p}", "families", "paired_bit", (p,)))
    for p in (4, 5, 6, 7):
        t.append((f"omega_bit_{p}", "families", "incap_omega", (p, "bit")))
        if p != 7:
            t.append((f"omega_cx_{p}", "families", "incap_omega", (p, "cx")))
    sat = importlib.import_module("sat_e8")
    npats = {}
    for r in (16, 17):
        chunks, n = sat.k2_tasks(r, 32)
        npats[r] = n
        for i, ch in enumerate(chunks):
            t.append((f"k2_r{r}_{i}", "sat_e8", "k2_solve", (ch,)))
    return t, npats


def work(spec):
    mod, fn, args = spec
    sys.dont_write_bytecode = True
    t0 = time.monotonic()
    out = getattr(importlib.import_module(mod), fn)(*args)
    return out, time.monotonic() - t0


def strip_seconds(x):
    if isinstance(x, dict):
        return {k: strip_seconds(v) for k, v in x.items() if k != "seconds"}
    if isinstance(x, list):
        return [strip_seconds(v) for v in x]
    return x


def assemble(res, npats):
    import families
    import sat_e8
    f = {}
    f["certificates"] = {k: res[f"cert_{k}"] for k in ("p3", "p10", "p11")}
    f["toy_p3"] = res["toy_p3"]
    f["pivots"] = dict(thm_P={"p10": res["thmP_p10"], "p11": res["thmP_p11"]}, copy_count_p10=res["copy_count_p10"],
                       overlap_scan_p10=res["overlap_p10"])
    f["mutable_425"] = res["mutable_425"]
    f["pricing"] = res["pricing"]
    u_res, u = res["h9_unique"]
    fam = dict(paired_bit={str(p): res[f"bit_p{p}"] for p in (4, 5, 10, 11)}, e8_bitdual=res["e8_bitdual"],
               e8_complex=families.e8_complex(u), p10_clique=res["p10_clique"],
               omega={f"{k}_{p}": res[f"omega_{k}_{p}"] for p in (4, 5, 6, 7) for k in ("bit", "cx")
                      if f"omega_{k}_{p}" in res})
    f["families"] = fam
    k2 = {}
    for r in (16, 17):
        parts = [res[f"k2_r{r}_{i}"] for i in range(32)]
        k2[f"r{r}"] = sat_e8.k2_collect(r, parts, npats[r])
    f["e8_labels"] = dict(uniqueness_h9=u_res, calibrations=res["calibrations"], cliques=res["e8_cliques"],
                          k2_planes=k2)
    # Thm B table, derived from the measured neighbourhood ranks: m >= 1 + s * rank N versus the layout widths s * h
    tb = {}
    for name, h, rank in (("complex_p10", 20, f["certificates"]["p10"]["N_rank"]),
                          ("complex_p11", 22, f["certificates"]["p11"]["N_rank"]),
                          ("bit_p10", 20, [fam["paired_bit"]["10"]["N_rank"]] * 2),
                          ("bit_p11", 22, [fam["paired_bit"]["11"]["N_rank"]] * 2),
                          ("e8_bit_dual", 8, [fam["e8_bitdual"]["neighbourhood"][0][1]] * 2),
                          ("e8_complex", 9, [fam["e8_complex"]["N_rank"]] * 2)):
        assert rank == [h - 1, h - 1], (name, rank)
        tb[name] = {f"s{s}": dict(m_min=1 + s * (h - 1), layout_s_times_h=s * h) for s in (3, 5, 7, 9)}
    f["thmB_table"] = tb
    return f


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--output", type=Path, help="new directory (outside the package) for facts.json / verification.json")
    ap.add_argument("--jobs", type=int, default=max(1, min(12, (os.cpu_count() or 2))))
    ap.add_argument("--write-expected", action="store_true", help="maintenance: rewrite expected.json from this run")
    args = ap.parse_args()
    assert sys.version_info >= (3, 11), "Python 3.11+ required"
    for pkg, ver in PINNED_PACKAGES.items():
        got = md.version(pkg)
        assert got == ver, f"{pkg}=={ver} required, found {got} (python3 -m pip install -r requirements.txt)"
    out = args.output or Path(tempfile.mkdtemp(prefix="format-obstructions-"))
    if args.output:
        assert not out.resolve().is_relative_to(ROOT) and not out.exists(), "output must be new and outside the package"
        out.mkdir(parents=True)
    before = package_files()
    npins = integrity()
    T0 = time.monotonic()
    tk, npats = tasks()
    res, secs = {}, {}
    print(f"[{time.monotonic() - T0:6.1f}s] {npins} pinned inputs verified; {len(tk)} tasks on {args.jobs} workers", flush=True)
    ctx = mp.get_context("spawn")
    with ProcessPoolExecutor(max_workers=args.jobs, mp_context=ctx) as ex:
        fut = {ex.submit(work, (m, fn, a)): tid for tid, m, fn, a in tk}
        for f in as_completed(fut):
            tid = fut[f]
            try:
                res[tid], secs[tid] = f.result()
            except BaseException:
                traceback.print_exc()
                raise SystemExit(f"FAILED task {tid}")
            if not tid.startswith("k2_") or len([k for k in res if k.startswith("k2_")]) % 16 == 0:
                print(f"[{time.monotonic() - T0:6.1f}s] done {tid} ({secs[tid]:.1f}s)", flush=True)
    facts = assemble(res, npats)
    wall = time.monotonic() - T0
    norm = json.loads(json.dumps(strip_seconds(facts), sort_keys=True))
    exp_path = ROOT / "expected.json"
    if args.write_expected:
        exp_path.write_text(json.dumps(norm, indent=1, sort_keys=True) + "\n")
        print("expected.json written")
    else:
        want = json.loads(exp_path.read_text())
        assert norm == want, "facts differ from expected.json: " + ", ".join(
            k for k in sorted(set(norm) | set(want)) if norm.get(k) != want.get(k))
    after = package_files()
    if args.write_expected:
        after = [x for x in after if x != "expected.json"]
    assert after == [x for x in before if not (args.write_expected and x == "expected.json")], \
        "the package tree changed during the run"
    stage_secs = {}
    for tid, s in secs.items():
        key = "k2_planes" if tid.startswith("k2_") else tid
        stage_secs[key] = round(stage_secs.get(key, 0.0) + s, 1)
    report = dict(status="PASS", python=sys.version.split()[0], packages=PINNED_PACKAGES, pinned_inputs=npins,
                  tasks=len(tk), jobs=args.jobs, wall_seconds=round(wall, 1), cpu_seconds_sum=round(sum(secs.values()), 1),
                  stage_cpu_seconds=dict(sorted(stage_secs.items(), key=lambda kv: -kv[1])))
    (out / "facts.json").write_text(json.dumps(facts, indent=1, sort_keys=True) + "\n")
    (out / "verification.json").write_text(json.dumps(report, indent=1) + "\n")
    print(json.dumps(report), flush=True)
    print(f"PASS: all format-obstruction checks, wall {wall:.1f}s (output in {out})", flush=True)


if __name__ == "__main__":
    main()
