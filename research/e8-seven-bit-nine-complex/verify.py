#!/usr/bin/env python3
"""Replay both E8 suppliers and their shared conditional outer assembly.
Prepared with OpenAI Codex assistance. Apache-2.0.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse, hashlib, importlib.util, json, os, subprocess, sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2,default=str)+'\n')
def integrity():
    files=read(ROOT/'MANIFEST.json')
    assert {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}==set(files)|{'MANIFEST.json'}
    for p,h in files.items():assert sha(ROOT/p)==h,p
    sources=read(ROOT/'SOURCES.json')
    assert sha(ROOT/'source375/MANIFEST.sha256')==sources['bit']['manifest_sha256']
    assert sha(ROOT/'source377/MANIFEST.json')==sources['complex']['manifest_sha256']
def main():
    assert __debug__, 'Keep assertions enabled'
    ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);ap.add_argument('--boost-include',type=Path);a=ap.parse_args();out=a.output.resolve()
    assert out!=ROOT and ROOT not in out.parents and not out.exists()
    integrity();out.mkdir(parents=True);(out/'tmp').mkdir()
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(out/'tmp'),VERIFY_PYTHON=sys.executable,SOURCE375=str(ROOT/'source375'),CX_RECORD=str(out/'unexpected-record.json'))
    includes=[str(a.boost_include)] if a.boost_include else []
    if sys.platform=='darwin':includes.insert(0,str(ROOT/'support'))
    if env.get('CPLUS_INCLUDE_PATH'):includes.append(env['CPLUS_INCLUDE_PATH'])
    if includes:env['CPLUS_INCLUDE_PATH']=os.pathsep.join(includes)
    def run(argv,log):
        print('RUN',log,flush=True)
        with (out/log).open('w') as f:subprocess.run(argv,cwd=out,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
    def py(script,*args):return [sys.executable,'-B',str(script),*map(str,args)]
    script=(ROOT/'source375/verify.sh').read_text();old='HERE=$(cd "$(dirname "$0")" && pwd)'
    assert script.count(old)==1 and script.count('PY="python3 -B"')==1
    script=script.replace(old,'HERE=$SOURCE375').replace('set -euo pipefail',"set -euo pipefail\nIFS=$'\\n\\t'").replace('PY="python3 -B"','PY=py; py() { "$VERIFY_PYTHON" -B "$@"; }')
    (out/'bit-baseline.sh').write_text(script)
    run(['bash',str(out/'bit-baseline.sh'),str(out/'bit')],'bit-baseline.log')
    assert not (out/'unexpected-record.json').exists()
    old=read(out/'bit/kappa.json');assert old['kappa']=='95424356568133/100000000000000000'
    # Each original vendor verifier runs unmodified, including its regressions.
    run(py(ROOT/'source377/verify.py','--work',out/'complex'),'complex-component.log')
    receipt=read(out/'complex/VERIFICATION.json')
    assert receipt['status']=='PASS_PORTABLE_NINE_STAGE_COMPLEX_FINITE_COMPONENT'
    assert len(receipt['fresh_stages'])==8 and all(x['returncode']==0 for x in receipt['fresh_stages'])
    co=out/'complex/work/complex-nine-native';audit=read(co/'INDEPENDENT-TEMPLATE-AUDIT.json');global_=read(co/'GLOBAL-REVIEW.json');invoice=global_['finite_invoice']
    b=Q(audit['coarse_complex']);assert str(b)==receipt['complex_coarse']
    assert (global_['m'],global_['live'],global_['physical'],global_['deficit'])==(73,14727,15520,2496)
    assert (invoice['G_exponent'],invoice['E_exponent'],invoice['C0_exponent'])==(30000,100000,210000)
    assert invoice['router_bits']<=30000 and invoice['literal_bits']<=100000 and invoice['required_C0_bits']<=210000
    assert invoice['physical_row_coefficient']==15445<invoice['retained_row_coefficient']==20161
    assert invoice['halving_degree']==2 and invoice['induction_gap_multiple_B']==49
    outer_path=ROOT/'source375/code/pricing/outer.py'
    assert outer_path.read_bytes()==(ROOT/'source377/work/pr361/code/engines/outer.py').read_bytes()
    # The freshly reconstructed complex invoice fits the exact same retained
    # precision/row envelope used by both pinned outer assembly callers.
    bridge=dict(proof='source377/work/complex-nine-native/PROOF.txt',representation='Exact powers with source-bound finite overcharges',semantic=dict(G=dict(base=2,exponent=invoice['G_exponent']),E=dict(base=2,exponent=invoice['E_exponent']),B_upper=dict(base=2,exponent=100001),C0=dict(base=2,exponent=invoice['C0_exponent']),C1=1,strict_literal_gap=1,induction_gap_lower=1),rows=dict(coefficient=invoice['retained_row_coefficient'],degree=10**6,suffix_slope=4*10**6,degree_gap=Q(10**6)-Q(51*invoice['retained_row_coefficient'],25)))
    bit=ROOT/'source375/code/bit';rec=out/'bit/records'
    run(py(bit/'checkers/certify_bit_k.py',rec,b,3,8,7,out/'combined-kappa.json'),'combined-pricing.log')
    k=read(out/'combined-kappa.json');k.pop('word');assert k==read(ROOT/'EXPECTED.json')
    assert k['binding']=='bit' and k['complex_coarse']==str(b)
    for key in ('bit_coarse','normalized_histogram','bit_moment_interval','W','m','T','maxchild'):assert k[key]==old[key]
    spec=importlib.util.spec_from_file_location('outer',outer_path);outer=importlib.util.module_from_spec(spec);spec.loader.exec_module(outer)
    c=Q(k['bit_coarse']);eta=Q(1,10**12);beta=Q(1,10**9);chain=[Q(384599,10**10)]
    assert c<(1-beta)*b
    for _ in range(3):chain.append((1-c)*c+c*chain[-1])
    kappa=Q(k['kappa']);asm=outer.assembly(chain[-1],b,bridge,kappa,eta=eta,beta=beta)
    assert len(asm['strict_constraints'])==47 and all(v>0 for v in asm['strict_constraints'].values())
    try:outer.assembly(chain[-1],b,bridge,kappa+Q(1,10**18),eta=eta,beta=beta)
    except AssertionError:pass
    else:raise AssertionError('adjacent kappa grid point accepted')
    write(out/'assembly.json',dict(bootstrap_chain=list(map(str,chain)),strict_constraints={k:str(v) for k,v in asm['strict_constraints'].items()},parameters={k:str(v) for k,v in asm['parameters'].items()},minimum_margin=str(asm['minimum_margin']),adjacent_grid_rejected=True,common_envelope=bridge))
    run(py(bit/'receipts_k.py',ROOT/'source375/data/bit/bitE8-r865.json.gz',rec,out/'bit/cout/legality.json',out/'bit/k3/columns.json',out/'combined-kappa.json',out/'finite-input.json'),'finite-input.log')
    run(py(bit/'checkers/finite_k.py','e8',out/'finite-input.json',out/'finite.json'),'finite.log')
    assert read(out/'finite.json')==read(out/'bit/finite.json')
    compare=Q(read(ROOT/'SOURCES.json')['comparison']['kappa']);assert kappa>compare
    integrity();result=dict(status='PASS_SEVEN_STAGE_BIT_NINE_STAGE_COMPLEX_COMPOSITION',kappa=str(kappa),bit_coarse=str(c),complex_coarse=str(b),binding='bit',comparison_pr378=str(compare),gain_percent=float(100*(kappa/compare-1)),bit_formal_columns=read(out/'bit/k3/columns.json')['formal_columns_checked'],complex_stages_checked=len(receipt['fresh_stages']),complex_physical_row_coefficient=invoice['physical_row_coefficient'],outer_strict_constraints=47,scope='Conditional on the pinned suppliers and their proof interfaces, including the compressed nine-stage Clifford/window/bank/common-grid/analytic interfaces. No new Lean proof or bit-side circuit claimed.')
    write(out/'RESULT.json',result);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
