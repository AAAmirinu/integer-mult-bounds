#!/usr/bin/env bash
# One-command verification of research/e8-kernel-bit-b3.   usage: bash verify.sh [--quick] /fresh/output/dir
#   needs python3 >= 3.11 (standard library only), a C++17 compiler (CXX, default c++) and Boost headers (BOOST_INCLUDE).
#   --quick skips the five-stage regression of PR #370's numbers (step 1b).
set -euo pipefail
QUICK=0; if [ "${1:-}" = "--quick" ]; then QUICK=1; shift; fi
HERE=$(cd "$(dirname "$0")" && pwd); WD=$(mkdir -p "$1" && cd "$1" && pwd)
case "$WD" in "$HERE"*) echo "output dir must be outside the package"; exit 2;; esac
PY="${PYTHON:-python3} -I -B"; CXX=${CXX:-c++}; BI=${BOOST_INCLUDE:-/usr/include}; C=$HERE/code; CK=$C/checkers; ST=$HERE/stages
IN=$HERE/data/input/bitE8-r865.json.gz; FIN=$HERE/data/final/bitE8-kernel.json.gz; G377=$HERE/data/pr377/GLOBAL-REVIEW.json

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
for p,h,what in (('$IN','8bec1751f7e33c3a1e4673ef5dbc34d6f205321e','#370 E8 bit word bitE8-r865 (utcorvusvolat-dotcom, b7fe9cd; = #373 data/bit)'),
                 ('$G377','332f011f05f1b433e184e207ddf2c724de735514','#377 nine-stage complex receipt GLOBAL-REVIEW.json (jacklightChen, d0a620f)')):
    assert blob(p)==h,(p,blob(p));print('  ',h[:12],what)"
if [ $QUICK = 0 ]; then
  echo "   1b. regression: our engine reproduces #370's five-stage numbers on its own word"
  $PY -c "
import sys;sys.path.insert(0,'$C');from e8core import *
p=price_word(load_word('$IN'));assert p['c']==Q(452036410121261,5*10**17)
k2,_=kappa(p['c'],B2);k3,_=kappa(p['c'],B3);assert k2==Q(875481145306751,10**18) and k3==Q(903256210211384,10**18)
print('   c =',p['c'],'| kappa(b2) =',k2,'(= #370) | kappa(b3) =',k3,'(= #370 secondary)')"
fi

echo "== 2. transcript stages from frozen selections (each bound to its exact input word, full exact replay after each)"
$PY $C/stages.py retime $IN $WD/retimed.json.gz $ST/retime-selection.json
$PY $C/stages.py kernel $WD/retimed.json.gz $WD/final.json.gz $ST/kernel-selection.json
$PY -c "
import sys,gzip;sys.path.insert(0,'$C');from stages import *
a=load_word('$WD/final.json.gz');b=load_word('$FIN');assert content_sha(a)==content_sha(b);print('   rebuilt final word equals the shipped word (content sha',content_sha(b)[:16]+'...)')"
$PY $C/controls.py $FIN

echo "== 3. labels, nondegeneracy, official PR #266 legality (h = 8, NCOPY = 9) and the bridged formal columns (our B_K port)"
$PY $C/export249.py $FIN $WD/snap $WD/cin $WD/cout
$PY $C/nondeg.py $FIN $WD/snap
$CXX -O2 -std=c++17 -DHDIM=8 -DNCOPY=9 -I$CK -I$BI -o $WD/legality $CK/legality_h.cpp
$CXX -O2 -std=c++17 -DHDIM=8 -I$CK -I$BI -o $WD/legality8 $CK/legality_h.cpp
$CXX -O2 -std=c++17 -DHDIM=8 -DNCOPY=9 -DVPORTS=120 -DRHELP=865 -I$CK -I$BI -o $WD/columns_h $CK/columns_h.cpp
$CXX -O2 -std=c++17 -DHDIM=8 -DNCOPY=9 -DVPORTS=120 -DRHELP=865 -DKPAIRS=2 -I$CK -I$BI -o $WD/columns_k2 $CK/columns_k.cpp
$CXX -O2 -std=c++17 -DHDIM=8 -DNCOPY=9 -DVPORTS=120 -DRHELP=865 -DKPAIRS=3 -I$CK -I$BI -o $WD/columns_k3 $CK/columns_k.cpp
$WD/legality $WD/cin $WD/cout $WD/legality.json > /dev/null
for b in columns_h columns_k2 columns_k3; do $WD/$b $WD/cout/COHORT249-RECORDS.bin $WD/$b.json > /dev/null 2> $WD/$b.err; done
$PY -c "
import json,sys;sys.path.insert(0,'$C');from e8core import *
l=json.load(open('$WD/legality.json'));assert l['status']=='PASS_INDEPENDENT_COHORT_LEGALITY_SOURCE_OWNERS_AND_LIFECYCLE' and l['copies']==9
H=price_word(load_word('$FIN'))['H'];assert {int(a):b for a,b in l['paid_histogram']}==dict(H)
print('   official legality PASS:',l['records'],'records,',l['common_frame_ADDs'],'common-frame ADDs, rank mass',l['rank_mass'],', 9 COPY/ERASE; paid histogram = our replay')
a=json.load(open('$WD/columns_h.json'));b=json.load(open('$WD/columns_k2.json'));k=json.load(open('$WD/columns_k3.json'))
for d in (a,b): d.pop('seconds')
assert a.pop('fresh_center_copies')==120 and b.pop('fresh_center_copies')==54
assert a==b and a['status']=='PASS_NEW_COHORT249_ALL_FIVE_STAGE_FORMAL_COLUMNS_AND_PREFIX_BILL'
print('   regression: our B_K port at K = 2 gives the #266 five-stage columns receipt (1345 columns, 6 omitted-bridge controls) field for field,')
print('   except the h = 20 literal fresh_center_copies = 120 of the original, which the port reports as 6 NCOPY = 54')
assert k['status']=='PASS_NEW_COHORT249_ALL_BRIDGED_STAGE_FORMAL_COLUMNS_AND_PREFIX_BILL' and k['formal_columns_checked']==1585 and len(k['stages'])==7
assert len(k['negative_controls'])==12 and all(x['rejected'] for x in k['negative_controls']) and dict(k['local_raw_H'])==dict(H)
print('   B_3 formal columns PASS:',k['formal_columns_checked'],'physical columns over F2 (dirty helpers, kernel entrances) through 7 invocations,',k['bridge_additions']//120,'twin bridges and the terminal exchange; 12 omitted-bridge controls rejected; prefix payload',k['payload_prefix_bits'],'bits < 104')"
if bash -c '"$0" "$1" "$2" "$3" > /dev/null 2>&1' $WD/legality8 $WD/cin $WD/cout $WD/l8.json 2> /dev/null; then echo "control FAILED: NCOPY = h = 8 accepted"; exit 1; else echo "   control: the unmodified copy count (NCOPY = h = 8) rejects the 9 retained totals"; fi

echo "== 4. B_3 layout (our reimplementation of #363's rule) and banks"
$PY -c "
import sys;sys.path.insert(0,'$C');from layout_bk import layout
assert layout(2,8)['per_pair']=={1:[18],2:[14,7,4]} and layout(3,8)['per_pair']=={1:[34],2:[14,7,20],3:[28,7,6]}
print('   nested climbs, equal-frame twin gates, stage entries, final frames, m-1 moves per role, exchange identity: PASS')
print('   bit idle climbs h = 8: B_2',layout(2,8)['per_pair'],'(= 2h+2 | 2h-2, h-1, 4) | B_3',layout(3,8)['per_pair'],'(= #373)')"
$PY $C/tile_m.py $FIN 56
$PY $C/tile_m.py $FIN 40 1

echo "   halving-degree guard for the bit side (#375's generalised guard, evaluated at the bit parameters; the formal columns above do not depend on the idle-climb split)"
$PY $C/guard.py $FIN

echo "== 5. complex b (#377, re-certified from its receipt), bit c in B_3, PR #315 outer assembly"
$PY $C/kappa.py $FIN $IN $G377 $WD/kappa.json
$PY -c "
import json;k=json.load(open('$WD/kappa.json'))
u=k['ours_unsplit'];s=k['ours_split']
assert u['kappa']=='998243154231047/1000000000000000000' and u['binding']=='complex' and u['halving_degree']==2
assert s['kappa']=='245546943425791/250000000000000000' and s['binding']=='bit' and s['halving_degree']==1
print('PASS conditional kappa =',u['kappa'],'=',u['kappa_float'],'(our E8 bit word in B_3 unsplit, halving degree 2, with #377: complex-bound)')
print('     without the bit-side halving-degree-two admission (B_3 split, degree 1): kappa =',s['kappa'],'=',s['kappa_float'],'(bit-bound)')"
