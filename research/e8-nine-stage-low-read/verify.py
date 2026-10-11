#!/usr/bin/env python3
"""Compose PR379's local schedule with PR381's nine-stage layout.
Prepared with OpenAI Codex assistance; Apache-2.0. Assertions must stay enabled.
"""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import argparse, gzip, hashlib, json, os, subprocess, sys, tarfile
ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, value): p.write_text(json.dumps(value, indent=2, default=str) + '\n')
def integrity():
    manifest = read(ROOT / 'MANIFEST.json')
    assert {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()} == set(manifest) | {'MANIFEST.json'}
    for name, digest in manifest.items(): assert sha(ROOT / name) == digest, name
    sources = read(ROOT / 'SOURCES.json')
    assert sha(ROOT / 'source381/MANIFEST.sha256') == sources['baseline']['manifest_sha256']
    assert sha(ROOT / 'candidate379.tar.gz') == sources['candidate']['sha256']
def extract(destination):
    destination.mkdir()
    with tarfile.open(ROOT / 'candidate379.tar.gz', 'r:gz') as archive:
        seen = set()
        for item in archive.getmembers():
            target = (destination / item.name).resolve()
            assert destination in target.parents and item.isfile() and target not in seen, item.name
            seen.add(target); target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.extractfile(item).read())
    for line in (destination / 'MANIFEST.sha256').read_text().splitlines():
        digest, name = line.split(None, 1)
        assert sha(destination / name.strip()) == digest, name

def main():
    assert __debug__, 'Keep assertions enabled'
    ap = argparse.ArgumentParser(); ap.add_argument('output', type=Path); ap.add_argument('--boost-include', type=Path)
    args = ap.parse_args(); out = args.output.resolve()
    assert out != ROOT and ROOT not in out.parents and not out.exists()
    integrity(); out.mkdir(parents=True); (out / 'tmp').mkdir()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(out / 'tmp'), VERIFY_PYTHON=sys.executable,
               SOURCE381=str(ROOT / 'source381'), CX_RECORD=str(out / 'unexpected-record.json'))
    includes = [str(args.boost_include)] if args.boost_include else []
    if sys.platform == 'darwin': includes.insert(0, str(ROOT / 'support'))
    if env.get('CPLUS_INCLUDE_PATH'): includes.append(env['CPLUS_INCLUDE_PATH'])
    if includes: env['CPLUS_INCLUDE_PATH'] = os.pathsep.join(includes)
    def run(argv, log):
        print('RUN', log, flush=True)
        with (out / log).open('w') as f:
            subprocess.run(list(map(str, argv)), cwd=out, env=env, stdout=f, stderr=subprocess.STDOUT, check=True)
    def py(script, *a): return [sys.executable, '-B', script, *a]
    # Only shell path/interpreter handling changes; every baseline scientific
    # command, comparison and negative control executes as originally supplied.
    script = (ROOT / 'source381/verify.sh').read_text(); old = 'HERE=$(cd "$(dirname "$0")" && pwd)'
    assert script.count(old) == 1 and script.count('PY="python3 -B"') == 1
    script = script.replace(old, 'HERE=$SOURCE381').replace('set -euo pipefail', "set -euo pipefail\nIFS=$'\\n\\t'")
    script = script.replace('PY="python3 -B"', 'PY=py; py() { "$VERIFY_PYTHON" -B "$@"; }')
    (out / 'baseline.sh').write_text(script)
    run(['bash', out / 'baseline.sh', out / 'baseline'], 'baseline.log')
    assert not (out / 'unexpected-record.json').exists()
    baseline = read(out / 'baseline/kappa.json'); sources = read(ROOT / 'SOURCES.json')
    assert baseline['kappa'] == sources['baseline']['kappa']
    complex_receipt = read(out / 'baseline/complex377/VERIFICATION.json')
    assert complex_receipt['status'] == 'PASS_PORTABLE_NINE_STAGE_COMPLEX_FINITE_COMPONENT'
    assert len(complex_receipt['fresh_stages']) == 8 and all(x['returncode'] == 0 for x in complex_receipt['fresh_stages'])
    candidate = out / 'candidate-source'; extract(candidate)
    run(py(candidate / 'verify.py'), 'producer-operator.log')
    local = read(candidate / 'RESULT.json')
    assert local['status'] == 'PASS_SOURCE_REPLAY_OPERATOR_EQUALITY_AND_EXACT_PAID_MOMENT'
    load_word = lambda p: json.loads(gzip.decompress(p.read_bytes()))
    assert load_word(candidate / 'baseline-word.json.gz') == load_word(ROOT / 'source381/data/bit/bitE8-r865.json.gz')
    word = candidate / 'candidate-word.json.gz'; bit = ROOT / 'source381/code/bit'; ck = bit / 'checkers'
    rec = out / 'candidate-records'; cin = out / 'cin'; cout = out / 'cout'; bins = out / 'baseline/bin'
    run(py(bit / 'independent/checkword.py', word, ROOT / 'source381/code/pricing'), 'local-columns.log')
    run(py(bit / 'independent/mutate.py', word, ROOT / 'source381/code/pricing'), 'local-negative-controls.log')
    run(py(bit / 'export_records.py', word, rec), 'records.log')
    run(py(bit / 'regression/stage_cohort.py', rec, rec, cin, cout), 'stage-cohort.log')
    run([bins / 'legality', cin, cout, out / 'legality.json'], 'legality.log')
    run([bins / 'columns_k4', cout / 'COHORT249-RECORDS.bin', out / 'columns.json'], 'global-columns.log')
    columns = read(out / 'columns.json')
    assert columns['status'] == 'PASS_NEW_COHORT249_ALL_BRIDGED_STAGE_FORMAL_COLUMNS_AND_PREFIX_BILL'
    assert columns['formal_columns_checked'] == columns['global_live_registers'] == 1825
    assert len(columns['stages']) == 9 and [s['signed_inverse'] for s in columns['stages']] == [False, True, False, True, False, True, False, True, False]
    assert columns['bridge_additions'] == 18 * 120 and columns['fresh_center_copies'] == 81
    assert len(columns['negative_controls']) == 18 and all(x['rejected'] for x in columns['negative_controls'])
    run(py(bit / 'mutate_records.py', rec, cin, cout, bins / 'legality', bins / 'columns_k4', bins / 'legality_ncopy_h'), 'record-negative-controls.log')
    run(py(ck / 'gram_frames.py', rec, '--gram', 'e8ham', '--h', 8, '--positive'), 'gram.log')
    run(py(ck / 'geometry_k.py', 4, word, 'unsplit'), 'geometry.log')
    run(py(ck / 'tile_k.py', rec, 4, 8, 9), 'banks.log')
    run(py(ck / 'certify_bit_k.py', rec, complex_receipt['complex_coarse'], 4, 8, 9, out / 'kappa.json', 'unsplit'), 'pricing.log')
    k = read(out / 'kappa.json'); k.pop('word'); assert k == read(ROOT / 'EXPECTED.json')
    for key in ('m', 'W', 'T', 'maxchild', 'halving_degree', 'idle_blocks_per_role_pair', 'complex_coarse'):
        assert k[key] == baseline[key], key
    before = Counter({int(r): n for r, n in baseline['normalized_histogram'].items()})
    after = Counter({int(r): n for r, n in k['normalized_histogram'].items()})
    delta = {r: after[r] - before[r] for r in sorted(before.keys() | after.keys()) if before[r] != after[r]}
    local_delta = {int(r): n for r, n in local['delta_steps'].items()}
    assert delta == {r: 81*n for r, n in local_delta.items()} == {1: 1620, 2: -972, 3: 486, 4: -2268, 7: 1134}
    # For f(r)=r^p, 0<p<1, each bracket is strictly negative. This is
    # an analytic strict-improvement certificate, independent of root rounding.
    weights = {2: 20, 3: 28, 4: 42, 5: 28, 6: 14}; expanded = Counter()
    for center, weight in weights.items():
        assert weight > 0
        expanded[center-1] += weight; expanded[center] -= 2*weight; expanded[center+1] += weight
    assert {r: n for r, n in expanded.items() if n} == local_delta
    calls = sum(after.values()); mass = sum(r*n for r, n in after.items())
    assert calls == sum(before.values()) == 362772 and mass == sum(r*n for r, n in before.items()) == 1179792
    assert k['m'] * k['W'] - mass == 2808
    write(out / 'strict-concavity.json', dict(normalized_histogram_delta=delta, local_second_difference_weights=weights,
        multiplier=81, calls=calls, rank_mass=mass, deficit=2808, identical_fallback=True,
        proof='For 0<p<1, strict concavity gives f(j-1)-2f(j)+f(j+1)<0. Positive weighted sum equals the local profile change; multiply by 81.'))
    run(py(bit / 'receipts_k.py', word, rec, out / 'legality.json', out / 'columns.json', out / 'kappa.json', out / 'finite-input.json'), 'finite-input.log')
    run(py(ck / 'finite_k.py', 'e8', out / 'finite-input.json', out / 'finite.json'), 'finite.log')
    finite = read(out / 'finite.json'); row = finite['row_reserve']
    assert row['halving_degree'] == 2 and row['internal_coefficient'] == 2*(72*72+1)
    kappa = Q(k['kappa']); compare = Q(baseline['kappa']); assert kappa > compare and k['binding'] == 'bit'
    integrity()
    result = dict(status='PASS_NINE_STAGE_LOW_READ_COMPOSITION', kappa=str(kappa), bit_coarse=k['bit_coarse'],
        complex_coarse=k['complex_coarse'], binding=k['binding'], comparison_pr381=str(compare), gain_percent=float(100*(kappa/compare-1)),
        formal_columns=columns['formal_columns_checked'], stages=len(columns['stages']), omitted_bridge_controls=18,
        record_negative_controls=6, complex_fresh_stages=8, outer_strict_constraints=47, strict_concavity_identity=True,
        candidate_word_sha256=sha(word), scope='Conditional on PR381 and PR379 source interfaces, including signed integer lifting and the nine-stage Clifford/window/bank/common-grid/analytic interfaces; no new Lean proof.')
    write(out / 'RESULT.json', result); print(json.dumps(result, indent=2), flush=True)
if __name__ == '__main__': main()
