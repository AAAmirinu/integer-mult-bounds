"""Copy-free (or minimum-copy) read ordering per block. Atoms = 12 keys + 8 own rows. Registers = copies of keys. A read (x,K,copy) at time tau
makes x acquire the register's frame atoms and the register acquire x's frame atoms; every atom in a target's frame must lie in its cap.
Own read is each target's first read. Usage: order_model.py blocks.json [maxcopies per key] [time limit s] [variant]
variant 'A': all 12 keys read as formed M's; 'B': selected partition delivered by the existing butterfly (its 4 keys + partner's own enter the
frame at a fixed point: we model it as x having read both selected keys and partner's own atom before any non-selected read)."""
import json,sys,itertools as it,collections
from ortools.sat.python import cp_model
BL=json.load(open(sys.argv[1]));MAXC=int(sys.argv[2])if len(sys.argv)>2 else 1;TL=float(sys.argv[3])if len(sys.argv)>3 else 60;VAR=sys.argv[4]if len(sys.argv)>4 else'A';OWN=sys.argv[6]if len(sys.argv)>6 else'first'
def solve(cname,b):
    ids=b['sources'];keys=[str(k)for k in b['keys']];sel={str(k):v['selected']for k,v in zip(b['keys'],b['K'].values())}
    T=b['T'];cons={x:[str(k)for k in T[x]['cons']]for x in T};own_in={x:{y:T[x]['own_in_cap'][y]for y in T[x]['own_in_cap']}for x in T}
    X=list(T)
    atoms=keys+['own'+x for x in X]
    def incap(x,a):
        if a.startswith('own'):return own_in[a[3:]][x]
        return a in cons[x]
    rdkeys={x:[k for k in cons[x]if VAR=='A'or not sel[k]]for x in X}
    reads=[(x,k)for x in X for k in rdkeys[x]]+[(x,'own')for x in X]
    N=len(reads);m=cp_model.CpModel()
    pos={r:m.NewIntVar(0,N-1,'p%s'%str(r))for r in reads};m.AddAllDifferent(list(pos.values()))
    at={(r,t):m.NewBoolVar('')for r in reads for t in range(N)}
    for r in reads:
        m.AddExactlyOne(at[r,t]for t in range(N))
        for t in range(N):m.Add(pos[r]==t).OnlyEnforceIf(at[r,t]);m.Add(pos[r]!=t).OnlyEnforceIf(at[r,t].Not())
    for x in X:
        for k in rdkeys[x]:
            if OWN=='first':m.Add(pos[x,'own']<pos[x,k])
    regs=[(k,i)for k in keys if any(k in rdkeys[x]for x in X)for i in range(MAXC)]
    use={(x,k,i):m.NewBoolVar('')for x in X for k in rdkeys[x]for i in range(MAXC)}
    used={(k,i):m.NewBoolVar('')for k,i in regs}
    for x in X:
        for k in rdkeys[x]:
            m.AddExactlyOne(use[x,k,i]for i in range(MAXC))
            for i in range(MAXC):m.AddImplication(use[x,k,i],used[k,i])
    for k,i in regs:
        if i:m.AddImplication(used[k,i],used[k,i-1])
    # frames over time
    inF={(x,a,t):(m.NewBoolVar('')if incap(x,a)else None)for x in X for a in atoms for t in range(N+1)}
    regF={(k,i,a,t):m.NewBoolVar('')for k,i in regs for a in atoms for t in range(N+1)}
    for x in X:
        for a in atoms:
            if inF[x,a,0]is not None:m.Add(inF[x,a,0]==0)
            for t in range(N):
                if inF[x,a,t]is not None:m.AddImplication(inF[x,a,t],inF[x,a,t+1])
    for k,i in regs:
        for a in atoms:
            m.Add(regF[k,i,a,0]==(a==k))
            for t in range(N):m.AddImplication(regF[k,i,a,t],regF[k,i,a,t+1])
    # variant B initial frame: selected keys and selected partner's own are in x's frame from the start (butterfly before non-selected reads)
    if VAR=='B':
        for x in X:
            for k in cons[x]:
                if sel[k]:m.Add(inF[x,k,1]==1)
        # partner's own: find partner = same tetrad target sharing both selected keys
        for x in X:
            for y in X:
                if y!=x and T[x]['tetrad']==T[y]['tetrad']and set(k for k in cons[x]if sel[k])==set(k for k in cons[y]if sel[k]):
                    a='own'+y
                    if inF[x,a,1]is None:print('  variant B: partner own not in cap!',x,y);m.Add(0==1)
                    else:m.Add(inF[x,a,1]==1)
    for x in X:
        for t in range(N):
            # own read at t: own atom enters
            m.AddImplication(at[(x,'own'),t],inF[x,'own'+x,t+1])
            for k in rdkeys[x]:
                for i in range(MAXC):
                    both=m.NewBoolVar('');m.AddBoolAnd([at[(x,k),t],use[x,k,i]]).OnlyEnforceIf(both);m.AddBoolOr([at[(x,k),t].Not(),use[x,k,i].Not()]).OnlyEnforceIf(both.Not())
                    for a in atoms:
                        # register atoms flow to x
                        if inF[x,a,t+1]is None:m.AddImplication(both,regF[k,i,a,t].Not())
                        else:m.AddBoolOr([both.Not(),regF[k,i,a,t].Not(),inF[x,a,t+1]])
                        # x's atoms flow to register
                        if inF[x,a,t]is not None:m.AddBoolOr([both.Not(),inF[x,a,t].Not(),regF[k,i,a,t+1]])
                    m.AddImplication(both,inF[x,k,t+1])
    ncopies=sum(used[k,i]for k,i in regs if i>0)
    m.Minimize(ncopies)
    s=cp_model.CpSolver();s.parameters.max_time_in_seconds=TL;s.parameters.num_workers=8
    st=s.Solve(m)
    print(cname,'variant',VAR,'own',OWN,'maxcopies',MAXC,'status',s.StatusName(st),'copies',s.ObjectiveValue()if st in(cp_model.OPTIMAL,cp_model.FEASIBLE)else None,'bound',s.BestObjectiveBound()if st in(cp_model.OPTIMAL,cp_model.FEASIBLE)else None,'time',round(s.WallTime(),1))
    if st in(cp_model.OPTIMAL,cp_model.FEASIBLE):
        order=sorted(reads,key=lambda r:s.Value(pos[r]))
        sched=[(r[0],r[1],next(i for i in range(MAXC)if r[1]=='own'or s.Value(use[r[0],r[1],i])))for r in order]
        return sched
for c in list(BL)[:int(sys.argv[5])if len(sys.argv)>5 else 1]:
    sch=solve(c,BL[c])
    if sch:
        X=list(BL[c]['T']);per=collections.defaultdict(list)
        for x,k,i in sch:per[x].append((k,i))
        for x in X:print('  ',x,per[x])
