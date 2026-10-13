"""Usage: blockdata.py ROLES.json PROTOTYPE.json OUT.json
Per-block delivery data from ROLES.json (raw 240-register numbering): targets, 12 keys, M sources, consumers, cap containment,
own-row sources and their containment. Writes blocks.json."""
import json,itertools as it,collections,sys
from fractions import Fraction as Q
ROL=json.load(open(sys.argv[1]));P=ROL['ports'];R=json.load(open(sys.argv[2]))['root_lines'];OUTF=sys.argv[3]
def basis(vs):
    b={}
    for x in vs:
        for p in sorted(b,reverse=True):
            if x>>p&1:x^=b[p]
        if x:
            p=x.bit_length()-1
            for q in b:
                if b[q]>>p&1:b[q]^=x
            b[p]=x
    return tuple(b[p]for p in sorted(b,reverse=True))
inside=lambda a,b:basis(list(a)+list(b))==tuple(b)
hyper=lambda p:basis([x for x in range(1,512)if(x&p).bit_count()%2==0])
G=ROL['G']
blocks={tuple(json.loads(k.replace('(','[').replace(')',']'))):v for k,v in ROL['blocks'].items()}
rows={int(r):{int(s):Q(x)for s,x in d.items()}for r,d in ROL['rows'].items()}
own={int(t):(r,Q(c),tuple(F))for t,(r,c,F)in ROL['own_rows'].items()}
# root line signs from G? we need R[s][i]; reconstruct sign vectors from ROLES? not stored; derive eps via faces: use packets rows.
packets={}
for k,(r,a)in ROL['packets'].items():
    c,p,eps,d=eval(k);packets[(tuple(c),tuple(p),eps,tuple(d))]=(r,Q(a))
sel={}
for pr in ROL['pairs']:
    for k in pr['keys']:sel[(tuple(k[0]),tuple(k[1]),k[2])]=pr['selected']
out={}
stats=collections.Counter()
for c,z in sorted(blocks.items()):
    ids=z['sources'];keys=[(p,e)for p in it.combinations(c,2)for e in(-1,1)]
    others=[d for d in blocks if d!=c]
    K={}
    for p,e in keys:
        ds=sorted(d for d in others if set(p)<=set(d));assert len(ds)==2
        src=set()
        for d in ds:
            src|={s for s in blocks[d]['sources'] if R[s][p[0]]*R[s][p[1]]==e}
        assert len(src)==8,(c,p,e,len(src))
        span=basis([P[s]for s in src])
        K[(p,e)]=dict(sources=sorted(src),span=span,dim=len(span),selected=sel[(c,p,e)])
    T={}
    for x in ids:
        cap=hyper(P[x]);cons=[(p,e)for(p,e)in keys if all(G[x][s]!=0 for s in K[(p,e)]['sources'])]
        contain=[(p,e)for(p,e)in keys if inside(K[(p,e)]['span'],cap)]
        anyG=[(p,e)for(p,e)in keys if any(G[x][s]!=0 for s in K[(p,e)]['sources'])]
        stats['cons==contain']+=cons==contain;stats['cons!=contain']+=cons!=contain;stats['partial G']+=len(set(anyG)-set(cons))
        r,cf,F=own[x];osrc=sorted(rows[r]);
        T[x]=dict(cap=cap,cons=cons,contain=contain,own_reg=r,own_sources=osrc,own_frame=F,own_in_cap={y:inside(F,hyper(P[y]))for y in ids},
                  tetrad=0 if x in z['tetrads'][0]else 1)
    out[str(c)]=dict(sources=ids,keys=[[list(p),e]for p,e in keys],K={str((list(p),e)):dict(v,span=list(v['span']))for(p,e),v in K.items()},
                     T={str(x):dict(v,cap=list(v['cap']),cons=[[list(p),e]for p,e in v['cons']],contain=[[list(p),e]for p,e in v['contain']],own_in_cap={str(k):b for k,b in v['own_in_cap'].items()})for x,v in T.items()})
print(stats)
c0=sorted(blocks)[0];b=out[str(c0)]
print('block',c0,'keys dims',[v['dim']for v in b['K'].values()],'selected',[v['selected']for v in b['K'].values()])
for x,v in b['T'].items():print(' target',x,'tetrad',v['tetrad'],'cons',len(v['cons']),'contain',len(v['contain']),'own sources',v['own_sources'],'own frame dim',len(v['own_frame']),'own in caps of',sum(v['own_in_cap'].values()),'/8')
# pairwise common consumption
xs=list(b['T']);import itertools
cm=collections.Counter()
for x,y in itertools.combinations(xs,2):
    a=set(map(str,b['T'][x]['cons']));bb=set(map(str,b['T'][y]['cons']));cm[(b['T'][x]['tetrad']==b['T'][y]['tetrad'],len(a&bb))]+=1
print('pairwise (same tetrad, |common cons|):',sorted(cm.items()))
json.dump(out,open(OUTF,'w'))
