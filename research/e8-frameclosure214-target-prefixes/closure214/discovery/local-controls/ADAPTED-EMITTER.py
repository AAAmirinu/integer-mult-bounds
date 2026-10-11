def emit(c,ori):
    """Construct the complete local parametric invocation, before cover routing.
    One role stream is its full complete address rectangle. Frame labels denote
    exact canonical representatives, never just rank or binary matrices.
    """
    A=list(flat(c['A']));B=list(flat(c['B']));cur=c['start'].copy()
    sc=scatter.table(c);rank=scatter.centre_ranks(c)
    K=list(FROZEN_K)
    yield ('phase','old_response')
    if ori=='forward':
        for q in range(R):yield scal('old_response',copy(('T',q),L(2*V+q)),'old0')
        for _,t,s,a,b in K:yield scal('old_response',add(t,s,Q(-a if t[0]=='L' else a,b)),'old0')
    else:
        for q in range(R):yield scal('old_response',clear(('T',q)),'old0')
        for _,t,s,a,b in reversed(K):yield scal('old_response',add(s,t,Q(a,b)),'old0')
        for q in range(R):yield scal('old_response',add(L(2*V+q),('T',q),Q(1)),'old0')
    for q in range(R):yield scal('old_response',clear(('T',q)),'old0')
    yield ('phase','ad0')
    for r,f in enumerate(c['start']):yield ('adapter','old_to_new',r,f)
    for part in ['A','centers','B','final']:
        yield ('phase',part)
        if part in ['A','B']:
            for g in c[part]:
                regs=[g[2]]+[x[0] for x in g[3]]+(g[4] if g[0]=='out' else [])
                for r in regs:
                    if cur[r]!=g[1]:
                        old=cur[r];cur[r]=g[1]
                        yield ('climb',part,r,old,g[1],len(c['frames'][g[1]])-len(c['frames'][old]))
                for t,s,q in flat([g]):
                    e=add(L(t),L(s),q) if ori=='forward' else add(L(s),L(t),-q)
                    yield scal('main',e,g[1])
        elif part=='centers':
            for k,r,f in c['ret']:
                yield scal('main',clear(C(k)),f if ori=='forward' else 0)
                if ori=='forward':yield scal('main',add(C(k),L(r),Q(1)),f)
                else:
                    for t,p in enumerate(c['ports']):
                        if k in sc[t]:yield scal('main',add(C(k),L(V+t),sc[t][k]),0)
                yield ('center',k,f if ori=='forward' else 0,0 if ori=='forward' else f,rank[k])
                if ori=='forward':
                    for t,p in enumerate(c['ports']):
                        if k in sc[t]:yield scal('main',add(L(V+t),C(k),sc[t][k]),0)
                else:yield scal('main',add(L(r),C(k),Q(-1)),f)
                yield scal('main',clear(C(k)),0 if ori=='forward' else f)
        else:
            for r,f in enumerate(c['final']):
                if cur[r]!=f:
                    old=cur[r];cur[r]=f
                    yield ('climb','final',r,old,f,len(c['frames'][f])-len(c['frames'][old]))
    yield ('phase','adF')
    for r,f in enumerate(c['final']):yield ('adapter','new_to_old',r,f)
    yield ('phase','cleanup')
    for t,s,q in reversed(A+B):
        if role(t)=='Y':continue
        e=add(L(t),L(s),-q) if ori=='forward' else add(L(s),L(t),q)
        yield scal('cleanup',e,'old1')
    yield ('phase','done')

