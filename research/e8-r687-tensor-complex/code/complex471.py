"""Run PR #471's complex supplier (research/e8-tensor-normalization, Dugongue) UNCHANGED: the exact complex command sequence of its
verify.py (scalar/phase build, nine-axis normalisation, data phases, borrowed-spectator emission, independent borrowed audit,
independent routes, whole controller), without its bit part (replaced here by the R687 bit supplier).
Integrity: every file of the package must match #471's MANIFEST.json.  The manifest also lists '.gitattributes', which is not in
the PR's git tree (web upload of a dotfile); that single entry is reported, not required.
usage: complex471.py RESEARCH_ROOT OUT.   Prepared by DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code. Apache-2.0."""
from pathlib import Path
import hashlib, json, os, subprocess, sys, time
assert __debug__
R, OUT = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(); ROOT = R / 'e8-tensor-normalization'
assert not OUT.exists()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest(); read = lambda p: json.loads(p.read_text(encoding='utf-8'))
man = read(ROOT / 'MANIFEST.json')
actual = {p.relative_to(ROOT).as_posix(): sha(p) for p in ROOT.rglob('*') if p.is_file() and p.name != 'MANIFEST.json' and '__pycache__' not in p.parts}
missing = sorted(set(man) - set(actual)); assert missing in ([], ['.gitattributes']), missing
assert {k: v for k, v in man.items() if k != '.gitattributes'} == actual, 'PR #471 package differs from its manifest'
OUT.mkdir(parents=True); steps = []
env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1', PYTHONINTMAXSTRDIGITS='0', TMP=str(OUT), TEMP=str(OUT),
           PYTHONPATH=os.pathsep.join(map(str, [ROOT / 'vendor/runtime', ROOT / 'vendor/complex', ROOT / 'code']))); env.pop('PYTHONOPTIMIZE', None)
def py(name, path, *args):
    print('RUN', name, flush=True); t = time.monotonic(); p = OUT / (name + '.log')
    with p.open('w', encoding='utf-8') as f: r = subprocess.run([sys.executable, '-B', *map(str, [path, *args])], env=env, stdout=f, stderr=subprocess.STDOUT)
    assert r.returncode == 0, (name, p.read_text(encoding='utf-8')[-5000:])
    steps.append(dict(name=name, seconds=round(time.monotonic() - t, 3), log_sha256=sha(p))); print('PASS', name, flush=True)
co = OUT / 'provider'; tr = ROOT / 'vendor/transport'; cx = OUT / 'complex'
py('complex-scalar-and-phase', ROOT / 'code/build-local.py', '--word', ROOT / 'inputs/kernel79.json.gz', '--vendor', tr / 'upstream449', '--routes', tr / 'routes.json.gz', '--clifford', tr / 'clifford_exact.py', '--out', co)
py('complex-normalization', ROOT / 'code/normalize-local.py', '--canonical', co / 'CANONICAL-WORD.json.gz', '--programs', co / 'LOCAL-PROGRAMS.json.gz', '--checks', co / 'LOCAL-CHECKS.json', '--clifford', tr / 'clifford_exact.py', '--out', co)
for ori, c in read(co / 'NORMALIZED-CHECKS.json').items(): assert c['sha256'] == read(tr / 'receipts79/NORMALIZED-CHECKS.json')[ori]['sha256']
cx.mkdir()
py('data-phases', ROOT / 'vendor/complex/complex_phases.py', co / 'CANONICAL-WORD.json.gz', cx / 'DATA-PHASES.json')
sel = ROOT / 'inputs/borrowed79-selection.json'; base = ROOT / 'inputs/complex-controller-base.json.gz'; phase = cx / 'DATA-PHASES.json'; word = co / 'CANONICAL-WORD.json.gz'
local = co / 'SCALAR-FRAME-AUDIT.json'; wrapper = co / 'CANONICAL-WRAPPERS.json'; template = cx / 'GLOBAL-TEMPLATE.json.gz'
py('borrowed-emission', ROOT / 'code/borrowed_emit.py', sel, base, phase, word, local, wrapper, template, co)
py('borrowed-independent', ROOT / 'code/borrowed_audit.py', template, sel, base, phase, word, local, wrapper, cx / 'PHYSICAL-AUDIT.json', co)
py('routes-independent', ROOT / 'code/independent_routes.py', template, phase, cx / 'INDEPENDENT-ROUTES.json')
py('whole-controller', ROOT / 'code/global_controller.py', template, cx / 'PHYSICAL-AUDIT.json', co / 'NORMALIZED-CHECKS.json', phase, cx / 'GLOBAL.json', cx / 'AUDIT.json')
a = read(cx / 'AUDIT.json'); assert a['profile'] == read(ROOT / 'EXPECTED.json')['complex_profile']
(OUT / 'RECEIPT.json').write_text(json.dumps(dict(status='PASS_PR471_COMPLEX_SUPPLIER_UNCHANGED', manifest_sha256=sha(ROOT / 'MANIFEST.json'), manifest_entries_absent=missing,
    complex_template_sha256=read(cx / 'GLOBAL.json')['template_sha256'], python=sys.version.split()[0], steps=steps), indent=2) + '\n')
print('PASS_PR471_COMPLEX_SUPPLIER_UNCHANGED')
