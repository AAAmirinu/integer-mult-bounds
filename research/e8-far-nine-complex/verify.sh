#!/usr/bin/env bash
# One-command verification of research/e8-far-nine-complex.   usage: bash verify.sh [--quick] /fresh/output/dir
#   python3 >= 3.11, standard library only.  --quick skips step 4 (regeneration of the certificate under #377's ledger).
set -euo pipefail
QUICK=0; if [ "${1:-}" = "--quick" ]; then QUICK=1; shift; fi
HERE=$(cd "$(dirname "$0")" && pwd); WD=$(mkdir -p "$1" && cd "$1" && pwd)
case "$WD" in "$HERE"*) echo "output dir must be outside the package"; exit 2;; esac
PY="${PYTHON:-python3} -I -B"; C=$HERE/code; GX=$HERE/complex/gx
ORIG=$HERE/complex/gcert1-e8-r783.json.gz; OURS=$HERE/data/gcert1-e8-r783-far.json.gz
G377=$HERE/data/pr377/GLOBAL-REVIEW.json; WORD=$HERE/data/bit/bitE8-kernel.json.gz

echo "== 0. manifest"; (cd "$HERE" && $PY -c "
import hashlib,sys,os
bad=0;listed=set()
for line in open('MANIFEST.sha256'):
    h,p=line.rstrip('\n').split('  ',1);listed.add(p)
    if hashlib.sha256(open(p,'rb').read()).hexdigest()!=h: print('MISMATCH',p);bad+=1
files={os.path.relpath(os.path.join(r,f)) for r,_,fs in os.walk('.') for f in fs if '__pycache__' not in r}-{'MANIFEST.sha256'}
if files-listed: print('UNLISTED',sorted(files-listed));bad+=1
sys.exit(1 if bad else 0)") || { echo "MANIFEST FAIL"; exit 1; }; echo "   all files match MANIFEST.sha256"

echo "== 1. pinned inputs (git blob ids)"
$PY -c "
import hashlib
def blob(p):
    d=open(p,'rb').read();return hashlib.sha1(b'blob %d\0'%len(d)+d).hexdigest()
pins={'$ORIG':('0bd0bacf744f1c31419e05b834e34a92be77ae57','Sussman gcert1-e8-r783 (wht-power-saving-lean 9c94857; = #363/#365/#375/#378 vendored copy)'),
      '$GX/gx.py':('6d14c0a976146eb881c1e3897b2476f8633d4e9c','Sussman tools/gx/gx.py'),
      '$GX/gxcore.py':('3e3f0a3076f3c326e7833c74eceecb3436dd3185','Sussman tools/gx/gxcore.py'),
      '$OURS':('56708f99a48c3f86bfcabfc526c2ff224bdba66a','PR #378 re-timed certificate gcert1-e8-r783-far (c248962)'),
      '$G377':('332f011f05f1b433e184e207ddf2c724de735514','PR #377 receipt GLOBAL-REVIEW.json (jacklightChen, d0a620f)'),
      '$WORD':('22141be33d588ed9495feaeedda7efe205a5f8d0','PR #382 E8 bit word bitE8-kernel (015f00b)')}
for p,(h,what) in pins.items():
    assert blob(p)==h,(p,blob(p));print('  ',h[:12],what)
assert hashlib.sha256(open('$ORIG','rb').read()).hexdigest()=='4b92f00fc7454b9b15e6d71a3b05062792eacca0a0ca4efee46f87827d57c8aa'
print('   Sussman certificate sha256 4b92f00f... = the E8 certificate pinned by #377 (its README and native358 sources)')"

echo "== 2. complex certificates: Sussman's checkers, the source-span rule, and the full operator identity"
$PY $C/cxcheck.py $ORIG $GX
$PY $C/cxcheck.py $OURS $GX
$PY $C/cxop.py $ORIG $OURS
$PY -c "
import gzip,json
a=json.load(gzip.open('$ORIG'));b=json.load(gzip.open('$OURS'))
assert (a['h'],a['v'],a['R'],a['cst'],a['N'],a['ports'],a['start'],a['final'],a['ret'],a['scat'],a['ext'])==(b['h'],b['v'],b['R'],b['cst'],b['N'],b['ports'],b['start'],b['final'],b['ret'],b['scat'],b['ext'])
assert b['frames'][:len(a['frames'])]==a['frames']
print('   same h, v, R, cst, N = %d, ports, start/final frames, retained totals, scatter table; frame table extended by %d frames'%(b['N'],len(b['frames'])-len(a['frames'])))"

echo "== 3. #377's nine-stage profile, rebuilt from the certificate, with the swapped unit; bit c; PR #315 outer assembly"
$PY $C/nine.py $ORIG $OURS $G377 $WORD $WD/kappa.json
$PY -c "
import json;k=json.load(open('$WD/kappa.json'))
assert k['b']=='999632926176283/1000000000000000000' and k['kappa']=='998634656132003/1000000000000000000' and k['binding']=='complex'
assert k['max_child']==48 and k['halving_degree']==2
print('PASS conditional kappa =',k['kappa'],'=',k['kappa_float'],'(complex-bound: #377 nine-stage component with the re-timed E8 unit; bit PR #382)')"

if [ $QUICK = 0 ]; then
  echo "== 4. regeneration: our search re-run from Sussman's original with #377's ledger (m = 73) reaches the shipped certificate"
  $PY $C/far9.py $ORIG $GX $WD/regen-split.json.gz 120 > $WD/regen.txt
  tail -2 $WD/regen.txt
  $PY $C/cxfinal.py $WD/regen-split.json.gz $ORIG $WD/regen.json.gz
  $PY -c "
import gzip;assert gzip.open('$WD/regen.json.gz').read()==gzip.open('$OURS').read();print('   regenerated certificate equals the shipped one (decompressed bytes): no further move of this family helps at m = 73')"
fi
