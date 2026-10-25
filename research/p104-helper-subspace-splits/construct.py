"""Split independent helper jobs with three scalar basis changes.

Ali Romman with substantial OpenAI Codex assistance. Apache-2.0.
The source word and caller retain the credits in README.md.
"""
from copy import deepcopy
from collections import Counter
from difflib import SequenceMatcher
from fractions import Fraction as Q
import local as L


def merge_relay(original, changed):
    """Merge disjoint published edits against their common PR5580 source."""
    C = L.load(L.HERE/'inputs/PR5605-construct.py', 'released_relay_constructor')
    relay = C.construct(original)
    L.need(all(relay[k] == original[k] for k in original if k != 'program'),
           'The relay changes only the scalar program and transports')

    def edits(word):
        a = [tuple(e) for e in original['program']]
        b = [tuple(e) for e in word['program']]
        return [(i,j,word['program'][u:v]) for op,i,j,u,v in
                SequenceMatcher(None,a,b,autojunk=False).get_opcodes() if op != 'equal']

    frame_edits, relay_edits = edits(changed), edits(relay)
    for i,j,_ in frame_edits:
        for u,v,_ in relay_edits:
            L.need(not (max(i,u) < min(j,v) or (i == j and u <= i <= v) or
                        (u == v and i <= u <= j)), 'Disjoint exact source edits')
    word, program, start = deepcopy(changed), [], 0
    for i,j,events in sorted(frame_edits+relay_edits):
        L.need(start <= i, 'Ordered nonoverlapping source edits')
        program += original['program'][start:i]+events
        start = j
    word['program'] = deepcopy(program+original['program'][start:])
    L.replay(word)
    return word, {'frame_edits':len(frame_edits), 'relay_edits':len(relay_edits)}


def prepare_helper(source, declaration):
    """Reuse PR5606's two exact value identities and remove the H2 target."""
    n, h = source['public'], declaration['helper']
    L.need(n == 744 and source.get('owned_fields', 8) == 8, 'Complete pre-preparation interface')
    L.need(h == 573 and source['initial'][h] == 3 and source['final'][h] == 603,
           'The declared rank-two prefix helper')
    L.need(len(source['frames'][603])-len(source['frames'][3]) == 2, 'Debited target rank')
    L.need(h > max(set(source['live']) | {r+112 for r in source['live']}), 'Main roles retain their labels')
    sites = {item['event']:item for item in declaration['replacements']}
    L.need(len(sites) == 2, 'Two prepared query sites')
    rows = [{r:Q(1)} if r < n and r != h else {} for r in range(n+8)]
    current = source['initial']+[None]*8
    program, receipts = [['INIT',h,3]], []
    for i,e in enumerate(source['program']):
        op,r = e[:2]
        if i in sites:
            item = sites[i]
            L.need(e == item['old'] and op == 'MOVE' and r == h and not e[4], 'Exact prepared paid site')
            target = {}
            for s,q in item['suppliers']:
                L.need(current[s] == e[3], 'Coframed preparation supplier')
                L.add(target,rows[s],Q(q))
            L.need(target == rows[h], 'Exact current-value preparation identity')
            a,b = item['suppliers']
            program += [['CLEAR',h,e[2]],['INIT',h,e[3]],
                        ['COPY',h,a[0],a[1],e[3]],['ADD',h,b[0],b[1],e[3]]]
            current[h] = e[3]
            receipts.append({'event':i, 'rank':len(source['frames'][e[3]])-len(source['frames'][e[2]])})
            continue
        program.append(e[:])
        if op == 'MOVE':
            current[r] = e[3]
        elif op in ('INIT','CLEAR'):
            rows[r] = {}
            current[r] = e[2] if op == 'INIT' else None
        elif op == 'SCALE':
            rows[r] = {k:Q(e[-2])*v for k,v in rows[r].items()}
        elif op == 'COPY':
            rows[r] = {k:Q(e[-2])*v for k,v in rows[e[2]].items()}
        else:
            L.add(rows[r],rows[e[2]],Q(e[-2]))
    L.need(len(receipts) == 2 and all(x['rank'] == 1 for x in receipts) and not rows[h],
           'Two rank-one queries removed and a zero final helper')
    program.append(['CLEAR',h,603])

    def rename(r):
        return n+7 if r == h else r-int(r > h)

    for e in program:
        e[1] = rename(e[1])
        if e[0] in ('ADD','COPY'):
            e[2] = rename(e[2])
    word = deepcopy(source)
    word.update(schema='p104-helper-subspace-prepared/1', public=n-1, owned_fields=9,
                initial=source['initial'][:h]+source['initial'][h+1:],
                final=source['final'][:h]+source['final'][h+1:], program=program)
    L.replay(word)
    return word, {'old_helper':h, 'new_owned_role':n+7, 'debited_target_rank':2, 'sites':receipts}


def boundary_changes(source, changes, published):
    """Apply five fixed PR5602 relations at checked PR5601 event positions."""
    C = L.load(L.HERE/'inputs/PR5602-construct.py', 'released_boundary_constructor')
    L.need([c['source_step'] for c in changes] == list(range(5)), 'Five published boundary relations')
    word, evidence = deepcopy(source), []
    public = word['public']

    def owned_events(w):
        return [e for e in w['program'] if e[1] >= public or
                (e[0] in ('ADD', 'COPY') and e[2] >= public)]

    owned = owned_events(source)
    before = L.replay(word)
    for item in changes:
        c = item['witness']
        original = published['steps'][item['source_step']]
        L.need(dict(c, cut=original['cut']) == original, 'Unchanged published boundary relation')
        oriented = C.transpose(word) if c['reverse'] else word
        L.need(oriented['program'][c['cut']] == item['anchor'], 'Exact boundary event anchor')
        word = C.boundary_basis(word, c)
        after = L.replay(word)
        for name, expected in (('paid', {5:-1}), ('helpers', {4:1, 9:-1})):
            delta = Counter(after[name])
            delta.subtract(before[name])
            L.need({r:n for r,n in delta.items() if n} == expected, 'Exact boundary '+name+' delta')
        evidence.append({'helper':c['helper'], 'cut':c['cut'], 'reverse':c['reverse'],
                         'events':len(word['program']), 'paid':after['paid'], 'helpers':after['helpers']})
        before = after
    C.restore_copy_opcodes(word)
    L.need(owned_events(word) == owned, 'The complete chronological owned paths are unchanged')
    L.replay(word)
    return word, evidence


def inverse(program):
    return [[e[0], *e[1:-2],
             str(1/Q(e[-2]) if e[0] == 'SCALE' else -Q(e[-2])), e[-1]]
            for e in reversed(program)]


def basis(a, b, pivot, frame):
    """Return B with row pivot equal to a and B b equal to e_pivot."""
    L.need(sum(v*b.get(k, 0) for k, v in a.items()) == 1, 'Unit basis pairing')
    roles = sorted(set(a) | set(b) | {pivot})
    values, program = dict(b), []

    def emit(event):
        program.append(event)
        r, q = event[1], Q(event[-2])
        if event[0] == 'SCALE':
            values[r] = values.get(r, 0)*q
        else:
            values[r] = values.get(r, 0)+q*values.get(event[2], 0)

    j = pivot if b.get(pivot) else next(r for r in roles if b.get(r))
    if j != pivot:
        for event in [['ADD', pivot, j, '1', frame],
                      ['ADD', j, pivot, '-1', frame],
                      ['ADD', pivot, j, '1', frame],
                      ['SCALE', j, '-1', frame]]:
            emit(event)
    if values[pivot] != 1:
        emit(['SCALE', pivot, str(1/values[pivot]), frame])
    for r in roles:
        if r != pivot and values.get(r):
            emit(['ADD', r, pivot, str(-values[r]), frame])
    L.need(all(values.get(r, 0) == int(r == pivot) for r in roles), 'Basis column')
    inverse_rows = {r: {r: Q(1)} for r in roles}
    for e in inverse(program):
        if e[0] == 'SCALE':
            inverse_rows[e[1]] = {k: Q(e[-2])*v for k, v in inverse_rows[e[1]].items()}
        else:
            L.add(inverse_rows[e[1]], inverse_rows[e[2]], Q(e[-2]))
    row = {}
    for r, q in a.items():
        L.add(row, inverse_rows[r], q)
    L.need(row[pivot] == 1, 'Basis row coefficient')
    for r in roles:
        if r != pivot and row.get(r):
            program.append(['ADD', pivot, r, str(row[r]), frame])
    return program


def check_cut(word, h):
    """Check the whole prefix row and suffix column over the rationals."""
    n, cut, f, p = word['public'], h['cut_after'], h['frame'], h['pivot']
    a, b, c, d = ({int(k): Q(v) for k, v in h[s].items()} for s in ('a', 'b', 'c', 'd'))
    main = set(word['live']) | {r+112 for r in word['live']}
    L.need(p < n and p not in main, 'A helper supplies the retained output role')
    u, v = word['initial'][p], word['final'][p]
    group = {r for r in range(n) if r not in main and
             (word['initial'][r], word['final'][r]) == (u, v)}
    L.need(set(c) | set(d) <= group, 'Both boundary vectors use one helper group')
    L.need(L.span(word['frames'][u]) < L.span(word['frames'][f]) < L.span(word['frames'][v]),
           'Two strictly productive nested targets')
    L.need(h['ranks'] == [len(word['frames'][f])-len(word['frames'][u]),
                          len(word['frames'][v])-len(word['frames'][f])], 'Declared split ranks')
    owned = word.get('owned_fields', 8)
    rows = [{r: Q(1)} if r < n else {} for r in range(n+owned)]
    current = word['initial']+[None]*owned
    for e in word['program'][:cut+1]:
        op, r = e[:2]
        if op == 'MOVE':
            current[r] = e[3]
        elif op in ('INIT', 'CLEAR'):
            rows[r] = {}
            current[r] = e[2] if op == 'INIT' else None
        elif op == 'SCALE':
            rows[r] = {k: Q(e[-2])*x for k, x in rows[r].items()}
        elif op == 'COPY':
            rows[r] = {k: Q(e[-2])*x for k, x in rows[e[2]].items()}
        else:
            L.add(rows[r], rows[e[2]], Q(e[-2]))
    L.need(all(current[r] == f for r in set(a) | set(b) | {p}), 'One intermediate chart')
    total = {}
    for r, q in a.items():
        L.add(total, rows[r], q)
    L.need(total == c, 'Exact prefix functional; no other input')
    column = [b.get(r, Q(0)) for r in range(n+owned)]
    for e in word['program'][cut+1:]:
        op, r = e[:2]
        if op in ('INIT', 'CLEAR'):
            column[r] = Q(0)
        elif op == 'SCALE':
            column[r] *= Q(e[-2])
        elif op == 'COPY':
            column[r] = Q(e[-2])*column[e[2]]
        elif op == 'ADD':
            column[r] += Q(e[-2])*column[e[2]]
    L.need(column == [d.get(r, Q(0)) for r in range(n+owned)], 'Exact suffix direction; no other output')
    L.need(sum(x*b.get(r, 0) for r, x in a.items()) ==
           sum(x*d.get(r, 0) for r, x in c.items()) == 1, 'Both independent pairings')
    return a, b, c, d


def split(word, h):
    a, b, c, d = check_cut(word, h)
    n, p, f, cut = word['public'], h['pivot'], h['frame'], h['cut_after']
    u, v = word['initial'][p], word['final'][p]

    def shift_owned(event):
        e = event.copy()
        e[1] += int(e[1] >= n)
        if e[0] in ('ADD', 'COPY'):
            e[2] += int(e[2] >= n)
        return e

    def use_successor(event):
        e = event.copy()
        if e[1] == p:
            e[1] = n
        if e[0] in ('ADD', 'COPY') and e[2] == p:
            e[2] = n
        return e

    boundary, middle = basis(c, d, p, u), basis(a, b, p, f)
    out = deepcopy(word)
    out['public'] = n+1
    out['initial'].append(f)
    out['final'].append(v)
    out['final'][p] = f
    out['program'] = inverse(boundary)
    out['program'] += [shift_owned(e) for e in word['program'][:cut+1]]
    out['program'] += [shift_owned(e) for e in middle]
    out['program'] += [use_successor(shift_owned(e)) for e in inverse(middle)]
    out['program'] += [use_successor(shift_owned(e)) for e in word['program'][cut+1:]]
    out['program'] += [use_successor([*e[:-1], v]) for e in boundary]
    return out


def construct(source, witnesses):
    word = deepcopy(source)
    baseline = L.replay(source)
    receipts = []
    for h in witnesses:
        word = split(word, h)
        result = L.replay(word)
        L.need(result['paid'] == baseline['paid'], 'Every paid Gaussian occurrence retained')
        receipts.append({'cut_after': h['cut_after'], 'pivot': h['pivot'],
                         'ranks': h['ranks'], 'public': word['public'],
                         'events': len(word['program'])})
    return word, receipts
