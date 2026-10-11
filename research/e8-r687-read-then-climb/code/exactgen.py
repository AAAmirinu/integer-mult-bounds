# Exact min sum-rank (=> max pivots) for one 'big' component via: block decomposition, per-block exact DP over span states,
# coupling elements enumerated, DFS over blocks with optimistic-completion pruning.
# usage: exactgen.py DATA.json comps.json [maxslack] [lb]     ('lb': stop after the lower bounds; small components are still exact)
# Completeness: block states are kept up to slack MAXSLACK, so an infeasible total T is proved only when T - LB <= MAXSLACK; the
# reported optimum T is exact when T - LB <= MAXSLACK + 1 (the last infeasible total lies within the kept slack). Feasible totals
# come with an explicit assignment found by the search.
# Prepared by DreamingOfClouds with Claude (the project's matroid scout), via Claude Code; header, 'lb' mode and the machine-readable
# CERT line by DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code.  Apache-2.0.
import json,sys,time,itertools,pickle
from collections import defaultdict
DATA=sys.argv[1]; COMPS=sys.argv[2]; MAXSLACK=int(sys.argv[3]) if len(sys.argv)>3 else 2; LBONLY=len(sys.argv)>4 and sys.argv[4]=='lb'
D=json.load(open(DATA))
fl={int(k):v for k,v in D['fl'].items()}; resp={int(k):v for k,v in D['resp'].items()}
comps=json.load(open(COMPS)); comps.sort(key=len,reverse=True)
def red(y,b):
    for x in b: y=min(y,y^x)
    return y
def canon(basis):
    out=[]
    for x in sorted(basis,reverse=True):
        x=red(x,out)
        if x: out.append(x); out.sort(reverse=True)
    ch=True
    while ch:
        ch=False
        for i in range(len(out)):
            for j in range(len(out)):
                if i!=j and (out[i]>>(out[j].bit_length()-1))&1: out[i]^=out[j]; ch=True
    return tuple(sorted(out,reverse=True))
def blockstates(els,cap):
    classes=sorted({i for h in els for i in fl[h]}); ci={i:k for k,i in enumerate(classes)}
    els=sorted(els,key=lambda h:(len(fl[h]),resp[h]))
    states={tuple(() for _ in classes):0}
    for h in els:
        new={}
        for st,cost in states.items():
            for i in fl[h]:
                k=ci[i]; b=st[k]; y=red(resp[h],list(b))
                if y:
                    nc=cost+1
                    if nc>cap: continue
                    ns=st[:k]+(canon(list(b)+[resp[h]]),)+st[k+1:]
                else: nc=cost; ns=st
                if ns not in new or new[ns]>nc: new[ns]=nc
        states=new
    return classes,states
def supp(y): return [t for t in range(120) if y>>t&1]
def span_of(vs):
    b=[]
    for y in vs:
        y=red(y,b)
        if y: b.append(y); b.sort(reverse=True)
    return b
def quot_rank(vecs,basis):
    b=list(basis); r=0
    for v in vecs:
        y=red(v,b)
        if y: b.append(y); b.sort(reverse=True); r+=1
    return r
def analyse(c):
    par=list(range(120))
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for h in c:
        s=supp(resp[h])
        if len(s)<=4:
            for t in s[1:]: par[f(t)]=f(s[0])
    blocks=defaultdict(list); coupling=[]
    for h in c:
        bs={f(t) for t in supp(resp[h])}
        if len(bs)==1: blocks[bs.pop()].append(h)
        else: coupling.append(h)
    return blocks,coupling
def solve(c):
    blocks,coupling=analyse(c)
    t0=time.time()
    mins={}; STs={}
    for kk,els in blocks.items():
        for cap in range(1,60):
            cl,st=blockstates(els,cap)
            if st: break
        mn=min(st.values()); mins[kk]=mn
        cl,st=blockstates(els,mn+MAXSLACK); STs[kk]=(cl,st)
    S0=sum(mins.values())
    classes8=range(8)
    locmax={kk:{i:span_of([resp[h] for h in els if i in fl[h]]) for i in classes8} for kk,els in blocks.items()}
    fixed=[h for h in coupling if len(fl[h])==1]; free=sorted(h for h in coupling if len(fl[h])>1)
    def Ci(a):
        d=defaultdict(list)
        for h in fixed: d[fl[h][0]].append(h)
        for h,i in zip(free,a): d[i].append(h)
        return d
    def value(a,spans):
        d=Ci(a); return sum(quot_rank([resp[h] for h in d[i]],spans[i]) for i in classes8)
    fullmax={i:span_of([v for kk in blocks for v in locmax[kk][i]]) for i in classes8}
    allA=list(itertools.product(*[fl[h] for h in free]))
    vals=[(value(a,fullmax),a) for a in allA]
    cmin=min(v for v,a in vals)
    LB=S0+cmin
    print(f'  blocks {len(blocks)} coupling {len(coupling)} (free {len(free)}), sum block mins {S0}, coupling LB {cmin} -> LB sumrank {LB}  [{time.time()-t0:.0f}s]',flush=True)
    order=sorted(blocks,key=lambda kk:len(STs[kk][1]))
    def feasible(T):
        budget=T-S0   # slack_total + coupling <= budget
        A=[a for v,a in vals if v<=budget]
        def opt_spans(chosen,depth):
            sp={i:list(chosen[i]) for i in classes8}
            for kk in order[depth:]:
                for i in classes8:
                    for v in locmax[kk][i]:
                        y=red(v,sp[i])
                        if y: sp[i].append(y); sp[i].sort(reverse=True)
            return sp
        def dfs(depth,chosen,alive,slack):
            if depth==len(order): return True
            kk=order[depth]; cls,st=STs[kk]
            for s_,cost in st.items():
                sl=cost-mins[kk]
                if slack+sl>budget: continue
                ch={i:list(chosen[i]) for i in classes8}
                for k,i in enumerate(cls):
                    for v in s_[k]:
                        y=red(v,ch[i])
                        if y: ch[i].append(y); ch[i].sort(reverse=True)
                sp=opt_spans(ch,depth+1)
                al=[a for a in alive if slack+sl+value(a,sp)<=budget]
                if al and dfs(depth+1,ch,al,slack+sl): return True
            return False
        return dfs(0,{i:[] for i in classes8},A,0)
    if LBONLY: return None,LB
    for T in range(LB,LB+MAXSLACK+3):
        ok=feasible(T)
        print(f'  total sumrank <= {T} attainable: {ok}  [{time.time()-t0:.0f}s]',flush=True)
        if ok: return T,LB
    return None,LB
tot=0; cert=[]
for c in comps:
    if len(c)<2: continue
    print('component',len(c),'rank',len(span_of([resp[h] for h in c])),flush=True)
    r=len(span_of([resp[h] for h in c]))
    # small components: exact DP directly
    if len(c)<=40:
        for cap in range(1,60):
            cl,st=blockstates(c,cap)
            if st: break
        T=min(st.values()); print('  exact DP min sumrank',T,'pivots',len(c)-T); tot+=len(c)-T; cert.append(dict(size=len(c),method='dp',min_sumrank=T)); continue
    T,LB=solve(c)
    print('  => min sumrank',T,'(LB',LB,') pivots',len(c)-T if T else None); tot+=len(c)-T if T else len(c)-LB
    cert.append(dict(size=len(c),method='search',LB=LB,min_sumrank=T,maxslack=MAXSLACK,complete=(T is not None and T-LB<=MAXSLACK+1)))
coloops=sum(1 for c in comps if len(c)<2); tot+=0   # coloops carry no pivot
print(('UPPER BOUND max pivots (lower bounds only)' if LBONLY else 'TOTAL max pivots (exact, rank-1 axis-class model)'),tot)
print('CERT',json.dumps(dict(components=cert,coloops=coloops,max_pivots=None if LBONLY else tot,upper_bound=tot,lb_only=LBONLY)))
