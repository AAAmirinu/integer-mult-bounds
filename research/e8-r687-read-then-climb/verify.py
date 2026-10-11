"""Fresh reconstruction of the R687 E8 bit supplier (READ-THEN-CLIMB phases, coset-split pi-pairings) at eleven stages with
WHOLE-residual hosting (PR #442's rule; no cross-family split, no cross-copy lemma) and target mixing, paired with a verified
complex supplier (PR #442's here; research/e8-r687-tensor-complex composes it with PR #471's).
usage: python -B research/e8-r687-read-then-climb/verify.py /absolute/new/output [--quick] [--discover-check] [--complex-upstream=DIR]
  --quick               skip only PR #443's historical regressions
  --discover-check      recompute the frozen hosting selection with scipy (HiGHS) and require equality
  --certificate         also rerun the exhaustive refutation of the R687 pivot certificate (about 30 min loaded); by default the
                        lower bounds and the witness are recomputed and the pinned refutation log is checked
  --complex-upstream=D  use an already verified complex supplier directory with PR #442's layout (parent/changed, complex/,
                        AUDIT.json, RESULT.json, RECEIPT.json) instead of running PR #442's verifier
needs: Python 3.11+, numpy, mpmath, sympy, scipy (as PR #443/#450); a C++17 compiler (CXX) and Boost headers (BOOST_INCLUDE).
Apache-2.0.  Prepared by DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code."""
from pathlib import Path
import gzip, hashlib, json, os, shutil, subprocess, sys, time
from fractions import Fraction
assert __debug__
ROOT = Path(__file__).resolve().parent; R = ROOT.parent
args = [a for a in sys.argv[1:] if not a.startswith('--')]; flags = {a.split('=')[0]: a.partition('=')[2] for a in sys.argv[1:] if a.startswith('--')}
assert len(args) == 1 and set(flags) <= {'--quick', '--discover-check', '--complex-upstream', '--certificate'}, __doc__
out = Path(args[0]).resolve(); assert not out.exists() and not out.is_relative_to(R)
quick = '--quick' in flags
read = lambda p: json.loads(Path(p).read_text())
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def csha(p):
    w = json.load(gzip.open(p, 'rt') if str(p).endswith('.gz') else open(p))
    return hashlib.sha256(json.dumps(w, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
def inventory(p):
    return {f.relative_to(p).as_posix(): sha(f) for f in sorted(Path(p).rglob('*')) if f.is_file() and '__pycache__' not in f.parts}
def integrity():
    actual = inventory(ROOT); actual.pop('MANIFEST.json')
    assert actual == read(ROOT / 'MANIFEST.json'), 'package manifest differs'
    for name, expected in read(ROOT / 'SOURCE.json')['packages'].items():
        assert inventory(R / name) == expected['files'], ('upstream package differs', name)
integrity(); out.mkdir(parents=True)
PY = sys.executable
CXX = os.environ.get('CXX', 'c++'); BOOST = os.environ.get('BOOST_INCLUDE', '/usr/include')
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONINTMAXSTRDIGITS='0', PYTHON=PY, CXX=CXX, BOOST_INCLUDE=BOOST); env.pop('PYTHONOPTIMIZE', None)
steps = []; (out / 'logs').mkdir()
P443 = R / 'e8-r740-replica32'; P442 = R / 'idle-axis-hosting'; CODE = ROOT / 'code'; D = ROOT / 'data'
BITC = P443 / 'parent436/code/bit'; CK = BITC / 'checkers'; RH = 687
SEL = D / 'selection.json'; ISO = D / 'residual-isometries.json'
K456 = Fraction(1266564732900111, 10 ** 18)   # PR #456 (rohanarun): whole-residual reference used by the assembly label
C715 = Fraction(642564369945714399381, 5 * 10 ** 23)   # R715 bit supplier (research/e8-r715-eleven-stage-whole)
K454 = Fraction(1266536148630310, 10 ** 18)   # PR #454 (chafreaky): target mixing with whole-residual hosting
C454 = Fraction(1275657818793753037875, 10 ** 24)   # PR #454's bit lower endpoint
def run(name, cmd, cwd=None, expect_fail=False, stdout_to=None):
    t = time.monotonic(); log = out / 'logs' / (name + '.log'); print('RUN', name, flush=True)
    with log.open('w') as f, (open(stdout_to, 'w') if stdout_to is not None else f) as g:
        q = subprocess.run(list(map(str, cmd)), cwd=cwd, env=env, stdout=g, stderr=f if stdout_to is not None else subprocess.STDOUT)
    if expect_fail:
        if q.returncode == 0: raise RuntimeError(('negative control accepted', name))
    elif q.returncode: raise RuntimeError((name, q.returncode, log.read_text()[-4000:]))
    steps.append(dict(name=name, seconds=round(time.monotonic() - t, 2), log_sha256=sha(log))); print(('REJECTED' if expect_fail else 'PASS'), name, flush=True)
def py(name, path, *a, **k): run(name, [PY, '-B', path, *a], **k)
try:
    compiler = subprocess.run([CXX, '--version'], capture_output=True, text=True).stdout.splitlines()[0]
    # ---------------- parents: PR #443 (checkers, C++ legality) and the complex supplier (PR #442 layout)
    base = out / 'base443'
    run('parent443', ['bash', P443 / 'verify.sh', *(['--quick'] if quick else []), base])
    bindir = base / 'parent/bin'
    if flags.get('--complex-upstream'):
        up = Path(flags['--complex-upstream']).resolve(); assert (up / 'RESULT.json').exists() and (up / 'complex').is_dir()
    else:
        up = out / 'upstream442'; py('parent442', P442 / 'verify.py', up)
    # ---------------- the word: frozen hierarchy -> PR #370 compile -> PR #443 reuse/retime -> kernel -> mixing
    w = out / 'word'; w.mkdir()
    py('hierarchy-compile', CODE / 'hier_word_rtc.py', R, D / 'hierarchy-r687.json', w / 'raw.json.gz', w / 'reused.json.gz', w / 'word.json.gz', stdout_to=w / 'hierarchy.json')
    assert csha(w / 'word.json.gz') == csha(D / 'word-r687.json.gz'), 'regenerated R687 word differs'
    hj = read(w / 'hierarchy.json'); assert hj['final_R'] == RH and hj['raw_R'] == 811 and hj['compile2']['carriers'] == 240 and hj['compile2']['copies'] == 500 and hj['compile2']['Brules'] == 100
    for mode_ in ('rtc', 'allA'):   # copy anatomy (independent Dilworth recount) and the transversal-cover bound; allA = same DAG with PR #370's phases
        py('copy-bound-' + mode_, CODE / 'copy_bound.py', R, D / 'hierarchy-r687.json', mode_, stdout_to=w / ('copy-bound-%s.json' % mode_))
    cb, cba = read(w / 'copy-bound-rtc.json'), read(w / 'copy-bound-allA.json')
    assert cb['copies'] == hj['compile2']['copies'] == 500 and cb['carriers'] == 240 and cb['transversal_cover_bound'] == 464 and cba['copies'] == 556
    assert cb['by_class']['8/5'] == dict(copies=112, bound=112)
    py('independent-checkword', BITC / 'independent/checkword.py', D / 'word-r687.json.gz', P443 / 'parent436/code/pricing', stdout_to=w / 'checkword.txt')
    assert 'PASS' in (w / 'checkword.txt').read_text()
    py('independent-mutants', BITC / 'independent/mutate.py', D / 'word-r687.json.gz', P443 / 'parent436/code/pricing')
    py('kernel-exact', CODE / 'kernel_exact.py', R, D / 'word-r687.json.gz', D / 'pivot-selection.json', w / 'kernel.json.gz', w / 'kernel-selection.json', w / 'isometries.json', stdout_to=w / 'kernel.json')
    assert len(read(D / 'pivot-selection.json')) == 101 and read(w / 'kernel.json')['entries'] == 100   # the frozen selection: 101 pivots, 100 after parity
    assert csha(w / 'kernel.json.gz') == csha(D / 'word-kernel.json.gz') and read(w / 'kernel-selection.json') == read(D / 'kernel-selection.json') and read(w / 'isometries.json') == read(ISO)
    mx = out / 'mixed'; mx.mkdir()
    py('mix-generate', CODE / 'mix_target.py', D / 'word-kernel.json.gz', mx / 'word-mixed.json', stdout_to=mx / 'mix.json')
    assert csha(mx / 'word-mixed.json') == csha(D / 'word-mixed.json.gz'), 'regenerated mixed word differs'
    for tag, wd in (('kernel', D / 'word-kernel.json.gz'), ('mixed', D / 'word-mixed.json.gz')):   # independent validator's relaxed all-column checker
        py('relaxed-checkword-' + tag, CODE / 'checkword_relaxed.py', wd, P443 / 'parent436/code/pricing', stdout_to=w / ('checkword-relaxed-%s.txt' % tag))
        t_ = (w / ('checkword-relaxed-%s.txt' % tag)).read_text()
        assert 'legality + exact F2 on all %d columns: PASS' % (2 * 120 + RH) in t_ and 'all Gram dets > 0' in t_
    # ---------------- local checks on the mixed word (PR #443 checkers; formal columns at five and eleven stages)
    s11 = out / 'eleven'; (s11 / 'geo/nine').mkdir(parents=True); (s11 / 'bin').mkdir()
    inc = ['-I' + str(P443 / 'parent436/portable-include'), '-I' + str(CK), '-I' + BOOST]
    run('cxx-columns-h', [CXX, '-O2', '-std=c++17', '-DHDIM=8', '-DNCOPY=9', '-DVPORTS=120', '-DRHELP=%d' % RH, *inc, '-o', s11 / 'bin/columns_h', CK / 'columns_h.cpp'])
    run('cxx-columns-k5', [CXX, '-O2', '-std=c++17', '-DHDIM=8', '-DNCOPY=9', '-DVPORTS=120', '-DRHELP=%d' % RH, '-DKPAIRS=5', *inc, '-o', s11 / 'bin/columns_k5', CK / 'columns_k.cpp'])
    py('mixed-export', BITC / 'export_records.py', mx / 'word-mixed.json', mx / 'records')
    py('mixed-stage-cohort', BITC / 'regression/stage_cohort.py', mx / 'records', mx / 'records', mx / 'cin', mx / 'cout')
    run('mixed-legality', [bindir / 'legality', mx / 'cin', mx / 'cout', mx / 'cout/legality.json'], stdout_to=mx / 'cout/legality.log')
    run('mixed-columns-h', [s11 / 'bin/columns_h', mx / 'cout/COHORT249-RECORDS.bin', mx / 'cout/columns.json'], stdout_to=mx / 'cout/columns.log')
    l, c = read(mx / 'cout/legality.json'), read(mx / 'cout/columns.json')
    assert l['status'] == 'PASS_INDEPENDENT_COHORT_LEGALITY_SOURCE_OWNERS_AND_LIFECYCLE' and l['copies'] == l['erasures'] == 9
    assert c['status'] == 'PASS_NEW_COHORT249_ALL_FIVE_STAGE_FORMAL_COLUMNS_AND_PREFIX_BILL' and c['formal_columns_checked'] == 4 * 120 + RH
    run('mixed-columns-k5', [s11 / 'bin/columns_k5', mx / 'cout/COHORT249-RECORDS.bin', mx / 'cout/columns_k5.json'], stdout_to=mx / 'cout/columns_k5.log')
    k = read(mx / 'cout/columns_k5.json')
    assert k['status'] == 'PASS_NEW_COHORT249_ALL_BRIDGED_STAGE_FORMAL_COLUMNS_AND_PREFIX_BILL' and k['formal_columns_checked'] == 10 * 120 + RH
    assert k['bridge_additions'] == 24 * 120 and len(k['stages']) == 11 and all(x['rejected'] for x in k['negative_controls'])
    py('mixed-mutate-records', BITC / 'mutate_records.py', mx / 'records', mx / 'cin', mx / 'cout', bindir / 'legality', s11 / 'bin/columns_k5', bindir / 'legality_ncopy_h')
    py('mix-check', CODE / 'mix_check.py', mx / 'word-mixed.json', mx / 'records', '--controls', D / 'word-kernel.json.gz', stdout_to=mx / 'mix-check.json')
    mc = read(mx / 'mix-check.json'); assert mc['status'] == 'PASS' and set(mc['mutation_controls'].values()) == {'REJECTED'} and len(mc['mutation_controls']) == 4
    run('mixed-gram', [PY, '-I', '-B', CK / 'gram_frames.py', mx / 'records', '--gram', 'e8ham', '--h', 8, '--positive'])
    # ---------------- eleven stages: geometry -> parent template -> audit -> whole-residual hosting -> audit -> assembly
    py('geometry-eleven', CODE / 'geometry_k.py', '--source', P443 / 'parent436', '--out', s11 / 'geo/nine', '--stages', 11, '--no-timing')
    geo = read(s11 / 'geo/nine/GEOMETRY.json')
    assert (geo['m'], geo['stages'], geo['route_checks'], geo['max_route_factors'], geo['route_denominators'], geo['bad_prime_factors']) == (78, 11, 1320, 77, [1, 2, 4], [2])
    v = s11 / 'mixed_d3'; (v / 'nine').mkdir(parents=True); shutil.copy(s11 / 'geo/nine/GEOMETRY.json', v / 'nine/GEOMETRY.json')
    (v / 'records').symlink_to(mx / 'records', target_is_directory=True)
    py('global', CODE / 'global_k.py', '--word', mx / 'word-mixed.json', '--local-check', mx, '--out', v / 'nine', '--isometries', ISO, '--stages', 11, '--replicas', 1, '--no-banks')
    py('parent-audit', CODE / 'audit_parent_k.py', '--local-check', mx, '--out', v / 'nine', '--word', mx / 'word-mixed.json')
    if '--discover-check' in flags:
        sel = v / 'selection-recomputed.json'
        py('discover', CODE / 'emit_k.py', v / 'nine', mx, v / 'hosted-discover', '--selection', sel, '--key', 'bit11_d3', '--discover', '--host-all', '--depth', 3, '--version-tag', 'e8-eleven-stage-idle-hosting-v1')
        assert read(sel)['bit11_d3'] == read(SEL)['bit11_d3'], 'frozen hosting selection differs from the recomputed optimum'
    py('emit', CODE / 'emit_k.py', v / 'nine', mx, v / 'hosted', '--selection', SEL, '--key', 'bit11_d3', '--host-all', '--depth', 3, '--version-tag', 'e8-eleven-stage-idle-hosting-v1')
    py('hosted-audit', CODE / 'audit_hosted_k.py', v, v / 'hosted', v / 'hosted/AUDIT.json')
    py('assembly', CODE / 'assemble_k.py', v, up, v / 'hosted', v / 'hosted/AUDIT.json', v / 'RESULT.json', '--parent-kappa', '%d/%d' % (K456.numerator, K456.denominator), '--label', '#456')
    res = read(v / 'RESULT.json')
    got = dict(kappa=res['kappa'], bit_lower=res['bit_lower'], complex_lower=res['complex_lower'], binding_component=res['binding_component'],
               bit_only_kappa=res['bit_only_kappa'], bit=res['bit'], bit_profile=res['bit_profile'], halving_depth=res['halving_depth'],
               external_row_allowance=res['external_row_allowance'], strict_constraints=len(res['strict_outer_constraints']), outer_controls=res['outer_controls'],
               bit_template_sha256=res['bit_template_sha256'], emitted_program_sha256=res['emitted_program_sha256'],
               bit_c_gain_over_pr454_percent=float(100 * (Fraction(res['bit_lower']) / C454 - 1)), bit_c_gain_over_r715_percent=float(100 * (Fraction(res['bit_lower']) / C715 - 1)),
               kappa_gain_over_pr456_percent=float(100 * (Fraction(res['kappa']) / K456 - 1)))
    checks = dict(word_sha256=csha(D / 'word-r687.json.gz'), hierarchy=hj, copy_bound=cb, copy_bound_allA_phases=dict(copies=cba['copies'], chi_histogram=cba['chi_histogram']), kernel=read(w / 'kernel.json'), mix=read(mx / 'mix.json'), mixed_word_sha256=csha(D / 'word-mixed.json.gz'),
                  columns_k5_formal=k['formal_columns_checked'], mixed_local_profile=mc['profile'], mixed_local_cost_per_call=mc['local_cost_per_call'])
    record = bool(os.environ.get('E8R687_RECORD'))
    complex_tag = 'pr442' if not flags.get('--complex-upstream') else 'external'
    if record:
        (out / 'EXPECTED.recorded.json').write_text(json.dumps(dict(status='PASS_R687_READ_THEN_CLIMB_ELEVEN_STAGE_WHOLE_RESIDUAL', variants={complex_tag: got}, checks=checks), indent=2, sort_keys=True) + '\n')
    else:
        e = read(ROOT / 'EXPECTED.json')
        assert checks == e['checks'], 'checks differ from EXPECTED'
        ev = e['variants']['pr442']   # the bit supplier's own fields do not depend on the complex upstream: always compared
        for kk in ('bit_lower', 'bit', 'bit_profile', 'bit_template_sha256', 'emitted_program_sha256', 'halving_depth', 'strict_constraints', 'external_row_allowance'):
            assert got[kk] == ev[kk], (kk, got[kk], ev[kk])
        if complex_tag in e['variants']:
            for kk, vv in e['variants'][complex_tag].items(): assert got[kk] == vv, (kk, got[kk], vv)
    # ---------------- R715 copy anatomy on its own pinned hierarchy (PR #370 phases)
    py('copy-bound-r715', CODE / 'copy_bound.py', R, R / 'e8-r715-eleven-stage-whole/data/hierarchy-r715.json', 'allA', stdout_to=w / 'copy-bound-r715.json')
    c715 = read(w / 'copy-bound-r715.json'); assert c715['copies'] == 528 and c715['carriers'] == 240 and c715['transversal_cover_bound'] == 492
    # ---------------- exact pivot maximum on R687 (matroid min-sum-rank list partition; README 'Exact kernel pivots')
    pv = w / 'pivot-data-r687.json'; pc = w / 'pivot-comps-r687.json'
    py('pivot-data-r687', CODE / 'pivot_data.py', R, D / 'word-r687.json.gz', pv, pc, stdout_to=w / 'pivot-data-r687.out')
    py('pivot-bounds-r687', CODE / 'exactgen.py', pv, pc, 1, 'lb', stdout_to=w / 'pivot-bounds-r687.txt')
    cert = json.loads((w / 'pivot-bounds-r687.txt').read_text().split('CERT ')[1])
    assert [(x['size'], x.get('LB'), x['min_sumrank']) for x in cert['components']] == [(190, 111, None), (26, None, 11), (12, None, 4)] and cert['upper_bound'] == 102
    comps = read(pc); sel = read(D / 'pivot-selection.json'); cid = {h: i for i, c in enumerate(comps) for h in c}
    per = [sum(1 for E_, p_, D_ in sel if cid[p_] == i) for i in range(3)]
    assert per == [190 - 112, 26 - 11, 12 - 4] and len(sel) == 101   # the frozen selection is a witness: sum-rank LB + 1 = 112 on the big component
    pin = (D / 'pivot-certificate-r687.txt').read_text()   # pinned exhaustive run: sum-rank 111 refuted (complete: slack 0 <= MAXSLACK 1)
    assert 'LB sumrank 111' in pin and 'total sumrank <= 111 attainable: False' in pin and 'total sumrank <= 112 attainable: True' in pin and 'TOTAL max pivots (exact, rank-1 axis-class model) 101' in pin
    piv = dict(r687=101, upper_bound_recomputed=cert['upper_bound'], witness=len(sel), refutation='pinned log' if '--certificate' not in flags else 'recomputed')
    if '--certificate' in flags:   # the exhaustive refutation itself (about 30 min on a loaded 12-core machine)
        py('pivot-exact-r687', CODE / 'exactgen.py', pv, pc, 1, stdout_to=w / 'pivot-exact-r687.txt')
        t_ = (w / 'pivot-exact-r687.txt').read_text(); full = json.loads(t_.split('CERT ')[1])
        assert full['max_pivots'] == 101 and all(x.get('complete', True) for x in full['components'])
        strip = lambda txt: [l.split('  [')[0] for l in txt.splitlines() if not l.startswith('CERT')]
        assert strip(t_) == strip(pin), 'recomputed certificate differs from the pinned log'
    integrity()
    receipt = dict(status='PASS_R687_READ_THEN_CLIMB_ELEVEN_STAGE_WHOLE_RESIDUAL', mode='quick' if quick else 'full', exact_pivot_maximum=piv, copy_bound_r715=dict(copies=c715['copies'], bound=c715['transversal_cover_bound']), complex=complex_tag, kappa=res['kappa'], kappa_decimal=res['kappa_decimal'],
                   bit_lower=res['bit_lower'], complex_lower=res['complex_lower'], binding_component=res['binding_component'], bit_only_kappa=res['bit_only_kappa'],
                   bit_c_gain_over_pr454_percent=got['bit_c_gain_over_pr454_percent'], bit_c_gain_over_r715_percent=got['bit_c_gain_over_r715_percent'], kappa_gain_over_pr456_percent=got['kappa_gain_over_pr456_percent'],
                   manifest_sha256=sha(ROOT / 'MANIFEST.json'), source_sha256=sha(ROOT / 'SOURCE.json'), compiler=compiler, python=sys.version.split()[0], checks=steps)
    (out / 'RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({kk: receipt[kk] for kk in ('status', 'complex', 'kappa', 'kappa_decimal', 'bit_lower', 'binding_component', 'bit_c_gain_over_r715_percent', 'kappa_gain_over_pr456_percent')}, indent=2))
except BaseException as e:
    (out / 'FAILURE.json').write_text(json.dumps(dict(error=repr(e), completed=steps), indent=2) + '\n'); raise
