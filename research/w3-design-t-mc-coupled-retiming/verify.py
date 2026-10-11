#!/usr/bin/env python3
"""Source-bound replay of the coupled retiming extension to PR364.

Requires Python 3.11+, numpy, mpmath, a C++17 compiler and Boost headers.
All generated files, compiler temporaries and logs go under the requested output.
"""
import argparse
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import shutil

if not __debug__:
    raise SystemExit('Assertions must remain enabled')
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SRC = HERE/'source'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())

def check_manifest():
    manifest=read(HERE/'MANIFEST.json')
    actual={str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts}-{'MANIFEST.json'}
    assert actual==set(manifest), ('Manifest membership',actual^set(manifest))
    for name,h in manifest.items():assert sha(HERE/name)==h, ('Hash mismatch',name)
    source=read(HERE/'SOURCE.json')
    assert sha(SRC/'MANIFEST.sha256')==source['manifest_sha256']
    for line in (SRC/'MANIFEST.sha256').read_text().splitlines():
        h,name=line.split('  ',1);assert sha(SRC/name)==h, ('Upstream manifest',name)
    return source

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output',type=Path)
    ap.add_argument('--cxx',default=os.environ.get('CXX','c++'))
    ap.add_argument('--boost-include',default=os.environ.get('BOOST_INCLUDE','/usr/include'))
    a=ap.parse_args();out=a.output.resolve()
    assert not out.exists() and not out.is_relative_to(HERE), 'Output must be new and outside package'
    source=check_manifest();out.mkdir(parents=True);(out/'tmp').mkdir()
    os.environ['TMPDIR']=str(out/'tmp');os.environ['PYTHONDONTWRITEBYTECODE']='1'
    def run(*args):
        print('RUN',*map(str,args),flush=True)
        subprocess.run(list(map(str,args)),check=True)
    def py(script,*args):run(sys.executable,'-B',SRC/'code'/script,*args)
    def archive_snapshot(path):
        archive=out/(path.name+'.tar.gz')
        with tarfile.open(archive,'w:gz') as t:t.add(path,arcname=path.name)
        with tarfile.open(archive,'r:gz') as t:
            for member in t.getmembers():
                if member.isfile():
                    assert hashlib.sha256(t.extractfile(member).read()).hexdigest()==sha(out/member.name)
        shutil.rmtree(path)
    for name in ('staged','parity','parity325'):
        (out/name).mkdir()
        for file in ('249-records.bin','249-states.json','frames.json'):
            (out/name/file).write_bytes(gzip.decompress((SRC/'data'/name/(file+'.gz')).read_bytes()))
    py('dt.py',out/'staged',out/'T');py('comp.py',out/'T')
    saved=os.environ.get('TWIN_CAP');os.environ['TWIN_CAP']='470'
    py('twin.py',out/'T',out/'TT')
    if saved is None:os.environ.pop('TWIN_CAP')
    else:os.environ['TWIN_CAP']=saved
    assert (out/'TT'/'249-records.bin').read_bytes()==gzip.decompress((SRC/'data'/'designt'/'249-records.bin.gz').read_bytes())
    archive_snapshot(out/'staged');archive_snapshot(out/'T')
    before=out/'TT'
    for stage,name,target in [('kernel','kernel','K'),('retime','retime','KR'),('reorder','reorder','KRO'),('reorder','reorder2','base')]:
        py('stages.py',stage,before,out/target,SRC/'stages'/(name+'-selection.json'),SRC/'data'/'labels.json')
        archive_snapshot(before)
        before=out/target
    assert (before/'249-records.bin').read_bytes()==gzip.decompress((SRC/'data'/'final'/'249-records.bin.gz').read_bytes())
    py('price.py',before)
    base_price=read(before/'kappa.json');expected=read(HERE/'EXPECTED.json')
    assert base_price['kappa']==expected['baseline_kappa']
    sys.path.insert(0,str(SRC/'code'))
    import numpy as np
    import stagelib as L
    import stages
    snap=L.load_snapshot(before);sel=read(HERE/'selection.json')
    assert sel['stage']=='retime' and sel['input_records_sha256']==L.rec_sha(snap)
    entries=sel['entries'];assert len({e['record'] for e in entries})==len(entries)
    for e in entries:
        assert 0<=e['record']<len(snap['rec'])
        row=snap['rec'][e['record']].tolist()
        assert row[0]==1 and e['scalar']==[row[1],row[2],row[3],row[5]]
        assert all(len(b)==snap['fr']['h'] and all(isinstance(x,int) for x in b) for b in e['new_basis'])
    # Omission of source binding and mismatched scalar incidences must not be admitted.
    damaged=copy.deepcopy(entries);damaged[0]['scalar'][2]*=-1
    try:stages.retime(snap,damaged)
    except AssertionError:pass
    else:raise AssertionError('Damaged scalar binding accepted')
    changed=stages.retime(snap,entries)
    assert L.rec_sha(changed)==sel['output_records_sha256']==expected['word_sha256']
    def scalar(s):
        r=s['rec'];return r[r[:,0]!=0][:,[0,1,2,3,5]].tobytes()
    assert scalar(snap)==scalar(changed), 'Exact signed scalar instruction sequence changed'
    assert snap['s']['initial']==changed['s']['initial'] and snap['s']['final']==changed['s']['final']
    checks=L.full_check(changed,L.labels_chi(SRC/'data'/'labels.json'),tag='coupled retiming')
    L.save_snapshot(changed,out/'candidate')
    py('nondeg.py',out/'candidate',out/'parity');py('tile.py',out/'candidate')
    # The original historical control is run as well as the changed final word.
    py('dt.py',out/'parity325',out/'T346');py('comp.py',out/'T346');py('twin.py',out/'T346',out/'TT346')
    assert sha(out/'TT346'/'249-records.bin')==expected['historical_control_sha256']
    archive_snapshot(out/'T346');archive_snapshot(out/'TT346');archive_snapshot(out/'parity325')
    h=snap['fr']['h'];v=snap['s']['v'];helpers=snap['s']['n']-2*v
    for exe,file,extra in [('legality','legality_h.cpp',[]),('columns','columns_h.cpp',[f'-DVPORTS={v}',f'-DRHELP={helpers}'])]:
        run(a.cxx,'-O2','-std=c++17',f'-DHDIM={h}',*extra,'-I'+str(SRC/'code'/'checkers'),'-I'+a.boost_include,'-o',out/exe,SRC/'code'/'checkers'/file)
    py('stage_official.py',out/'parity',out/'candidate',out/'cin',out/'cout')
    run(out/'legality',out/'cin',out/'cout',out/'legality.json')
    with (out/'columns.stdout').open('w') as stdout,(out/'columns.stderr').open('w') as stderr:
        subprocess.run([str(out/'columns'),str(out/'cout'/'COHORT249-RECORDS.bin'),str(out/'columns.json')],check=True,stdout=stdout,stderr=stderr)
    columns=read(out/'columns.json');assert columns['status']=='PASS_NEW_COHORT249_ALL_FIVE_STAGE_FORMAL_COLUMNS_AND_PREFIX_BILL'
    py('complex_b.py',SRC/'complex'/'gcert1-e8-r783.json.gz',SRC/'complex'/'gx')
    py('price.py',out/'candidate')
    price=read(out/'candidate'/'kappa.json')
    assert price['kappa']==expected['kappa'] and price['binding']=='bit'
    assert price['local']==expected['local_histogram']
    from fractions import Fraction
    assert Fraction(price['kappa'])>Fraction(base_price['kappa'])
    receipt=dict(status='PASS_SOURCE_BOUND_COUPLED_RETIMING',source=source,word_sha256=L.rec_sha(changed),
                 changed_gates=len(entries),checks=checks,columns=columns,price=price)
    (out/'RESULT.json').write_text(json.dumps(receipt,indent=2))
    print('PASS conditional kappa =',price['kappa'], '=',price['kappa_float'],flush=True)

if __name__=='__main__':main()
