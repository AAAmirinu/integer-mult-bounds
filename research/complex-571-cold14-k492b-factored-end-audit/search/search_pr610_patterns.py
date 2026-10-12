"""Exploratory fixed-dispatch pattern model; independently admit every output.

Uses PR610's documented pattern/flow model and bipartite edge colouring.
Prepared with OpenAI Codex assistance. No optimality beyond this pattern menu
is claimed; rounded entropy is a search objective, not a kappa certificate.
"""
import argparse, gzip, hashlib, json, math, time
from collections import Counter, defaultdict, deque
from pathlib import Path
from ortools.sat.python import cp_model

WIDTHS = (4,5,7,8,9)

def full_patterns(rank, i=0, prefix=()):
    if i == len(WIDTHS):
        if rank == 0:
            yield prefix
        return
    for n in range(rank // WIDTHS[i] + 1):
        yield from full_patterns(rank-n*WIDTHS[i], i+1, prefix+(n,))

def colour(flows, pattern, count):
    """Decompose a bipartite multigraph of maximum degree count into matchings."""
    times = sorted({t for t,w in flows})
    slots = [w for w,n in zip(WIDTHS,pattern) for _ in range(n)]
    n = max(len(times), len(slots))
    if not slots:
        return [[] for _ in range(count)]
    graph = [[0]*n for _ in range(n)]
    for w in WIDTHS:
        available = deque([s,count] for s,sw in enumerate(slots) if sw == w)
        for j,t in enumerate(times):
            remaining = flows.get((t,w),0)
            while remaining:
                s,space = available[0]; k = min(space,remaining)
                graph[s][j] += k; remaining -= k; available[0][1] -= k
                if available[0][1] == 0:
                    available.popleft()
        assert not available
    real = [row[:] for row in graph]
    rd = [count-sum(row) for row in graph]
    cd = [count-sum(graph[i][j] for i in range(n)) for j in range(n)]
    assert min(rd+cd) >= 0
    j = 0
    for i in range(n):
        while rd[i]:
            while cd[j] == 0:
                j += 1
            k = min(rd[i], cd[j]); graph[i][j] += k; rd[i] -= k; cd[j] -= k
    result = []
    for _ in range(count):
        match = [-1]*n
        def augment(i, seen):
            for j in range(n):
                if not graph[i][j] or j in seen:
                    continue
                seen.add(j)
                if match[j] < 0 or augment(match[j], seen):
                    match[j] = i
                    return True
            return False
        assert all(augment(i,set()) for i in range(n))
        roles = []
        for j,i in enumerate(match):
            graph[i][j] -= 1
            if real[i][j]:
                real[i][j] -= 1
                roles.append((times[j], slots[i]))
        assert len(roles) == len(slots) and len({t for t,w in roles}) == len(roles)
        result.append(roles)
    assert not any(any(row)for row in real)
    return result

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--seconds', type=float, default=120)
    args = ap.parse_args(); args.out.mkdir(parents=True,exist_ok=False)
    planraw = (args.data/'PLAN.json').read_bytes(); raw = (args.data/'OWNERS.json.gz').read_bytes()
    plan = json.loads(planraw); roles = json.loads(gzip.decompress(raw))
    groups = defaultdict(list)
    for key,(cap,ts) in plan['windows'].items():
        groups[cap,tuple(ts)].append(tuple(map(int,key.split(','))))
    groups = list(groups.items())
    group_at = {oc:g for g,(_,ocs) in enumerate(groups) for oc in ocs}
    bins = defaultdict(list)
    for r in roles:
        bins[r['owner_replica'],r['child'],r['port']].append(r)
    initial = Counter(); initial_flow = Counter(); menu = defaultdict(set)
    for g,((cap,ts),ocs) in enumerate(groups):
        for o,ch in ocs:
            for port in range(112):
                rows = bins[o,ch,port]; counts = Counter(r['width']for r in rows)
                p = tuple(counts[w]for w in WIDTHS); initial[g,p] += 1; menu[cap].add(p)
                for r in rows:
                    initial_flow[g,p,r['time'],r['width']] += 1
    for cap in menu:
        menu[cap].update(full_patterns(cap))
        menu[cap].add((0,)*len(WIDTHS))
        for w in WIDTHS:
            if w <= cap:
                menu[cap].add(tuple(int(v == w)for v in WIDTHS))
    model = cp_model.CpModel(); pattern_vars = {}; flow_vars = {}; demand_terms = defaultdict(list); objective = []
    for g,((cap,ts),ocs) in enumerate(groups):
        limit = 112*len(ocs); xs = []
        for p in sorted(menu[cap]):
            if sum(p) > len(ts):
                continue
            x = model.new_int_var(0,limit,f'x{g}_{p}'); pattern_vars[g,p] = x; xs.append(x)
            model.add_hint(x, initial[g,p])
            rem = cap-sum(w*n for w,n in zip(WIDTHS,p))
            cost = round(1e6*rem*math.log(73/rem)) if rem else 0
            objective.append(cost*x)
            by_width = defaultdict(list)
            for t in ts:
                fs = []
                for w,n in zip(WIDTHS,p):
                    if not n:
                        continue
                    f = model.new_int_var(0,limit,f'f{g}_{p}_{t}_{w}')
                    flow_vars[g,p,t,w] = f; fs.append(f); by_width[w].append(f); demand_terms[t,w].append(f)
                    model.add_hint(f, initial_flow[g,p,t,w])
                if fs:
                    model.add(sum(fs) <= x)
            for w,n in zip(WIDTHS,p):
                if n:
                    model.add(sum(by_width[w]) == n*x)
        model.add(sum(xs) == limit)
    for t,c in enumerate(plan['provider_calls']):
        counts = Counter(plan['provider_registry'][c['provider']]['widths'])
        for w in WIDTHS:
            model.add(sum(demand_terms[t,w]) == counts[w])
    model.minimize(sum(objective))
    solver = cp_model.CpSolver(); solver.parameters.num_search_workers = 2
    solver.parameters.random_seed = 0; solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.log_search_progress = True
    print('MODEL',len(pattern_vars),len(flow_vars),flush=True)
    status = solver.solve(model)
    summary = dict(status=solver.status_name(status), seconds=solver.wall_time, rounded_entropy=solver.objective_value/1e6, lower_bound=solver.best_objective_bound/1e6,
                   pattern_variables=len(pattern_vars), flow_variables=len(flow_vars), scope='Restricted-pattern nomination only; independent physical and exact arithmetic admission required.')
    (args.out/'SEARCH.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)
    if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        return
    queues = defaultdict(deque)
    for r in roles:
        queues[r['time'],r['width']].append(r)
    newroles = []; idle = Counter()
    for g,((cap,ts),ocs) in enumerate(groups):
        available = deque((o,ch,port)for o,ch in ocs for port in range(112))
        for p in sorted(menu[cap]):
            if (g,p) not in pattern_vars:
                continue
            count = solver.value(pattern_vars[g,p])
            if not count:
                continue
            flows = {(t,w):solver.value(flow_vars[g,p,t,w])for t in ts for w,n in zip(WIDTHS,p) if n}
            for matching in colour(flows,p,count):
                o,ch,port = available.popleft(); off = 0
                for t,w in sorted(matching):
                    r = dict(queues[t,w].popleft())
                    fam = o*896+(2*plan['pairs'][str(ch)]+plan['sides'][str(ch)])*112+port
                    r.update(owner_replica=o,child=ch,port=port,copy=o*112+port,family=fam,offset=off)
                    newroles.append(r); off += w
                if cap-off:
                    idle[cap-off] += 1
        assert not available
    assert not any(queues.values()) and len(newroles) == len(roles)
    paid = idle.copy()
    for c in plan['provider_calls']:
        paid.update({int(r):n for r,n in plan['provider_registry'][c['provider']]['actual_paid_profile'].items()})
    assert 73*plan['live']-sum(r*n for r,n in paid.items()) == plan['deficit']
    newroles.sort(key=lambda r:(r['time'],r['helper']))
    packed = json.dumps(newroles,sort_keys=True,separators=(',',':')).encode()
    plan.update(profile={str(r):n for r,n in sorted(paid.items())}, mode='restricted-pattern-exact-flow-edge-colouring', solver_status=summary['status'], gap=None,
                assignment_sha256=hashlib.sha256(packed).hexdigest(),source_plan_sha256=hashlib.sha256(planraw).hexdigest(),source_owners_sha256=hashlib.sha256(raw).hexdigest())
    (args.out/'OWNERS.json.gz').write_bytes(gzip.compress(packed,mtime=0))
    (args.out/'PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
    print('EXPANDED',len(newroles),'PROFILE',plan['profile'],flush=True)

if __name__ == '__main__':
    main()
