"""Joint multi-call nominations extending Jay Mosley's PR653 two-call model.

Every accepted move passes the inherited literal owner checks and exact integer
stop-loss inequalities. Solver output is not global admission. Apache-2.0.
Prepared by Jeremy Diviney with substantial OpenAI Codex assistance.
"""
from joint_owner_search import *
from joint_owner_passes import write_outputs


def solve_group(inst, calls, seconds):
    buckets = defaultdict(list)
    oldmaps = {t: {g: (h, w) for h, (g, w) in inst.bycall[t].items()} for t in calls}
    groups = set().union(*(inst.eligible[t] for t in calls))
    for g in sorted(groups):
        capacity = inst.caps[g] - inst.used[g] + sum(oldmaps[t].get(g, (None, 0))[1] for t in calls)
        mask = sum((1 << i) for i, t in enumerate(calls) if g in inst.eligible[t])
        buckets[capacity, mask].append(g)
    cats = sorted(buckets)
    widths = sorted(set(inst.widths))
    inventory = Counter(inst.widths)
    rhs = [len(buckets[key]) for key in cats] + [inventory[w] for _ in calls for w in widths]
    equalrows = len(rhs)
    oldremainders = [inst.caps[g] - inst.used[g] for g in groups]
    rhs += [sum(max(r-k, 0) for r in oldremainders) for k in range(1, 48)]
    columns, rows, cols, values, objective, bounds = [], [], [], [], [], []
    for ci, (capacity, mask) in enumerate(cats):
        options = [[0] + widths if mask & (1 << i) else [0] for i in range(len(calls))]
        for assignment in itertools.product(*options):
            if sum(assignment) > capacity:
                continue
            j = len(columns)
            columns.append((ci, assignment))
            rows.append(ci); cols.append(j); values.append(1)
            for side, w in enumerate(assignment):
                if w:
                    rows.append(len(cats) + side * len(widths) + widths.index(w))
                    cols.append(j); values.append(1)
            remainder = capacity - sum(assignment)
            for k in range(1, remainder):
                rows.append(equalrows+k-1); cols.append(j); values.append(remainder-k)
            objective.append((remainder * math.expm1(inst.baseline['b'] * math.log(73/remainder)) if remainder else 0) * 1e6)
            bounds.append(len(buckets[capacity, mask]))
    matrix = coo_matrix((values, (rows, cols)), shape=(len(rhs), len(columns))).tocsc()
    rhs = np.asarray(rhs)
    upper = np.concatenate((rhs[:equalrows], np.full(len(rhs)-equalrows, np.inf)))
    started = time.monotonic()
    result = milp(objective, integrality=np.ones(len(columns)), bounds=Bounds(np.zeros(len(columns)), bounds),
                  constraints=LinearConstraint(matrix, rhs, upper),
                  options={'time_limit': seconds, 'mip_rel_gap': 0.0, 'threads': 1})
    report = dict(calls=list(calls), status=int(result.status), message=str(result.message),
                  seconds=time.monotonic()-started, variables=len(columns), buckets=len(cats))
    if result.x is None:
        return report, None
    x = np.rint(result.x).astype(np.int64)
    assert np.max(np.abs(result.x-x)) < 1e-5
    assert np.all(x >= 0) and np.all(x <= bounds)
    assert np.all((matrix @ x)[:equalrows] == rhs[:equalrows])
    assert np.all((matrix @ x)[equalrows:] >= rhs[equalrows:])
    report.update(integer_equations_checked=True, mip_gap=float(result.mip_gap), mip_nodes=int(result.mip_node_count))
    choices = defaultdict(Counter)
    for count, (ci, assignment) in zip(x, columns):
        choices[ci][assignment] += int(count)
    assigned = {t: defaultdict(list) for t in calls}
    for ci, key in enumerate(cats):
        pending = []
        for g in buckets[key]:
            assignment = tuple(oldmaps[t].get(g, (None, 0))[1] for t in calls)
            if not choices[ci][assignment]:
                pending.append(g)
                continue
            choices[ci][assignment] -= 1
            for t, w in zip(calls, assignment):
                if w: assigned[t][w].append(g)
        remaining = deque(a for a, count in sorted(choices[ci].items()) for _ in range(count))
        assert len(remaining) == len(pending)
        for g in pending:
            for t, w in zip(calls, remaining.popleft()):
                if w: assigned[t][w].append(g)
    roles = [dict(z) for z in inst.roles if z['time'] not in calls]
    for t in calls:
        stage, replica = inst.plan['order'][t]
        available = {w: set(gs) for w, gs in assigned[t].items()}
        nominated = {}
        for h, (g, w) in sorted(inst.bycall[t].items()):
            if g in available[w]:
                available[w].remove(g); nominated[h] = g
        for h, w in enumerate(inst.widths):
            if h not in nominated:
                g = min(available[w]); available[w].remove(g); nominated[h] = g
            g = nominated[h]; owner_replica, child, port = g
            roles.append(dict(child=child, copy=owner_replica*112+port, family=inst.families[g], helper=h,
                              offset=0, owner_replica=owner_replica, port=port, replica=replica, stage=stage, time=t, width=w))
        assert not any(available.values())
    grouped = defaultdict(list)
    for role in roles: grouped[role['owner_replica'], role['child'], role['port']].append(role)
    for group in grouped.values():
        offset = 0
        for role in sorted(group, key=lambda z: (z['time'], z['helper'])):
            role['offset'] = offset; offset += role['width']
    roles.sort(key=lambda z: (z['time'], z['helper']))
    checked = inst.check(roles)
    old, new = Counter(inst.baseline['idle']), Counter(checked['idle'])
    margins = [sum(n*max(r-k, 0) for r, n in new.items()) - sum(n*max(r-k, 0) for r, n in old.items()) for k in range(49)]
    assert margins[0] == margins[-1] == 0 and min(margins) >= 0
    report.update(candidate=checked, gain_b=checked['b']-inst.baseline['b'], integer_stoploss_margins=margins,
                  strict_majorization=max(margins)>0)
    return report, roles


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--owners', type=Path, required=True)
    ap.add_argument('--groups', type=int, default=120)
    ap.add_argument('--size', type=int, choices=(2, 3, 4, 5), default=3)
    ap.add_argument('--seconds', type=float, default=2)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args(); args.out.mkdir(exist_ok=False)
    inst = Instance(args.owners); inst.source_owners_path = args.owners
    inst.source_head = '0805e78f5fecc700804d4766d7e3e1d7d7e6a2ba'
    original = inst.baseline; steps = []; reports = []
    defect = {g for g in inst.caps if 0 < inst.caps[g]-inst.used[g] < inst.caps[g]}
    overlap = {(a,b): len(inst.eligible[a] & inst.eligible[b] & defect) for a,b in itertools.combinations(range(72), 2)}
    pool = range(72)
    if args.size == 5:
        nonmax = {g for g in inst.caps if 0 < inst.caps[g]-inst.used[g] < 48}
        pool = sorted(range(72), key=lambda t: (len(inst.eligible[t] & nonmax), -t), reverse=True)[:16]
        overlap = {(a,b): len(inst.eligible[a] & inst.eligible[b] & nonmax) for a,b in itertools.combinations(range(72), 2)}
    scored = [(sum(overlap[p] for p in itertools.combinations(calls, 2)), calls) for calls in itertools.combinations(sorted(pool), args.size)]
    for _, calls in sorted(scored, reverse=True)[:args.groups]:
        report, roles = solve_group(inst, calls, args.seconds); reports.append(report)
        if roles is not None and report['strict_majorization']:
            assert report['gain_b'] > 0
            steps.append(report); inst.roles = roles; inst.used = Counter(); inst.bycall = defaultdict(dict)
            for z in roles:
                g = z['owner_replica'], z['child'], z['port']
                inst.used[g] += z['width']; inst.bycall[z['time']][z['helper']] = g, z['width']
            inst.baseline = inst.check(roles)
            write_outputs(args.out, inst, original, steps)
            print(json.dumps(dict(calls=calls, accepted=len(steps), b=inst.baseline['b'], gain=inst.baseline['b']-original['b'])), flush=True)
        (args.out/'SEARCH.json').write_text(json.dumps(dict(groups=len(reports), reports=reports), indent=2)+'\n')
    write_outputs(args.out, inst, original, steps)
    print('DONE', len(reports), 'groups;', len(steps), 'accepted;', inst.baseline['b'], flush=True)
