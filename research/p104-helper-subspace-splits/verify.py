"""Verify independent helper splits, all native maps and complete kappa.

Ali Romman with substantial OpenAI Codex assistance. Apache-2.0.
"""
import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha1, sha256
import gzip
import json
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def need(ok, why):
    if not ok:
        raise ValueError(why)


def authenticate():
    count = 0
    manifest = json.loads((HERE/'SOURCES.json').read_bytes())
    for row in manifest['files']:
        if row['usage'] == 'input':
            raw = (ROOT/row['path']).read_bytes()
            need(sha256(raw).hexdigest() == row['sha256'], 'Source SHA256: '+row['path'])
            need(sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == row['git_blob'],
                 'Source Git blob: '+row['path'])
            count += 1
    for row in manifest['external_inputs']:
        retained_path = (HERE.relative_to(ROOT)/row['local_path']).as_posix()
        retained, = [r for r in manifest['files'] if r['path'] == retained_path]
        need(retained['usage'] == 'input', 'Copied source is a declared live input')
        need((retained['sha256'],retained['git_blob']) == (row['sha256'],row['git_blob']),
             'Retained bytes equal the recorded published source')
    return count


def rejected(action):
    try:
        action()
    except ValueError as error:
        return str(error)
    raise ValueError('An invalid claim was accepted')


def run():
    pins = authenticate()
    sys.path.insert(0, str(HERE))
    import local as L
    import construct as R
    import pricing as P
    C = L.load(ROOT/'research/p104-productive-controller/caller.py', 'subspace_p104_caller')
    predecessor_word = L.read(HERE/'inputs/PR5580-WORD.json.gz')
    predecessor = L.replay(predecessor_word)
    cascade = L.replay(L.read(HERE/'inputs/PR5565-WORD.json.gz'))
    source = L.read(HERE/'inputs/PR5601-WORD.json.gz')
    witnesses = L.read(HERE/'SPLITS.json')
    need(len(witnesses) == 9, 'Nine explicit independent splits')
    baseline = L.replay(source)
    source_delta = {}
    for label, before, after, expected in (
            ('PR5565', predecessor, cascade,
             {'paid':{1:-8, 3:-1, 4:-2, 5:4}, 'helpers':{8:-1, 9:1}}),
            ('PR5601', cascade, baseline,
             {'paid':{2:-2, 3:2, 4:-2, 5:1}, 'helpers':{4:1, 5:-1}})):
        source_delta[label] = {}
        for name, profile in expected.items():
            delta = Counter(after[name])
            delta.subtract(before[name])
            source_delta[label][name] = {r:n for r,n in delta.items() if n}
            need(source_delta[label][name] == profile, 'Exact published '+label+' '+name+' change')
    source, relay_receipt = R.merge_relay(predecessor_word, source)
    relay_local = L.replay(source)
    relay_delta = Counter(relay_local['paid'])
    relay_delta.subtract(baseline['paid'])
    need({r:n for r,n in relay_delta.items() if n} == {1:-1,2:-1,3:-1,6:1}, 'Exact published relay paid delta')
    need(relay_local['helpers'] == baseline['helpers'], 'The relay retains every independent target')
    boundaries = L.read(HERE/'BOUNDARIES.json')
    boundary_word, boundary_receipts = R.boundary_changes(
        source, boundaries, L.read(HERE/'inputs/PR5602-WITNESS.json'))
    baseline = L.replay(boundary_word)
    split_word, cuts = R.construct(boundary_word, witnesses)
    split_local = L.replay(split_word)
    delta = Counter(split_local['helpers'])
    delta.subtract(baseline['helpers'])
    delta = {r:n for r,n in delta.items() if n}
    need(delta == {1:2, 2:5, 4:2, 5:2, 7:5, 8:2, 9:-9}, 'All split credits and removed targets')
    need(split_local['paid'] == baseline['paid'], 'Same paid histogram after independent splits')
    preparation = L.read(HERE/'PREPARATION.json')
    word, prepared_receipt = R.prepare_helper(split_word, preparation)
    local = L.replay(word)
    need((local['public_inputs'], local['owned_fields'], local['owned_lifetimes'], local['peak_owned_fields']) == (743,9,11,2),
         'Complete independent input, owned role, lifetime and peak counts')
    need(local['helpers'] == {1:2,2:4,4:91,5:6,7:5,8:16,9:411}, 'Exact final helper histogram with H2 debited')
    prepared_paid = Counter(split_local['paid'])
    prepared_paid[1] -= 2
    need(local['paid'] == prepared_paid, 'Both replaced rank-one Gaussian calls are removed')
    columns = L.reverse_columns(word)
    print('PASS shared relay, 5 boundaries, 9 splits, 2 prepared queries, all rows and columns', flush=True)
    native = L.native(word)
    controller = C.construct()
    need(controller == L.read(ROOT/'research/p104-productive-controller/CONTROLLER.json'), 'Same complete caller')
    physical = C.physical(controller, word)
    print('PASS every native phase, productive target and physical caller contact', flush=True)
    costs = P.run(local, native, controller, physical)
    controls = C.controls(controller)
    bad = deepcopy(witnesses[0])
    key = next(iter(bad['a']))
    bad['a'][key] = str(L.Q(bad['a'][key])+1)
    controls['contaminated_prefix'] = rejected(lambda: R.check_cut(boundary_word, bad))
    bad = deepcopy(witnesses[0])
    key = next(iter(bad['b']))
    bad['b'][key] = str(L.Q(bad['b'][key])+1)
    controls['contaminated_suffix'] = rejected(lambda: R.check_cut(boundary_word, bad))
    bad = deepcopy(boundaries)
    bad[0]['witness']['cut'] += 1
    controls['wrong_boundary_event'] = rejected(lambda: R.boundary_changes(
        source, bad, L.read(HERE/'inputs/PR5602-WITNESS.json')))
    bad = deepcopy(preparation)
    bad['replacements'][0]['suppliers'][1][1] = '-1'
    controls['false_preparation_identity'] = rejected(lambda: R.prepare_helper(split_word, bad))
    bad = deepcopy(word)
    bad['program'].pop(next(i for i,e in enumerate(bad['program']) if e[0] in ('ADD','SCALE')))
    controls['missing_input_basis'] = rejected(lambda: L.replay(bad))
    bad = deepcopy(word)
    bad['program'].pop(max(i for i,e in enumerate(bad['program']) if e[0] in ('ADD','SCALE')))
    controls['missing_output_basis'] = rejected(lambda: L.replay(bad))
    bad = deepcopy(word)
    bad['final'][259] = 127
    controls['unearned_whole_target'] = rejected(lambda: L.replay(bad))
    bad = deepcopy(local)
    bad['helpers'][1] += 1
    controls['extra_helper_credit'] = rejected(lambda: P.assemble(bad, native, controller, physical))
    bad = deepcopy(local)
    bad['helpers'][2] += 1
    controls['unremoved_prepared_target'] = rejected(lambda: P.assemble(bad, native, controller, physical))
    bad = deepcopy(local)
    bad['paid'][1] -= 1
    controls['unpaid_gaussian'] = rejected(lambda: P.assemble(bad, native, controller, physical))
    result = {'status':'PASS_P104_HELPER_SUBSPACE_KAPPA_00310432',
              'authenticated_inputs':pins, 'splits':cuts, 'local_helper_delta':delta,
              'boundaries':boundary_receipts,
              'relay':relay_receipt, 'preparation':prepared_receipt,
              'published_source_delta':source_delta,
              'local':local, 'separate_columns':columns, 'native':native,
              'physical_caller':physical, 'complete_cost':costs, 'negative_controls':controls,
              'limits':['The five selected framework assumptions and helper-endpoint contract remain.',
                        'No complete rounded multiplier or enormous uniform compiler word is materialized.',
                        'No independent human or proof-kernel acceptance or global optimality is claimed.']}
    return P.encode(result), word


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='p104-subspace-bytecode-') as cache:
        sys.pycache_prefix = cache
        result, word = run()
    for name, value in (('RESULT.json', result), ('WORD.json.gz', word)):
        path = HERE/name
        if args.write:
            raw = (json.dumps(value, sort_keys=True, indent=None if name.endswith('.gz') else 2)+'\n').encode()
            path.write_bytes(gzip.compress(raw, mtime=0) if name.endswith('.gz') else raw)
        else:
            raw = path.read_bytes()
            need(json.loads(gzip.decompress(raw) if name.endswith('.gz') else raw) == value,
                 'Exact saved artifact: '+name)
    print(result['status'])
    print(json.dumps({k:result['complete_cost'][k] for k in
                      ('kappa', 'gain', 'raw_root_interval', 'productive_fields', 'paid_calls')}, sort_keys=True))


if __name__ == '__main__':
    main()
