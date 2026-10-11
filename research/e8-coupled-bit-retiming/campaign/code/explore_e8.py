"""Bounded E8 compiler experiments against immutable PR370.

New research: OpenAI Codex assistance, Apache-2.0. Compiler policies derive
from Dylan Crow's PR370 compiler; this is a discovery tool, not a proof.
"""
from pathlib import Path
import os, sys, ast, json, gzip, math, inspect, copy, time, argparse
from collections import Counter, defaultdict
BASE = Path(__file__).resolve().parent
PRODUCER = BASE.parents[1] / 'vendor/source375/code/bit/producer'
os.environ['E8COORD'] = 'ham'
sys.path.insert(0, str(PRODUCER))
import e8lib as E, frames as F, ham1, ham2, compile as C, compile2 as C2, fullword
from scipy.optimize import linear_sum_assignment

PARAMS = {ast.literal_eval(k): v for k,v in json.loads((PRODUCER/'params-r865.json').read_text())}
V=120

def g(r):
    return r*math.log(40/r) if r else 0.0

def low_chain(h, needed, ph, drop=frozenset(), mode='weighted'):
    answer=set()
    for t in range(V):
        nodes=sorted((u for u in h.need[t] if h.dim[u]<7),key=lambda u:(h.dim[u],u))
        best={}
        for j,u in enumerate(nodes):
            # The path starts at zero and finishes at the rank-seven target cap.
            cost=g(h.dim[u]); chain=[u]
            for w in nodes[:j]:
                if h.dim[w]<h.dim[u] and F.inside(h.frame[w],h.frame[u]):
                    candidate=best[w][0]+g(h.dim[u]-h.dim[w])
                    if candidate<cost: cost,chain=candidate,best[w][1]+[u]
            best[u]=(cost,chain)
        options=[(g(7),[])]+[(cost+g(7-h.dim[u]),ch) for u,(cost,ch) in best.items()]
        chain=min(options,key=lambda p:(p[0],len(p[1])))[1]
        answer.update((t,u) for u in chain if (t,u) not in drop)
    return answer

def phase_cut(h,needed,cut):
    ph={}
    def visit(u):
        if u<V: return 'S'
        if u in ph:return ph[u]
        children=[visit(c) for c in h.kids[u]]
        ph[u]='A' if h.dim[u]<=cut and all(x in ('S','A') for x in children) else 'B'
        return ph[u]
    for u in needed:
        if u>=V:visit(u)
    return ph

def make_chains(h,needed,uses,policy):
    chains={}; chain_of={}
    for u in needed:
        ev=sorted(uses[u],key=lambda e:(e[0],e[1],e[2],e[4]))
        n=len(ev); score=[[0.0]*(2*n) for _ in range(n)]
        legal=set(); fu=h.dim[u]
        for i,a in enumerate(ev):
            for j in range(i+1,n):
                b=ev[j]
                if not (a[3]==b[3] or (a[1]<b[1] and F.inside(a[3],b[3]))):continue
                legal.add((i,j))
                if policy=='count':gain=1000.0
                elif policy=='entropy':gain=g(8-a[1])+g(b[1]-fu)+g(fu)-g(b[1]-a[1])
                else:
                    p=1-0.000904072820242522
                    power=lambda r:r**p if r else 0.0
                    gain=power(8-a[1])+power(b[1]-fu)+power(fu)-power(b[1]-a[1])-40**p/5
                # Count policy is only maximum-cardinality; the other policies
                # may leave a legal edge unmatched when it increases cost.
                score[i][j]=-gain
        rr,cc=linear_sum_assignment(score) if n else ([],[])
        nxt={i:j for i,j in zip(rr,cc) if (i,j) in legal and score[i][j]<-1e-13}
        incoming=set(nxt.values()); cl=[]
        for i in range(n):
            if i in incoming:continue
            ch=[]; j=i
            while True:
                ch.append(ev[j]);chain_of[(u,ev[j][2],ev[j][4])]=len(cl)
                if j not in nxt:break
                j=nxt[j]
            cl.append(ch)
        assert sum(map(len,cl))==n
        chains[u]=cl
    return chains,chain_of

def source_choice(chains,policy):
    eligible=[i for i,ch in enumerate(chains) if all(e[0]==0 for e in ch)]
    if not eligible:return None
    if policy=='deep':return max(eligible,key=lambda i:(chains[i][-1][1],len(chains[i])))
    def cost(i):
        dims=[1]+[e[1] for e in chains[i]]+[8]
        return sum(g(b-a) for a,b in zip(dims,dims[1:]))
    return min(eligible,key=cost)

def compiler(method):
    source=inspect.getsource(C2.compile2)
    env=dict(C2.__dict__)
    if method.startswith('cover_'):
        first=source.index('    chains={}; chain_of={}')
        last=source.index('    W=C.Word(); reg={}',first)
        source=source[:first]+"    chains,chain_of=custom_chains(h,needed,uses)\n"+source[last:]
        policy=method.split('_')[1]
        env['custom_chains']=lambda h,n,u:make_chains(h,n,u,policy)
    if method.startswith('source_'):
        old='        if cand: xi=max(cand,key=lambda i:len(cl[i]))'
        assert old in source
        source=source.replace(old,'        xi=source_choice(cl, SOURCE_POLICY)')
        env.update(source_choice=source_choice,SOURCE_POLICY=method.split('_')[1])
    if method.startswith('phase'):
        if method=='phase_minimal':
            def phases(h,needed):
                previous=C2.PHASEMODE[0]
                try:C2.PHASEMODE[0]='minimal';return C2.phases(h,needed)
                finally:C2.PHASEMODE[0]=previous
            env['phases']=phases
        else:env['phases']=lambda h,n:phase_cut(h,n,int(method[-1]))
    if method=='low_weighted':env['choose_low']=low_chain
    if method in ('low4','low5','no5','no_low'):
        def choose(h,n,p,drop=frozenset()):
            ans=C2.choose_low(h,n,p,drop)
            if method=='no_low':return set()
            if method=='no5':return {(t,u) for t,u in ans if h.dim[u]!=5}
            return {(t,u) for t,u in ans if h.dim[u]<=int(method[-1])}
        env['choose_low']=choose
    exec(compile(source,'<research-compiler>','exec'),env)
    return env['compile2']

def rebuild(h,method):
    new=ham1.SH()
    order=sorted(range(V,len(h.content)),key=lambda u:(h.content[u].bit_count(),u))
    for u in order:
        mask=h.content[u];leaves=[s for s in range(V) if mask>>s&1]
        if method=='tree_reuse':
            parts=[];remaining=mask
            while remaining:
                choices=[(new.content[w].bit_count(),-new.dim[w],w) for w in range(len(new.content))
                         if new.content[w] and new.content[w]&remaining==new.content[w]]
                w=max(choices)[2];parts.append(w);remaining^=new.content[w]
        else:parts=leaves
        while len(parts)>1:
            pairs=[]
            for i in range(len(parts)):
                for j in range(i+1,len(parts)):
                    a,b=parts[i],parts[j]
                    key=(new.content[a].bit_count()+new.content[b].bit_count(),i,j)
                    if method=='tree_frame':key=(F.dim(F.join(new.frame[a],new.frame[b])),key[0],i,j)
                    pairs.append((key,i,j))
            _,i,j=min(pairs);w=new.sym([parts[i],parts[j]])
            parts=[p for k,p in enumerate(parts) if k not in (i,j)]+[w]
    for t in range(V):new.need[t]={new.key[h.content[u]] for u in h.need[t]}
    return new

def evaluate_word(c):
    masks=[sum(1<<s for s in f) for f in c['frames']]
    dims=[F.dim(m) for m in masks];cur=list(c['start']);H=Counter()
    def move(r,f):
        assert F.inside(masks[cur[r]],masks[f]),('not nested',r,cur[r],f)
        d=dims[f]-dims[cur[r]]
        if d:H[d]+=1
        cur[r]=f
    for phase in ('D','A','B','C'):
        if phase=='B':
            assert all(dims[cur[q]]==8 for q in c['ret'])
            assert all(dims[cur[V+t]]==0 for t in range(V))
        for f,d,srcs in c[phase]:
            assert len(set([d]+srcs))==len([d]+srcs)
            for r in [d]+srcs:move(r,f)
    for r,f in enumerate(c['final']):move(r,f)
    # Complete formal-column identity, including initial dirty values.
    n=2*V+c['R'];val=[1<<r for r in range(n)]
    for phase in ('D','A','B','C'):
        if phase=='B':
            copies=[val[q] for q in c['ret']]
            for t,row in enumerate(c['scatter']):
                for k in row:val[V+t]^=copies[k]
        for _,d,srcs in c[phase]:
            for s in srcs:val[d]^=val[s]
    assert all(value==((1<<r)^(1<<(r-V)) if V<=r<2*V else 1<<r) for r,value in enumerate(val))
    import price
    saving,deficit,entropy=price.price(H,c['R'])
    return dict(saving=saving,R=c['R'],deficit=deficit,entropy=entropy,local_histogram=dict(sorted(H.items())),
                gates={p:len(c[p]) for p in ('D','A','B','C')},columns=n)

def initial(method):
    ham2.P.clear();ham2.P.update(PARAMS)
    h=ham2.build(0,True)
    if method.startswith('tree_'):h=rebuild(h,method)
    W=compiler(method)(h)
    return fullword.build(W)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('method');parser.add_argument('--out',type=Path)
    a=parser.parse_args();start=time.perf_counter()
    c=initial(a.method)
    changes=[]
    if a.method.startswith('retime_') or a.method.startswith('commute_') or a.method=='early_cleanup':
        import retime_e8 as R
        if a.method=='retime_components':c,changes=R.components(c)
        elif a.method.startswith('retime_'):c,changes=R.retime(c,a.method)
        else:c,changes=R.commute(c,a.method.split('_')[-1] if a.method!='early_cleanup' else 'backward',cleanup=a.method=='early_cleanup')
    if a.method=='decoder_basis':
        centres=list(C.default_centres());best_cost=sum(x.bit_count() for x in centres)+sum(len(row) for row in C.decoder(centres))
        for _ in range(3):
            improved=False
            for i in range(9):
                for j in range(9):
                    if i==j:continue
                    trial=centres[:];trial[i]^=trial[j]
                    cost=sum(x.bit_count() for x in trial)+sum(len(row) for row in C.decoder(trial))
                    if cost<best_cost:centres=trial;best_cost=cost;improved=True;changes.append([i,j,cost])
            if not improved:break
        ham2.P.clear();ham2.P.update(PARAMS)
        c=fullword.build(C2.compile2(ham2.build(0,True),centres=centres))
    r=evaluate_word(c);r.update(method=a.method,changes=len(changes),elapsed_seconds=time.perf_counter()-start)
    if a.out:
        a.out.mkdir(parents=True,exist_ok=True);fullword.save(c,str(a.out/'word.json.gz'))
        (a.out/'result.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
        (a.out/'changes.json').write_text(json.dumps(changes,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(r),flush=True)
if __name__=='__main__':main()
