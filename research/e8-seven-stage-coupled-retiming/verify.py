#!/usr/bin/env python3
"""Replay pinned PR373, PR365, and their seven-stage composition from source.
Prepared with OpenAI Codex assistance; Apache-2.0. No network or saved PASS inputs.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse, gzip, hashlib, importlib.util, json, os, subprocess, sys

ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def read(p):
    return json.loads(p.read_text())

def write(p, value):
    p.write_text(json.dumps(value, indent=2) + '\n')

def manifests():
    manifest = read(ROOT / 'MANIFEST.json')
    for path, digest in manifest.items():
        assert sha(ROOT / path) == digest, path
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    assert actual == set(manifest) | {'MANIFEST.json'}, 'unlisted package files'
    for line in (ROOT / 'source373/MANIFEST.sha256').read_text().splitlines():
        digest, path = line.split(None, 1)
        assert sha(ROOT / 'source373' / path) == digest, path
    source = read(ROOT / 'SOURCES.json')
    assert sha(ROOT / 'source373/MANIFEST.sha256') == source['pr373']['manifest_sha256']

def main():
    if sys.flags.optimize:
        raise SystemExit('Assertions must remain enabled')
    ap = argparse.ArgumentParser(); ap.add_argument('output', type=Path)
    ap.add_argument('--boost-include', type=Path)
    args = ap.parse_args(); out = args.output.resolve()
    assert out != ROOT and ROOT not in out.parents, 'output must be outside package'
    assert not out.exists(), 'choose a fresh output directory'
    manifests(); out.mkdir(parents=True); (out/'tmp').mkdir()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(out/'tmp'),
               VERIFY_PYTHON=sys.executable, SOURCE373=str(ROOT/'source373'),
               CX_RECORD=str(out/'unexpected-record.json'))
    include = [str(args.boost_include)] if args.boost_include else []
    if sys.platform == 'darwin': include.insert(0, str(ROOT/'support'))
    if env.get('CPLUS_INCLUDE_PATH'): include.append(env['CPLUS_INCLUDE_PATH'])
    if include: env['CPLUS_INCLUDE_PATH'] = os.pathsep.join(include)

    def run(command, log, extra=None):
        print('RUN', log, flush=True)
        with (out/log).open('w') as f:
            subprocess.run(command, env=dict(env, **(extra or {})), cwd=out,
                           stdout=f, stderr=subprocess.STDOUT, check=True)

    def py(script, *args):
        return [sys.executable, '-B', str(script), *map(str,args)]

    # Run the complete original baseline script. Only shell transport changes:
    # honor spaces in paths and use the same Python interpreter as this verifier.
    script = (ROOT/'source373/verify.sh').read_text()
    old = 'HERE=$(cd "$(dirname "$0")" && pwd)'
    assert script.count(old) == 1 and script.count('PY="python3 -B"') == 1
    script = script.replace(old, 'HERE=$SOURCE373')
    script = script.replace('set -euo pipefail', "set -euo pipefail\nIFS=$'\\n\\t'")
    script = script.replace('PY="python3 -B"', 'PY=py; py() { "$VERIFY_PYTHON" -B "$@"; }')
    (out/'baseline.sh').write_text(script)
    run(['bash', str(out/'baseline.sh'), str(out/'baseline')], 'baseline.log')
    assert not (out/'unexpected-record.json').exists(), 'baseline pins incomplete'
    expected = read(ROOT/'EXPECTED.json')
    baseline = read(out/'baseline/kappa.json'); baseline.pop('word')
    assert baseline == expected['baseline']
    print('PASS full pinned PR373 replay', flush=True)

    # PR365 independently reconstructs the circuit and checks every entry of
    # the full rational scalar map, including all initial helper columns.
    run(py(ROOT/'source365/verify.py'), 'pr365.json')
    pr365 = read(out/'pr365.json'); assert pr365['status'] == 'PASS'
    original = ROOT/'source373/code/complex/inputs/e8/tools/certificate/gcert1-e8-r783.json.gz'
    assert original.read_bytes() == (ROOT/'source365/data/original.json.gz').read_bytes()
    cert = ROOT/'source365/data/retimed.json.gz'; raw = gzip.decompress(cert.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == pr365['uncompressed_sha256'][1]

    cx = ROOT/'source373/code/complex'
    source_pins = read(cx/'inputs/complex/source-pins.json')
    source_pins['certificate'].update(path=str(cert), compressed_sha256=sha(cert),
                                     uncompressed_sha256=hashlib.sha256(raw).hexdigest())
    write(out/'candidate-source-pins.json',source_pins)
    # All structural/count pins are frozen; unexpected record mode is rejected.
    print('RUN candidate complex receipt', flush=True)
    with (out/'candidate-complex.json').open('w') as f, (out/'candidate-progress.log').open('w') as err:
        subprocess.run(py(cx/'portable_complex.py'),cwd=out,env=dict(env,
            CX_PINS=str(ROOT/'candidate-pins-b3.json'),
            CX_SOURCE_PINS=str(out/'candidate-source-pins.json')),
            stdout=f,stderr=err,check=True)
    assert not (out/'unexpected-record.json').exists()
    candidate = read(out/'candidate-complex.json')
    assert candidate['status'] == 'PASS_FRESH_COMPLEX_LABEL_SCALAR_SPLICE_PRECISION'
    assert candidate['ledger'] == expected['complex_ledger']
    oldcx = read(out/'baseline/complex-guard-b3.json')
    for key in ('rank_mass','deficit','max_child','copy_calls','centres','idle_calls'):
        assert candidate['ledger'][key] == oldcx['ledger'][key]
    assert candidate['ledger']['calls'] == oldcx['ledger']['calls'] - 7
    for key in ('forward','backward'):
        assert candidate['scalar_bill'][key]['totals'] == oldcx['scalar_bill'][key]['totals']
    oldH = {int(k):v for k,v in oldcx['five_stage_histogram'].items()}
    H = {int(k):v for k,v in candidate['five_stage_histogram'].items()}
    delta = {k:H.get(k,0)-oldH.get(k,0) for k in H.keys() | oldH.keys()}
    assert {k:v for k,v in delta.items() if v} == {int(k):7*v for k,v in pr365['histogram_delta'].items()}

    pricing = ROOT/'source373/code/pricing'
    moment = load('moment',pricing/'moment.py'); other=load('base_two_moment',pricing/'base_two_moment.py')
    m=candidate['precision_guard']['m']; W=candidate['precision_guard']['live_per_vertex']
    root=moment.certify(H,m,W,True); b=Q(int(Q(root['lower'])*10**18),10**18)
    assert str(b) == expected['candidate']['complex_coarse']
    bounds=[]; fallback=32*m*m*sum(H.values()); grid=Q(1,10**18)
    for saving in [b,b+grid]:
        a=moment.moment(H,m,W,saving,True)
        low,up=other.moment(m,W,list(H.items()),saving)
        flo,fup=other.moment(m,W,[(1,fallback)],saving)
        alt=[low+Q(1,10**16)*flo,up+Q(1,10**16)*fup]
        if saving==b: assert max(a[1],alt[1])<1
        else: assert min(a[0],alt[0])>1
        bounds.append(dict(saving=str(saving),original=list(map(str,a)),independent=list(map(str,alt))))
    write(out/'candidate-complex-moment.json',dict(b=str(b),bounds=bounds,histogram=H,m=m,W=W))
    bit=ROOT/'source373/code/bit'; rec=out/'baseline/records'
    run(py(bit/'checkers/certify_bit_k.py',rec,b,3,8,7,out/'candidate-kappa.json'),'candidate-pricing.log')
    kappa=read(out/'candidate-kappa.json'); kappa.pop('word')
    assert kappa==expected['candidate'] and Q(kappa['kappa'])>Q(baseline['kappa'])
    for key in ('bit_coarse','normalized_histogram','bit_moment_interval','W','m','T','maxchild'):
        assert kappa[key]==baseline[key]
    run(py(bit/'receipts_k.py',ROOT/'source373/data/bit/bitE8-r865.json.gz',rec,
           out/'baseline/cout/legality.json',out/'baseline/k3/columns.json',
           out/'candidate-kappa.json',out/'candidate-finite-input.json'),'candidate-finite-input.log')
    run(py(bit/'checkers/finite_k.py','e8',out/'candidate-finite-input.json',out/'candidate-finite.json'),
        'candidate-finite.log')
    assert read(out/'candidate-finite.json')==read(out/'baseline/finite.json')
    manifests()
    result=dict(status='PASS_FULL_SOURCE_BOUND_SEVEN_STAGE_COMPOSITION',
        kappa=kappa['kappa'],baseline_kappa=baseline['kappa'],complex_b=str(b),
        relative_gain_percent=float(100*(Q(kappa['kappa'])/Q(baseline['kappa'])-1)),
        bit_word_sha256=sha(ROOT/'source373/data/bit/bitE8-r865.json.gz'),
        complex_certificate_sha256=sha(cert),complex_uncompressed_sha256=hashlib.sha256(raw).hexdigest(),
        seven_stage_histogram_delta={k:v for k,v in delta.items() if v},
        complete_scalar_map=pr365['scalar_map_rows_and_columns'],
        checks=['full PR373 replay and controls','full PR365 replay and controls','frozen complex B3 pins',
                'two rational moment engines and adjacent-tick rejection','47 strict assembly constraints',
                'unchanged seven-stage bit histogram and finite bill'],
        scope='Conditional inherited PR373/365 interfaces; no new Lean build or unconditional multiplication theorem.')
    write(out/'RESULT.json',result);print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__': main()
