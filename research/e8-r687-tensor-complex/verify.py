"""R687 bit supplier (read-then-climb + exact pivots) composed with two complex suppliers:
  PR #484 (our draft; conditional on its Lemmas A and G), CITED from its pinned full-run result: the bit binds;
  PR #471 (Dugongue), rerun unchanged and composed by #471's own assembler: the complex binds.
usage: python -B research/e8-r687-tensor-complex/verify.py /absolute/new/output [--light]
  --light  (minutes) package integrity; the bit word regenerated from its frozen hierarchy with read-then-climb phases (byte check),
           the copy anatomy/bound, mixing regenerated (byte check), the relaxed all-column checker on the mixed word; then PR #471's
           assembler on the pinned evidence/ (bit and complex supplier outputs), compared with EXPECTED.json.
  default  FULL: the bit package's own full verify.py (PR #443 parent, PR #442 complex upstream, all local/formal/eleven-stage
           checks, hosting, audits), PR #471's complex supplier rerun unchanged (code/complex471.py), the composition on those
           fresh outputs, and equality of the fresh supplier outputs with the pinned evidence.
needs: Python 3.11+, numpy, mpmath, sympy, scipy; CXX (C++17) and BOOST_INCLUDE for FULL.
Prepared by DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code.  Apache-2.0."""
from pathlib import Path
import gzip, hashlib, json, os, shutil, subprocess, sys, time
assert __debug__
ROOT = Path(__file__).resolve().parent; R = ROOT.parent
args = [x for x in sys.argv[1:] if not x.startswith('--')]; flags = {x for x in sys.argv[1:] if x.startswith('--')}
assert len(args) == 1 and flags <= {'--light'}, __doc__
out = Path(args[0]).resolve(); assert not out.exists() and not out.is_relative_to(R)
light = '--light' in flags
read = lambda p: json.loads(Path(p).read_text()); sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def csha(p):
    w = json.load(gzip.open(p, 'rt') if str(p).endswith('.gz') else open(p))
    return hashlib.sha256(json.dumps(w, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
def inv(p): return {f.relative_to(p).as_posix(): sha(f) for f in sorted(Path(p).rglob('*')) if f.is_file() and '__pycache__' not in f.parts}
BIT = R / 'e8-r687-read-then-climb'; P471 = R / 'e8-tensor-normalization'
def integrity():
    a = inv(ROOT); a.pop('MANIFEST.json'); assert a == read(ROOT / 'MANIFEST.json'), 'package manifest differs'
    src = read(ROOT / 'SOURCE.json')
    b = src['bit']; assert sha(BIT / 'MANIFEST.json') == b['manifest_sha256'] and sha(BIT / 'SOURCE.json') == b['source_sha256']
    a = inv(BIT); a.pop('MANIFEST.json'); assert a == read(BIT / 'MANIFEST.json'), 'bit package differs'
    for name, e in read(BIT / 'SOURCE.json')['packages'].items(): assert inv(R / name) == e['files'], ('upstream package differs', name)
    c = src['complex']; assert sha(P471 / 'MANIFEST.json') == c['manifest_sha256']
    m = read(P471 / 'MANIFEST.json'); a = {k: v for k, v in inv(P471).items() if k != 'MANIFEST.json'}
    absent = sorted(set(m) - set(a))   # #471's manifest lists a .gitattributes that its PR tree lacks; when present it is hash-checked
    assert absent in c['manifest_entries_absent_from_pr_tree_allowed'] and {k: v for k, v in m.items() if k in a} == a, 'PR #471 package differs'
    return absent
absent471 = integrity(); out.mkdir(parents=True); (out / 'logs').mkdir(); steps = []
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONINTMAXSTRDIGITS='0'); env.pop('PYTHONOPTIMIZE', None)
if 'BOOST_INCLUDE' not in env and Path('/opt/homebrew/include/boost').exists(): env['BOOST_INCLUDE'] = '/opt/homebrew/include'
def run(name, cmd, stdout_to=None):
    t = time.monotonic(); log = out / 'logs' / (name + '.log'); print('RUN', name, flush=True)
    with log.open('w') as f, (open(stdout_to, 'w') if stdout_to else f) as g:
        q = subprocess.run(list(map(str, cmd)), env=env, stdout=g, stderr=f if stdout_to else subprocess.STDOUT)
    if q.returncode: raise RuntimeError((name, q.returncode, log.read_text()[-4000:]))
    steps.append(dict(name=name, seconds=round(time.monotonic() - t, 2), log_sha256=sha(log))); print('PASS', name, flush=True)
def py(name, path, *a, **k): run(name, [sys.executable, '-B', path, *a], **k)
try:
    E = read(ROOT / 'EXPECTED.json'); EB = read(BIT / 'EXPECTED.json')
    if light:
        w = out / 'bit'; w.mkdir()
        py('bit-hierarchy-compile', BIT / 'code/hier_word_rtc.py', R, BIT / 'data/hierarchy-r687.json', w / 'raw.json.gz', w / 'reused.json.gz', w / 'word.json.gz', stdout_to=w / 'hierarchy.json')
        assert csha(w / 'word.json.gz') == csha(BIT / 'data/word-r687.json.gz') == EB['checks']['word_sha256'] and read(w / 'hierarchy.json') == EB['checks']['hierarchy']
        py('bit-copy-bound', BIT / 'code/copy_bound.py', R, BIT / 'data/hierarchy-r687.json', 'rtc', stdout_to=w / 'copy-bound.json')
        assert read(w / 'copy-bound.json') == EB['checks']['copy_bound']
        py('bit-mix-generate', BIT / 'code/mix_target.py', BIT / 'data/word-kernel.json.gz', w / 'word-mixed.json', stdout_to=w / 'mix.json')
        assert csha(w / 'word-mixed.json') == csha(BIT / 'data/word-mixed.json.gz') == EB['checks']['mixed_word_sha256'] and read(w / 'mix.json') == EB['checks']['mix']
        py('bit-relaxed-checkword-mixed', BIT / 'code/checkword_relaxed.py', BIT / 'data/word-mixed.json.gz', R / 'e8-r740-replica32/parent436/code/pricing', stdout_to=w / 'checkword.txt')
        t_ = (w / 'checkword.txt').read_text(); assert 'legality + exact F2 on all 927 columns: PASS' in t_ and 'all Gram dets > 0' in t_
        bv, cxd = out / 'evidence-bit', out / 'evidence-complex'
        shutil.copytree(ROOT / 'evidence/bit', bv); shutil.copytree(ROOT / 'evidence/complex', cxd)
        g = read(bv / 'nine/GEOMETRY.json'); assert g['note'].startswith('summary') and g['full_sha256'] == E['bit_geometry_sha256']
    else:
        py('full-bit-r687', BIT / 'verify.py', out / 'bitr687')
        rb = read(out / 'bitr687/RECEIPT.json'); assert rb['status'] == 'PASS_R687_READ_THEN_CLIMB_ELEVEN_STAGE_WHOLE_RESIDUAL' and rb['mode'] == 'full' and rb['complex'] == 'pr442'
        py('complex-pr471-unchanged', ROOT / 'code/complex471.py', R, out / 'cx471')
        bv, cxd = out / 'bitr687/eleven/mixed_d3', out / 'cx471/complex'
        assert sha(bv / 'nine/GEOMETRY.json') == E['bit_geometry_sha256']
        drop = lambda d: {k: v for k, v in d.items() if k != 'seconds'}   # wall-clock field
        for p in ('nine/GLOBAL.json', 'hosted/GLOBAL.json', 'hosted/AUDIT.json'): assert drop(read(bv / p)) == drop(read(ROOT / 'evidence/bit' / p)), ('fresh bit output differs from evidence', p)
        for p in ('GLOBAL.json', 'AUDIT.json'): assert read(cxd / p) == read(ROOT / 'evidence/complex' / p), ('fresh complex output differs from evidence', p)
        assert read(out / 'bitr687/eleven/mixed_d3/RESULT.json')['bit_lower'] == EB['variants']['pr442']['bit_lower']
    ab = read(bv / 'hosted/AUDIT.json'); vb = EB['variants']['pr442']
    assert ab['profile'] == vb['bit_profile'] and read(bv / 'hosted/GLOBAL.json')['template_sha256'] == vb['bit_template_sha256'] and read(bv / 'hosted/GLOBAL.json')['emitted_program_sha256'] == vb['emitted_program_sha256']
    py('composition-pr471-assembler', ROOT / 'compose.py', out / 'composition', '--bit-v', bv, '--complex', cxd)
    res = read(out / 'composition/RESULT.json')
    for k, v in E['result_pr471'].items(): assert res[k] == v, (k, res[k], v)
    assert res['bit_lower'] == vb['bit_lower'] and res['binding_component'] == 'complex'
    bitres = out / 'bit-result.json'; bitres.write_text(json.dumps(dict(bit_lower=vb['bit_lower'], halving_depth=vb['halving_depth'], bit=vb['bit']), indent=2) + '\n')
    py('composition-pr484-cited', ROOT / 'compose484.py', bitres, out / 'RESULT-pr484.json')
    r4 = read(out / 'RESULT-pr484.json')
    for k, v in E['result_pr484'].items(): assert r4[k] == v, (k, r4[k], v)
    assert r4['binding_component'] == 'bit' and r4['bit_lower'] == vb['bit_lower']
    integrity()
    receipt = dict(status='PASS_R687_COMPOSITIONS', mode='light' if light else 'full', bit_lower=res['bit_lower'],
                   pr484_cited=dict(kappa=r4['kappa'], kappa_decimal=r4['kappa_decimal'], binding=r4['binding_component'], complex_lower=r4['complex_lower'], gain_over_pr483_percent=r4['gain_over_pr483_percent']),
                   pr471=dict(kappa=res['kappa'], kappa_decimal=res['kappa_decimal'], binding=res['binding_component'], complex_lower=res['complex_lower'], gain_over_pr473_percent=res['gain_over_pr473_percent']),
                   pr471_manifest_entries_absent=absent471, manifest_sha256=sha(ROOT / 'MANIFEST.json'), source_sha256=sha(ROOT / 'SOURCE.json'), python=sys.version.split()[0], steps=steps)
    (out / 'RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n'); print(json.dumps({k: receipt[k] for k in list(receipt)[:5]}, indent=2))
except BaseException as e:
    (out / 'FAILURE.json').write_text(json.dumps(dict(error=repr(e), completed=steps), indent=2) + '\n'); raise
