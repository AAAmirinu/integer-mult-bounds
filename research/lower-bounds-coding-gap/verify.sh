#!/usr/bin/env bash
# Replay every computational claim of research/lower-bounds-coding-gap. No kappa claim.
#   bash research/lower-bounds-coding-gap/verify.sh OUT_DIR
# Optional:
#   DYSFUNCTOR=/path/to/network-coding-counterexample   (clone at 2ad45b0) for the 33-vertex flow check (note 2)
#   DRAT_TRIM=/path/to/drat-trim                         to check the DRUP proofs of note 3
# Each step prints PASS or FAIL; the script exits non-zero on the first failure.
set -euo pipefail
PKG="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$PKG/../.." && pwd)"
OUT="${1:?usage: verify.sh OUT_DIR}"
mkdir -p "$OUT"; OUT="$(cd "$OUT" && pwd)"
PY="${PYTHON:-python3}"
S="$PKG/scripts"; L="$S/lorentz"
fail() { echo "FAIL $*"; exit 1; }

echo "== 0. manifest"
(cd "$PKG" && sha256sum --quiet -c MANIFEST.sha256) || fail manifest
echo "PASS manifest"

echo "== 1. note 2: paper eta and the motif flow bound"
"$PY" -B "$S/rank_metric_gap.py" > "$OUT/rank_metric_gap.log" || fail rank_metric_gap; grep "^PASS" "$OUT/rank_metric_gap.log" || fail rank_metric_gap

echo "== 2. note 2: dysfunctor 33-vertex instance, exact max concurrent flow"
if [ -n "${DYSFUNCTOR:-}" ]; then
  [ "$(git -C "$DYSFUNCTOR" rev-parse HEAD)" = 2ad45b0ee615787a2860d03bc39b8def6aaaf870 ] || fail "dysfunctor commit"
  "$PY" -B "$DYSFUNCTOR/scripts/verify-network-coding-33.py" --print-edges > "$OUT/edges33.txt"
  "$PY" -B "$S/mcf33.py" "$OUT/edges33.txt" > "$OUT/mcf33.log" || fail mcf33; grep "^PASS" "$OUT/mcf33.log" || fail mcf33
else
  echo "SKIP (set DYSFUNCTOR to a clone of dysfunctor/network-coding-counterexample at 2ad45b0)"
fi

echo "== 3. note 3: Lorentzian minrank"
cd "$OUT"
"$PY" -B "$L/explore.py" 11 > lorentz-explore11.log
grep -q 'max clique size 10 count 10395' lorentz-explore11.log || fail "explore 11"
echo "PASS 10395 maximum non-knowing cliques of size 10 in Gamma_11"
"$PY" -B "$L/final_span.py" > lorentz-final-span.log
grep -q 'n=9: rank of these 33 members of Z(U) = 7' lorentz-final-span.log &&
grep -q 'n=11: rank of these 52 members of Z(U) = 10' lorentz-final-span.log &&
grep -q 'n=13: rank of these 75 members of Z(U) = 12' lorentz-final-span.log || fail final_span
echo "PASS final span: hyperplane at n=9, full space at n=11 and n=13"
"$PY" -B "$L/model.py" 9 > lorentz-model9.log; grep -q '^violations: 0$' lorentz-model9.log || fail "model 9"
"$PY" -B "$L/model.py" 11 > lorentz-model11.log; grep -q '^violations: 130$' lorentz-model11.log || fail "model 11"
echo "PASS sigma-model cross-check: 0 violations at n=9, 130 at n=11"
mkdir -p "$OUT/proofs"
for N in 6 8 10 12; do
  "$PY" -B "$L/patsat_drat.py" "$N" "$OUT/proofs" > "lorentz-patsat-$N.log" || fail "patsat $N"
  cmp -s "$OUT/proofs/patsat-$N.cnf" "$PKG/proofs/patsat-$N.cnf" || fail "patsat $N: CNF differs from the shipped file"
  if [ -n "${DRAT_TRIM:-}" ]; then
    "$DRAT_TRIM" "$OUT/proofs/patsat-$N.cnf" "$OUT/proofs/patsat-$N.drat" > "drat-$N.log" || true
    grep -q 's VERIFIED' "drat-$N.log" || fail "drat-trim $N"
    "$DRAT_TRIM" "$PKG/proofs/patsat-$N.cnf" "$PKG/proofs/patsat-$N.drat" > "drat-shipped-$N.log" || true
    grep -q 's VERIFIED' "drat-shipped-$N.log" || fail "drat-trim shipped $N"
  fi
done
if [ -n "${DRAT_TRIM:-}" ]; then echo "PASS SAT step: N=6,8,10,12 UNSAT with drat-trim-verified proofs (fresh and shipped)"
else echo "PASS SAT step: N=6,8,10,12 UNSAT (proofs written; set DRAT_TRIM to check them)"; fi

echo "== 4. note 4: loss chain on published profiles (two rows read from main)"
"$PY" -B "$S/loss_chain.py" "$ROOT" > "$OUT/loss_chain.log" || fail loss_chain; grep "^PASS" "$OUT/loss_chain.log" || fail loss_chain

echo "== 5. note 4: piece-count remark"
"$PY" -B "$S/piece_count.py" > "$OUT/piece_count.log" || fail piece_count; grep "^PASS" "$OUT/piece_count.log" || fail piece_count

echo "ALL PASS"
