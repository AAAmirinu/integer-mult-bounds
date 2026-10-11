#!/usr/bin/env bash
# One-command verification of research/e8-r779-retimed-closure.   usage: bash verify.sh [--quick] /fresh/output/dir
#   python3 >= 3.11, standard library only.  --quick skips the retiming-search regeneration.
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
      '$D/pr408/LICENSE-pr408':('261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64','PR #408 LICENSE (Apache-2.0)'),
      '$D/pr414/selection.json':('a0eb21464470606a6b4bd4c7ecd72d8b902fcaaf','PR #414 research/e8-grouped210-target-prefixes/newgroup/selection.json (eumemic, 7132ca3)'),
      '$D/pr414/LICENSE-pr414':('261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64','PR #414 LICENSE (Apache-2.0)'),
      '$D/pr416/closure211-SELECTION.json':('c7fcb3b5cc9695bd116c6af8285d996f36100a8b','PR #416 research/e8-frameclosure214-target-prefixes/closure211/SELECTION.json (eumemic, c76d101)'),
      '$D/pr416/closure214-SELECTION.json':('6624229733f481d966cb980e13d01148af3f56f3','PR #416 closure214/SELECTION.json (eumemic, c76d101)'),
      '$D/pr416/LICENSE-pr416':('261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64','PR #416 LICENSE (Apache-2.0)'),
      '$D/pr423/closure215-SELECTION.json':('352efca2b921c1274ed627173dadc0c553bdd23e','PR #420 closure215/SELECTION.json (eumemic, 079d514; same blob in #423)'),
      '$D/pr423/capacity217-SELECTION.json':('b6f41beae4f8b58bf9c9e46efd6d1e3b6a548321','PR #421 capacity217/SELECTION.json (eumemic, 6dfe3f9; same blob in #423)'),
      '$D/pr423/enlarged217-SELECTION.json':('186d59bbaf2f956d235d0dd3fdafe4258a1da26c','PR #423 research/e8-grouped217-entrance-enlargement/enlarged217/SELECTION.json (eumemic, 997613c)'),
      '$D/pr423/grouped217-SELECTION.json':('83c166b159cfe420e96337bbee9a8456a393d154','PR #423 grouped217/SELECTION.json (eumemic, 997613c)'),
      '$D/pr423/LICENSE-pr423':('261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64','PR #423 LICENSE (Apache-2.0)'),
      '$D/pr426/gauged-candidate.json.gz':('0daa4323944fa3b7d08ccf04945fe49f0b61e327','PR #426 research/e8-clean-reuse-extension/data/gauged-candidate.json.gz (ai-nanachi, 88d5525)'),
      '$D/pr426/EXPECTED.json':('0974bc7101b5ba981913dad62e8279a01c05a2e5','PR #426 data/EXPECTED.json (b/kappa control)'),
      '$D/pr426/bank-patterns.json':('be3ff7f23a7a9ac2e85257c589219eefdba38c4a','PR #426 data/bank-patterns.json (control)'),
      '$D/pr426/LICENSE-pr426':('261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64','PR #426 LICENSE (Apache-2.0)'),
      '$D/pr428/retimed217-SELECTION.json':('163a16f915efcc68506e9d2d3b6cf707fbf8b559','PR #428 research/e8-combined-retiming217/retimed217/SELECTION.json (eumemic, 700e057; comparison)'),
      '$D/pr428/block217-SELECTION.json':('6c3ad5b3580c02c376ae39c91807496d811c3193','PR #428 block217/SELECTION.json (= #427, eumemic, 700e057; comparison)'),
      '$D/pr428/LICENSE-pr428':('261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64','PR #428 LICENSE (Apache-2.0)')}
for p,(h,what) in pins.items():
    assert blob(p)==h,(p,blob(p));print('  ',h[:12],what)"

echo "== 2. control: our #424 (R781; #419 + #420/#421 gauges, 14 enlargements, target-124/125 prefixes)"
mkdir -p "$WD/c424"
$PY $C/compose423.py $HERE $GX $WD/c424
$PY $C/cxcheck.py $WD/c424/gcert1-e8enlarged.json.gz $GX
echo "== 3. ours: #426 R779 gauged word + our #424 layers + 13 gate-frame retimings + target-172 prefix; local program, banks, price"
if [ $QUICK = 1 ]; then $PY $C/compose426.py $HERE $GX $WD; else $PY $C/compose426.py $HERE $GX $WD --regen; fi
echo "== 4. Sussman's checkers, flipped-sign control and source-span rule on ours"
$PY $C/cxcheck.py $WD/gcert1-e8r779.json.gz $GX
$PY -c "
import json;k=json.load(open('$WD/c424/kappa.json'));k6=json.load(open('$WD/kappa.json'))
assert k['kappa']=='1018509848057013/1000000000000000000' and k['binding']=='complex'
assert k6['control426']['b']=='254951444354246755323/250000000000000000000000'
assert k6['kappa']=='127469017914851/125000000000000000' and k6['b']=='255198274817418511443/250000000000000000000000' and k6['binding']=='complex' and k6['gauges']==213 and k6['T']==64 and k6['R']==779
print('PASS conditional kappa =',k6['kappa'],'=',k6['kappa_float'],'(complex-bound; gx.check1 + gxcore clean: #426 R779 + our #424 layers + 14 retimings + target-172 prefix)')"
