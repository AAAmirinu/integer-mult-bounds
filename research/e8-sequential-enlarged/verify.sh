#!/usr/bin/env bash
# One-command verification of research/e8-sequential-enlarged.   usage: bash verify.sh [--quick] /fresh/output/dir
#   python3 >= 3.11, standard library only.  --quick skips the regenerations (sink scans, isolation screen, re-synthesis discovery).
set -euo pipefail
QUICK=0; if [ "${1:-}" = "--quick" ]; then QUICK=1; shift; fi
HERE=$(cd "$(dirname "$0")" && pwd); WD=$(mkdir -p "$1" && cd "$1" && pwd)
case "$WD" in "$HERE"*) echo "output dir must be outside the package"; exit 2;; esac
PY="${PYTHON:-python3} -I -B"; C=$HERE/code; GX=$HERE/complex/gx; D=$HERE/data

echo "== 0. manifest"; (cd "$HERE" && $PY -c "
import hashlib,sys,os
bad=0;listed=set()
for line in open('MANIFEST.sha256'):
    h,p=line.rstrip('\n').split('  ',1);listed.add(p)
    if hashlib.sha256(open(p,'rb').read()).hexdigest()!=h: print('MISMATCH',p);bad+=1
files={os.path.relpath(os.path.join(r,f)) for r,_,fs in os.walk('.') for f in fs if '__pycache__' not in r}-{'MANIFEST.sha256'}
if files-listed: print('UNLISTED',sorted(files-listed));bad+=1
sys.exit(1 if bad else 0)") && echo "   all files match MANIFEST.sha256"

echo "== 1. pinned inputs (git blob ids)"
$PY -c "
import hashlib
def blob(p):
    d=open(p,'rb').read();return hashlib.sha1(b'blob %d\0'%len(d)+d).hexdigest()
pins={'$GX/gx.py':('6d14c0a976146eb881c1e3897b2476f8633d4e9c','Sussman tools/gx/gx.py'),
      '$GX/gxcore.py':('3e3f0a3076f3c326e7833c74eceecb3436dd3185','Sussman tools/gx/gxcore.py'),
      '$D/gcert1-e8-r783-far.json.gz':('56708f99a48c3f86bfcabfc526c2ff224bdba66a','PR #378 far-retimed E8 word (ours)'),
      '$D/pr390/prefix18.json.gz':('51f3ea73e0c1726351450e54e4873cfdd4d98d9e','PR #390 prefix18 word (Dugongue, 0e790f2)'),
      '$D/pr390/sink-audit.json':('ef2b6f9ee9d4c0cdd3a3a3aa46e8cfaf2958bf6d','PR #390 sink-audit.json (sinks 355/403)'),
      '$D/pr390/prewhite.json':('527a2ea46180a2e9464acbc7f8298474d5b78762','PR #390 prewhite.json (regression target only)'),
      '$D/pr398/signed25.json.gz':('23a6396ded06ffdd27a94e60bb0fe5ce4bea42ad','PR #398 R781 signed25 word (Dugongue, c3251c8)'),
      '$D/pr398/VALIDATION.json':('3b1a9bb6a400aed56ba08a2bdb8d90c9a4dace0d','PR #398 VALIDATION.json (kappa/b control)'),
      '$D/bit/bitE8-kernel.json.gz':('22141be33d588ed9495feaeedda7efe205a5f8d0','PR #382 E8 bit word (ours; #399 control only)'),
      '$D/pr401/selection.json':('6e75d62b7d419d203794840dcf964973addde0a9','PR #401 frames/selection.json (Dugongue, 7844f72)'),
      '$D/pr401/BANK-PATTERNS.json':('dae63550e4401415ac6a9d8da6534d81871deed9','PR #401 architecture/inputs/BANK-PATTERNS.json'),
      '$D/pr401/RESULT.json':('fa8bd211feff887a8c0bdd100332c2a3918d5142','PR #401 RESULT.json (bit coarse bound; b/kappa control)'),
      '$D/pr401/LICENSE-pr401':('261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64','PR #401 LICENSE (Apache-2.0)'),
      '$D/pr404/selection194.json':('486fc922eb80ae96b0ff30cd1a06a10ef3a729b0','PR #404 shared/selection194.json (Dugongue, 12f4882)'),
      '$D/pr404/bank-patterns.json':('3656863376afe53564d4d507e0b8fc67fd191f9f','PR #404 inputs/bank-patterns.json'),
      '$D/pr404/RESULT.json':('cbae9cc8fd797052f08353cf73c5ab7831b23f37','PR #404 RESULT.json (bit coarse bound; b/kappa control)'),
      '$D/pr404/LICENSE-pr404':('261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64','PR #404 LICENSE (Apache-2.0)'),
      '$D/pr409/SELECTION.json':('8b50349ab39a2c9cf90b39b8d01f4cfe26649b0a','PR #409 research/e8-sequential-gauges/SELECTION.json (rohanarun, 212e03d)'),
      '$D/pr409/PATTERNS.json':('153f46123b68faa0e72c3cb55a40343cf7e15839','PR #409 PATTERNS.json (b/kappa control)'),
      '$D/pr409/LICENSE-pr409':('261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64','PR #409 LICENSE (Apache-2.0)'),
      '$D/pr410/enlarged205.json':('fd74288793629087ba7dccef0416d87fdf21ea12','PR #410 research/e8-enlarged-sequential206/shared/enlarged205.json (eumemic, 95ad14d)'),
      '$D/pr410/bank-patterns.json':('acaa0964fb5e16f9ea964d1424eaa2d6e6bd30d1','PR #410 inputs/bank-patterns.json (b/kappa control)'),
      '$D/pr410/LICENSE-pr410':('261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64','PR #410 LICENSE (Apache-2.0)'),
      '$D/pr408/selection205.json':('f38d996f40a8399bd9c829b1e5c1b2393113a21d','PR #408 research/e8-shared-donor-205-bank64/shared/selection205.json (eumemic, 26332a3; control)'),
      '$D/pr408/bank-patterns.json':('c60f2aaea494493ea8a0c27090318a9e61268798','PR #408 inputs/bank-patterns.json (b/kappa control)'),
      '$D/pr408/LICENSE-pr408':('261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64','PR #408 LICENSE (Apache-2.0)')}
for p,(h,what) in pins.items():
    assert blob(p)==h,(p,blob(p));print('  ',h[:12],what)"

echo "== 2. controls: our #399 pipeline (bracket regression on #390, #398 b/kappa, #399 kappa)"
mkdir -p "$WD/c399"
if [ $QUICK = 1 ]; then $PY $C/clean.py $HERE $GX $WD/c399/kappa.json; else $PY $C/clean.py $HERE $GX $WD/c399/kappa.json --regen; fi
echo "== 3. control: our #402 (#401 word re-implemented, sink negative check, 177/220 re-synthesis, #401 b/kappa control)"
mkdir -p "$WD/c402"
if [ $QUICK = 1 ]; then $PY $C/resynth401.py $HERE $GX $WD/c402; else $PY $C/resynth401.py $HERE $GX $WD/c402 --regen; fi
echo "== 4. control: our #407 (#404 word re-implemented, re-pivoted gauges, fused sinks 301/387, re-synthesis, #404 b/kappa control)"
mkdir -p "$WD/c407"
if [ $QUICK = 1 ]; then $PY $C/fusion404.py $HERE $GX $WD/c407; else $PY $C/fusion404.py $HERE $GX $WD/c407 --regen; fi
echo "== 5. #406/#408/#409/#410 words re-implemented (hashes, b/kappa controls, checker failures); ours: re-pivoted #409 groups + #410 enlargements + sinks + re-synthesis; local program, banks, price"
$PY $C/compose410.py $HERE $GX $WD
echo "== 6. Sussman's checkers, flipped-sign control and source-span rule on ours"
$PY $C/cxcheck.py $WD/gcert1-e8seqenlarged.json.gz $GX
$PY -c "
import json;k=json.load(open('$WD/kappa.json'));k2=json.load(open('$WD/c402/kappa.json'));k3=json.load(open('$WD/c399/kappa.json'));k4=json.load(open('$WD/c407/kappa.json'))
assert k3['kappa']=='1002661106042177/1000000000000000000' and k2['kappa']=='1013357935292321/1000000000000000000' and k4['kappa']=='7941615395831/7812500000000000'
assert k['kappa_409']=='508625250464133/500000000000000000' and k['kappa_410']=='508781072593909/500000000000000000' and k['kappa_408']=='1017022657082799/1000000000000000000'
assert k['b']=='254703245981514431773/250000000000000000000000' and k['kappa']=='1017776060460931/1000000000000000000' and k['binding']=='complex'
print('PASS conditional kappa =',k['kappa'],'=',k['kappa_float'],'(complex-bound; checker-clean: #409 sequential gauges re-pivoted, #410 enlargements, #404 gauges re-pivoted, fused sinks 301/387, targets 177/220 re-synthesised)')"
