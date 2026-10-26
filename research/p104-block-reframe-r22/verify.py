"""Check the R22 reorder+reframe word on PR5751's P104 word on PR5751's own complete stack.

Joel Pulikkan (GamingPuzzled) with Claude Opus 5.5 (Anthropic) via Claude Code. Apache-2.0.
Every retained checker is loaded unmodified from ../p104-paid-meeting-splits (Ali Romman, flyingviper, zxv and
the contributors listed in its NOTICE); only the four declared pricing literals change.
"""
from collections import Counter, defaultdict
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse, gzip, importlib.util, json, sys, tempfile
from contextlib import ExitStack

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = HERE.parent/'p104-paid-meeting-splits'
sys.path.insert(0, str(HERE))
from construct import construct

PINS = {   # PR5751 head 8483f9a679d06c1e270141dbc686a7e76e7a7522
    'WORD.json.gz': 'fb60e34238a57a147f53aadb1af1209a562e2dcd18b05a29557df452cfe83133',
    'local.py': 'fc7c7293f7cffb8a9074e65b926e1782f2ebce2991c9ea75d42b94e888052689',
}
PUBLIC = 767
PARENT_KAPPA = Q('.00311301600')
LITERALS = [
    ("KAPPA, TESTED = Q('.00311301600'), Q('.003113016005')", "KAPPA, TESTED = Q('.00311313795'), Q('.003113137955')"),
    ("PREVIOUS = Q('.00311024570')", "PREVIOUS = Q('.00311301600')"),
    ("sum(paid.values()) == 66834", "sum(paid.values()) == 66852"),
    ("'kappa_decimal':'0.00311301600'", "'kappa_decimal':'0.00311313795'"),
]
STATUS = 'PASS_P104_R22_REFRAME_KAPPA_00311313795'


def need(ok, why):
    if not ok:
        raise ValueError(why)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module
    spec.loader.exec_module(module); return module


def read(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)


def kinds(e):
    """(register, type) per touched register; T/T and S/S commute exactly, everything else conflicts.
    Owned registers keep every operation exclusive; INIT/CLEAR also share the owned-lifetime token."""
    op = e[0]
    if op == 'ADD':
        out = [(e[1], 'T'), (e[2], 'S')]
    elif op == 'COPY':
        out = [(e[1], 'X'), (e[2], 'S')]
    elif op in ('INIT', 'CLEAR'):
        return [(e[1], 'X'), ('owned-lifetime', 'X')]
    else:
        out = [(e[1], 'X')]
    return [(r, 'X' if r >= PUBLIC else t) for r, t in out]


def strip(e):
    return tuple(e[:2]) if e[0] in ('INIT', 'CLEAR') else tuple(e[:-1])


def trace_equivalent(old, new):
    """Every scalar/owned operation appears once more; every dependent pair keeps its order."""
    need(Counter(map(strip, old)) == Counter(map(strip, new)), 'Same multiset of scalar and owned operations')
    slots = defaultdict(list)
    for j, e in enumerate(new):
        slots[strip(e)].append(j)
    for v in slots.values():
        v.reverse()
    match = [slots[strip(e)].pop() for e in old]
    groups = defaultdict(list)
    for i, e in enumerate(old):
        for r, t in kinds(e):
            g = groups[r]
            if g and g[-1][0] == t and t != 'X':
                g[-1][1].append(i)
            else:
                g.append([t, [i]])
    for g in groups.values():
        for (_, a), (_, b) in zip(g, g[1:]):
            need(max(match[i] for i in a) < min(match[i] for i in b), 'Dependent operations keep their order')
    return match


def changes(a, b):
    d = Counter(a); d.subtract(b); return {str(r): c for r, c in sorted(d.items()) if c}


def reject(f):
    try:
        f()
    except (ValueError, AssertionError, KeyError, IndexError) as e:
        return str(e) or type(e).__name__
    raise ValueError('Malformed control accepted')


def run():
    for name, digest in PINS.items():
        need(sha256((BASE/name).read_bytes()).hexdigest() == digest, 'Exact PR5751 source ' + name)
    base, word = read(BASE/'WORD.json.gz'), read(HERE/'WORD.json.gz')
    need(construct(base) == word, 'Exact regeneration from PR5751')
    for key in base:
        if key not in ('program', 'initial', 'final', 'frames', 'schema'):
            need(word[key] == base[key], 'Unchanged word field ' + key)
    need(word['frames'][:len(base['frames'])] == base['frames'], 'Existing charts unchanged')
    starts = {str(r): [a, b] for r, (a, b) in enumerate(zip(base['initial'], word['initial'])) if a != b}
    finals = {str(r): [a, b] for r, (a, b) in enumerate(zip(base['final'], word['final'])) if a != b}
    need(starts == {'741': [477, 1090]} and finals == {'405': [477, 1090]}, 'Exact changed helper endpoints')
    main = set(base['live']) | {r + 112 for r in base['live']}
    need(all(int(r) not in main for r in list(starts) + list(finals)), 'Only free helper endpoints change')
    scalar = lambda w: [e for e in w['program'] if e[0] != 'MOVE']
    match = trace_equivalent(scalar(base), scalar(word))
    old = scalar(base)
    charts = [[i, old[i][:-1], old[i][-1], scalar(word)[match[i]][-1]] for i in range(len(old))
              if scalar(word)[match[i]] != old[i]]
    print('PASS source pin, regeneration, trace equivalence; changed charts', charts, flush=True)

    sys.path.insert(0, str(BASE))
    S = load(BASE/'sources.py', 'r22_sources')
    original = (BASE/'pricing.py').read_text()
    for before, after in LITERALS:
        need(original.count(before) == 1, 'Unique pricing literal ' + before); original = original.replace(before, after)
    need((HERE/'pricing.py').read_text() == original, 'Only declared pricing literals change')
    with ExitStack() as contexts:
        cursor, _ = contexts.enter_context(S.sources())
        for depth in range(4):   # PR5751's own source chain; its local.py is pinned above
            cursor, framework = contexts.enter_context(load(cursor/'sources.py', 'r22_sources_%d' % depth).sources())
        L = load(BASE/'local.py', 'local')
        L.ROOT = framework
        parent_local, local = L.replay(base), L.replay(word)
        need(parent_local['real_scalar_allowance'] == local['real_scalar_allowance'], 'Same scalar allowance')
        paid_delta = changes(local['paid'], parent_local['paid'])
        helper_delta = changes(local['helpers'], parent_local['helpers'])
        need(paid_delta == {'1': 1, '4': 1, '5': -1} and helper_delta == {'1': -1, '4': 1, '5': 1, '8': -1},
             'Exact local invoice change')
        print('PASS exact local replay', local['paid'], local['helpers'], flush=True)
        transpose = L.reverse_columns(word)
        print('PASS every dense transpose column', transpose['columns'], flush=True)
        native = L.native(word)
        print('PASS every native map and exact phase', native['distinct_maps'], flush=True)
        C = load(framework/'research/p104-productive-controller/caller.py', 'r22_caller')
        caller = C.construct()
        need(caller == read(framework/'research/p104-productive-controller/CONTROLLER.json'), 'Exact retained caller')
        physical = C.physical(caller, word)
        print('PASS full physical caller', flush=True)
        P = load(HERE/'pricing.py', 'r22_pricing')
        price = P.run(local, native, caller, physical)
        print('PASS complete pricing', price['raw_root_interval'], flush=True)
        lo = Q(price['raw_root_interval'][0])
        need(lo > PARENT_KAPPA, 'Strict raw gain over PR5751 claim')
        controls = {}
        bad = deepcopy(word); bad['initial'][741] = 477
        controls['old_helper_start'] = reject(lambda: L.replay(bad))
        bad = deepcopy(word); i = bad['program'].index(['ADD', 42, 41, '1', 1090]); bad['program'][i][-1] = 477
        controls['block_op_on_old_chart'] = reject(lambda: L.replay(bad))
        bad = deepcopy(word); i = next(k for k, e in enumerate(bad['program']) if e[0] == 'MOVE' and e[3] == 1090)
        bad['program'].pop(i)
        controls['missing_block_move'] = reject(lambda: L.replay(bad))
        bad = deepcopy(local); bad['paid'][1] -= 1
        controls['unpaid_query'] = reject(lambda: P.assemble(bad, native, caller, physical))
        bad = deepcopy(local); bad['helpers'][9] += 1
        controls['extra_target_credit'] = reject(lambda: P.assemble(bad, native, caller, physical))
        bad = scalar(word)
        i, j = bad.index(['ADD', 42, 41, '1', 1090]), bad.index(['ADD', 41, 42, '-1', 1090])
        bad[i], bad[j] = bad[j], bad[i]
        controls['read_after_write'] = reject(lambda: trace_equivalent(scalar(base), bad))
    return P.encode({'status': STATUS, 'source': {'pr5751': '8483f9a679d06c1e270141dbc686a7e76e7a7522'},
                     'helper_starts': starts, 'helper_finals': finals, 'changed_charts': charts, 'local': local,
                     'local_paid_delta': paid_delta, 'helper_credit_delta': helper_delta,
                     'global_paid_delta': {r: 18*n for r, n in paid_delta.items()},
                     'transpose': transpose, 'native': native, 'physical': physical,
                     'complete_cost': price, 'controls': controls})


def main():
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    with tempfile.TemporaryDirectory(prefix='p104-r22-bytecode-') as cache:
        sys.pycache_prefix = cache; result = run()
    target = HERE/'RESULT.json'
    if args.write:
        target.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    else:
        need(read(target) == result, 'Exact saved complete receipt')
    print(result['status'], flush=True)


if __name__ == '__main__':
    main()
