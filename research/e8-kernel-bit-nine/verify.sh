#!/usr/bin/env bash
# One-command verification of research/e8-kernel-bit-nine.   usage: bash verify.sh [--quick] /fresh/output/dir
#   needs python3 >= 3.11 (standard library only), a C++17 compiler (CXX, default c++) and Boost headers (BOOST_INCLUDE).
#   --quick skips the K = 2 regression of our B_K columns port against the #266 five-stage receipt.
set -euo pipefail
QUICK=0; if [ "${1:-}" = "--quick" ]; then QUICK=1; shift; fi
HERE=$(cd "$(dirname "$0")" && pwd); WD=$(mkdir -p "$1" && cd "$1" && pwd)
case "$WD" in "$HERE"*) echo "output dir must be outside the package"; exit 2;; esac
PY="${PYTHON:-python3} -I -B"; CXX=${CXX:-c++}; BI=${BOOST_INCLUDE:-/usr/include}; C=$HERE/code; CK=$C/checkers; ST=$HERE/stages
IN=$HERE/data/input/bitE8-r865.json.gz; FS=$HERE/data/pr376/frame-selection.json; RS=$HERE/data/pr376/reuse-selection.json
FIN=$HERE/data/final/bitE8-nine-kernel.json.gz; CB=$HERE/data/complex-b.json

echo "== 0. manifest"; (cd "$HERE" && $PY -c "
import hashlib,sys,os
bad=0;listed=set()
for line in open('MANIFEST.sha256'):
    h,p=line.rstrip('\n').split('  ',1);listed.add(p)
    if hashlib.sha256(open(p,'rb').read()).hexdigest()!=h: print('MISMATCH',p);bad+=1
files={os.path.relpath(os.path.join(r,f)) for r,_,fs in os.walk('.') for f in fs if '__pycache__' not in r}-{'MANIFEST.sha256'}
if files-listed: print('UNLISTED',sorted(files-listed));bad+=1
sys.exit(1 if bad else 0)") || exit 1; echo "   all files match MANIFEST.sha256"

echo "== 1. pinned inputs (git blob ids) and our reconstruction of PR #376's R822 word"
$PY -c "
import hashlib
def blob(p):
    d=open(p,'rb').read();return hashlib.sha1(b'blob %d\0'%len(d)+d).hexdigest()
for p,h,what in (('$IN','8bec1751f7e33c3a1e4673ef5dbc34d6f205321e','#370 E8 bit word bitE8-r865 (utcorvusvolat-dotcom; = #381 data/bit, = #373 data/bit)'),
                 ('$FS','647b34368f3f0c7d228c70fa335af872e7946beb','#376 frame witness frame-selection.json (applecrusher, research/e8-bit-helper-reuse)'),
                 ('$RS','a6954dc65f28137ad16d015b42c40dbbde0bd66f','#376 helper-reuse witness reuse-selection.json (applecrusher)')):
    assert blob(p)==h,(p,blob(p));print('  ',h[:12],what)"
$PY $C/apply376.py $IN $FS $RS $WD/w376.json.gz

echo "== 2. our kernel stage from its frozen selection (bound to the exact R822 word; full exact replay after it)"
$PY $C/stages.py kernel $WD/w376.json.gz $WD/final.json.gz $ST/kernel-selection.json
$PY -c "
import sys;sys.path.insert(0,'$C');from stages import *
a=load_word('$WD/final.json.gz');b=load_word('$FIN');assert content_sha(a)==content_sha(b);print('   rebuilt final word equals the shipped word (content sha',content_sha(b)[:16]+'...)')"
$PY $C/controls.py $FIN

echo "== 3. labels, nondegeneracy, official PR #266 legality (h = 8, NCOPY = 9) and the bridged formal columns at K = 4 (our B_K port)"
R=$($PY -c "import sys;sys.path.insert(0,'$C');from e8core import load_word;print(load_word('$FIN')['R'])"); test "$R" = 822
$PY $C/export249.py $FIN $WD/snap $WD/cin $WD/cout
$PY $C/nondeg.py $FIN $WD/snap
$CXX -O2 -std=c++17 -DHDIM=8 -DNCOPY=9 -I$CK -I$BI -o $WD/legality $CK/legality_h.cpp
$CXX -O2 -std=c++17 -DHDIM=8 -I$CK -I$BI -o $WD/legality8 $CK/legality_h.cpp
$CXX -O2 -std=c++17 -DHDIM=8 -DNCOPY=9 -DVPORTS=120 -DRHELP=$R -DKPAIRS=4 -I$CK -I$BI -o $WD/columns_k4 $CK/columns_k.cpp
$WD/legality $WD/cin $WD/cout $WD/legality.json > /dev/null
$WD/columns_k4 $WD/cout/COHORT249-RECORDS.bin $WD/columns_k4.json > /dev/null 2> $WD/columns_k4.err
if [ $QUICK = 0 ]; then
  $CXX -O2 -std=c++17 -DHDIM=8 -DNCOPY=9 -DVPORTS=120 -DRHELP=$R -I$CK -I$BI -o $WD/columns_h $CK/columns_h.cpp
  $CXX -O2 -std=c++17 -DHDIM=8 -DNCOPY=9 -DVPORTS=120 -DRHELP=$R -DKPAIRS=2 -I$CK -I$BI -o $WD/columns_k2 $CK/columns_k.cpp
  for b in columns_h columns_k2; do $WD/$b $WD/cout/COHORT249-RECORDS.bin $WD/$b.json > /dev/null 2> $WD/$b.err; done
  $PY -c "
import json
a=json.load(open('$WD/columns_h.json'));b=json.load(open('$WD/columns_k2.json'))
for d in (a,b): d.pop('seconds')
assert a.pop('fresh_center_copies')==120 and b.pop('fresh_center_copies')==54
assert a==b and a['status']=='PASS_NEW_COHORT249_ALL_FIVE_STAGE_FORMAL_COLUMNS_AND_PREFIX_BILL'
print('   regression: our B_K port at K = 2 gives the #266 five-stage columns receipt field for field (except the h = 20 literal fresh_center_copies)')"
fi
$PY -c "
import json,sys;sys.path.insert(0,'$C');from e8core import *
l=json.load(open('$WD/legality.json'));assert l['status']=='PASS_INDEPENDENT_COHORT_LEGALITY_SOURCE_OWNERS_AND_LIFECYCLE' and l['copies']==9
H=replay(load_word('$FIN'))['H'];assert {int(a):b for a,b in l['paid_histogram']}==dict(H)
print('   official legality PASS:',l['records'],'records,',l['common_frame_ADDs'],'common-frame ADDs, rank mass',l['rank_mass'],', 9 COPY/ERASE; paid histogram = our replay')
k=json.load(open('$WD/columns_k4.json'))
assert k['status']=='PASS_NEW_COHORT249_ALL_BRIDGED_STAGE_FORMAL_COLUMNS_AND_PREFIX_BILL' and k['formal_columns_checked']==1782 and len(k['stages'])==9
assert len(k['negative_controls'])==18 and all(x['rejected'] for x in k['negative_controls']) and dict(k['local_raw_H'])==dict(H)
print('   B_4 formal columns PASS:',k['formal_columns_checked'],'physical columns over F2 (dirty helpers, kernel entrances) through 9 invocations,',k['bridge_additions']//120,'twin bridges and the terminal exchange; 18 omitted-bridge controls rejected; prefix payload',k['payload_prefix_bits'],'bits < 104')"
if bash -c '"$0" "$1" "$2" "$3" > /dev/null 2>&1' $WD/legality8 $WD/cin $WD/cout $WD/l8.json 2> /dev/null; then echo "control FAILED: NCOPY = h = 8 accepted"; exit 1; else echo "   control: the unmodified copy count (NCOPY = h = 8) rejects the 9 retained totals"; fi

echo "== 4. B_4 layout (our reimplementation of #363's rule; = #381's idle climbs), banks and the halving-degree guard"
$PY -c "
import sys;sys.path.insert(0,'$C');from layout_bk import layout
assert layout(4,8)['per_pair']=={1:[50],2:[14,7,36],3:[28,7,22],4:[42,7,8]} and layout(3,8)['per_pair']=={1:[34],2:[14,7,20],3:[28,7,6]}
print('   nested climbs, equal-frame twin gates, stage entries, final frames, m-1 moves per role, exchange identity: PASS')
print('   bit idle climbs h = 8: B_4',layout(4,8)['per_pair'],'(= #381) | B_3',layout(3,8)['per_pair'],'(= #373)')"
$PY $C/tile_m.py $FIN 72 9
$PY $C/guard.py $FIN 4

echo "== 5. bit c in B_4 (controls: #381's and #390's bit savings), outer assembly with the cited complex savings"
$PY $C/kappa.py $FIN $IN $WD/w376.json.gz $CB $WD/kappa.json
$PY -c "
import json;k=json.load(open('$WD/kappa.json'))
u=k['bit']['ours'];s=k['bit']['ours_split']
assert u['c']=='1044063934627389/1000000000000000000' and u['halving_degree']==2 and u['T']==9
assert s['c']=='1000662258257099/1000000000000000000' and s['halving_degree']==1
assert k['kappa']['pr407']['kappa']=='7941615395831/7812500000000000'
print('PASS bit coarse saving c =',u['c'],'=',u['c_float'],'(B_4 unsplit, halving degree 2; split degree-1: c =',s['c'],')')
print('     complex-bound with every cited complex supplier; with our #407 b: kappa =',k['kappa']['pr407']['kappa'],'=',k['kappa']['pr407']['kappa_float'])"
