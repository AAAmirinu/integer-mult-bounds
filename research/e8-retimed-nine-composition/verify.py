#!/usr/bin/env python3
"""Fresh supplier replays and source-bound retimed nine-stage composition.
Prepared with OpenAI Codex assistance. Apache-2.0.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse, gzip, hashlib, importlib.util, json, os, shutil, subprocess, sys
ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, value): p.write_text(json.dumps(value, indent=2, default=str) + '\n')
def integrity():
    manifest = read(ROOT/'MANIFEST.json')
    assert {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()} == set(manifest) | {'MANIFEST.json'}
    for name, digest in manifest.items(): assert sha(ROOT/name) == digest, name
    sources = read(ROOT/'SOURCES.json')
    assert sha(ROOT/'source382/MANIFEST.sha256') == sources['bit']['manifest_sha256']
    assert sha(ROOT/'source377/MANIFEST.json') == sources['complex']['manifest_sha256']
    assert sha(ROOT/'source365/data/retimed.json.gz') == sources['retiming']['certificate_sha256']
def main():
    assert __debug__, 'Keep assertions enabled'
    ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);ap.add_argument('--boost-include',type=Path)
    args=ap.parse_args();out=args.output.resolve()
    assert not out.exists() and out!=ROOT and ROOT not in out.parents
    integrity();out.mkdir(parents=True);(out/'tmp').mkdir()
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(out/'tmp'),VERIFY_PYTHON=sys.executable,SOURCE382=str(ROOT/'source382'))
    if args.boost_include:env['BOOST_INCLUDE']=str(args.boost_include)
    def run(argv, log, cwd=out):
        print('RUN',log,flush=True)
        with (out/log).open('w') as f:subprocess.run(list(map(str,argv)),cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
    def py(script,*a):return [sys.executable,'-B',script,*a]
    script=(ROOT/'source382/verify.sh').read_text();old='HERE=$(cd "$(dirname "$0")" && pwd)';oldpy='PY="${PYTHON:-python3} -I -B"'
    assert script.count(old)==1 and script.count(oldpy)==1
    script=script.replace(old,'HERE=$SOURCE382').replace('set -euo pipefail',"set -euo pipefail\nIFS=$'\\n\\t'")
    script=script.replace(oldpy,'PY=py; py() { "$VERIFY_PYTHON" -I -B "$@"; }')
    (out/'bit-baseline.sh').write_text(script)
    run(['bash',out/'bit-baseline.sh',out/'bit'],'bit-baseline.log')
    bit=read(out/'bit/kappa.json');assert bit['ours_unsplit']['kappa']==read(ROOT/'SOURCES.json')['comparison']['kappa']
    run(py(ROOT/'source377/verify.py','--work',out/'complex-baseline'),'complex-baseline.log')
    baseline=read(out/'complex-baseline/VERIFICATION.json')
    assert baseline['status']=='PASS_PORTABLE_NINE_STAGE_COMPLEX_FINITE_COMPONENT'
    assert len(baseline['fresh_stages'])==8 and all(x['returncode']==0 for x in baseline['fresh_stages'])
    run(py(ROOT/'source365/verify.py'),'pr365.json')
    retime=read(out/'pr365.json');assert retime['status']=='PASS'
    original=ROOT/'source377/work/pr361/complex/gcert1-e8-r783.json.gz'
    assert original.read_bytes()==(ROOT/'source365/data/original.json.gz').read_bytes()
    # Derive a separate work tree. Original supplier sources remain immutable.
    candidate=out/'candidate';candidate.mkdir();shutil.copytree(ROOT/'source377/work',candidate/'work')
    C=candidate/'work/native358/vendor/complex-reserve/upstream/pr352/code/complex'
    modifications={}
    def modify(path,data):
        modifications[str(path.relative_to(candidate))]=dict(before=sha(path),after=hashlib.sha256(data).hexdigest())
        path.write_bytes(data)
    cert=(ROOT/'source365/data/retimed.json.gz').read_bytes();raw=gzip.decompress(cert)
    assert hashlib.sha256(raw).hexdigest()==retime['uncompressed_sha256'][1]
    modify(C/'inputs/e8/tools/certificate/gcert1-e8-r783.json.gz',cert)
    modify(candidate/'work/pr361/complex/gcert1-e8-r783.json.gz',cert)
    sourcepins=read(C/'inputs/complex/source-pins.json')
    sourcepins['certificate'].update(compressed_sha256=hashlib.sha256(cert).hexdigest(),uncompressed_sha256=hashlib.sha256(raw).hexdigest(),source_pin=read(ROOT/'SOURCES.json')['retiming']['head'],url='https://github.com/CrocSwap/integer-mult-bounds/pull/365')
    modify(C/'inputs/complex/source-pins.json',(json.dumps(sourcepins,indent=2)+'\n').encode())
    pins=read(ROOT/'candidate-five-pins.json');original_pins=read(C/'pins-e8.json')
    for key in ('V','R','H','cst','N','scatter','centre_ranks','stock_bits','scalar_steps'):assert pins[key]==original_pins[key]
    assert pins['local_bill']==original_pins['local_bill']-8*64*46**3
    modify(C/'pins-e8.json',(json.dumps(pins,indent=2)+'\n').encode())
    # Freeze changed census/price assertions; no checks are disabled.
    changes=[('global_nine.py','local_children==3974','local_children==3973'),
             ('audit_nine_template.py','999240641319551','999388595603943')]
    for name,old,new in changes:
        path=candidate/'work/odd-stages'/name;code=path.read_text();assert code.count(old)==1
        modify(path,code.replace(old,new).encode())
    write(out/'DERIVATION.json',dict(changes=modifications,scope='Input certificate, its pins, local child count and exact expected price only. All verifier algorithms and controls are retained.'))
    vendor=candidate/'work/native358/vendor/complex-reserve';native=candidate/'work/complex-nine-native'
    run(py(vendor/'admit.py','--source',vendor/'upstream/pr352','--output',native/'local-admission'),'retimed-local-admission.log',candidate)
    guard=read(native/'local-admission/UPSTREAM-GUARD.json');admission=read(native/'local-admission/INDEPENDENT-AUDIT.json')
    assert all(x['all_live_rows_correct'] and x['all_private_work_restored_zero'] for x in admission['scalar_words'].values())
    assert guard['label_checks']['invocation_calls']==3973
    for name in ['complex_candidate.py','verify_clifford_frames.py','data_phases.py','global_nine.py','audit_nine_template.py']:
        run(py(candidate/'work/odd-stages'/name),'retimed-'+name+'.log',candidate)
    global_=read(native/'GLOBAL-REVIEW.json');audit=read(native/'INDEPENDENT-TEMPLATE-AUDIT.json');old=read(out/'complex-baseline/work/complex-nine-native/GLOBAL-REVIEW.json')
    assert global_['status']=='PASS_NINE_STAGE_SOURCE_BOUND_TEMPLATE_OWNERS_PROFILE_AND_FINITE_INVOICE'
    assert audit['status']=='PASS_INDEPENDENT_EMITTED_TEMPLATE_AUDIT_AND_TWO_MOMENTS'
    for key in ('m','live','physical','invocations','rank_mass','deficit','whole_residual_assignments','bank_padding_calls','bridge_additions','terminal_shift_calls','terminal_complete_stream_movements','cover_correction_calls'):
        assert global_[key]==old[key],key
    before={int(r):n for r,n in old['profile'].items()};after={int(r):n for r,n in global_['profile'].items()}
    delta={r:after.get(r,0)-before.get(r,0) for r in before.keys()|after.keys() if after.get(r,0)!=before.get(r,0)}
    assert delta=={int(r):72*n for r,n in retime['histogram_delta'].items()}
    assert global_['paid_calls']==old['paid_calls']-72 and global_['deficit']==2496
    invoice=global_['finite_invoice']
    assert (invoice['G_exponent'],invoice['E_exponent'],invoice['C0_exponent'])==(30000,100000,210000)
    assert invoice['router_bits']<=30000 and invoice['literal_bits']<=100000 and invoice['required_C0_bits']<=210000
    assert invoice['physical_row_coefficient']==15445<invoice['retained_row_coefficient']==20161
    assert invoice['halving_degree']==2 and invoice['induction_gap_multiple_B']==49
    # Reuse PR382's independent rational engines on the freshly emitted profile,
    # then its 47-inequality outer assembly with the freshly replayed bit price.
    sys.path.insert(0,str(ROOT/'source382/code'));import e8core
    b=e8core.coarse(after,global_['m'],global_['live']);assert str(b)==audit['coarse_complex']
    c=Q(bit['ours_unsplit']['c']);kappa,binding=e8core.kappa(c,b);expected=read(ROOT/'EXPECTED.json')
    assert str(kappa)==expected['kappa'] and str(b)==expected['complex_coarse'] and str(c)==expected['bit_coarse'] and binding==expected['binding']=='complex'
    compare=Q(read(ROOT/'SOURCES.json')['comparison']['kappa']);assert kappa>compare
    integrity();result=dict(status='PASS_RETIMED_NINE_STAGE_COMPLEX_KERNEL_BIT_COMPOSITION',kappa=str(kappa),kappa_float=float(kappa),bit_coarse=str(c),complex_coarse=str(b),binding=binding,comparison_pr382=str(compare),gain_percent=float(100*(kappa/compare-1)),complex_profile_delta=delta,complex_paid_calls_removed=72,complex_formal_frames=read(native/'CLIFFORD-REVIEW.json')['frames'],complex_invocations=72,complex_cover_corrections=14727,complex_physical_row_coefficient=15445,outer_strict_constraints=47,scope='Conditional on PR382 kernel entrance completion and omitted PR234-style geometry/finite-bill obligations, its bit degree-two guard, and PR377 compressed-window/bank/Clifford/common-grid/analytic interfaces. No new Lean proof.')
    write(out/'RESULT.json',result);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
