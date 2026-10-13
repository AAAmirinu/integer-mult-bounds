"""Usage: tolerance.py PROTOTYPE.json ROLES.json OUT.json
Pollution tolerance: for every (key, consumer block) incidence and every foreign/own target x consuming the key, at which stage of x's
chain (S1 own, S2 own+selected faces, S3 post-butterfly) is x's frame inside the caps of ALL 4 consumers of that incidence?"""
import json,itertools as it,collections
import sys
PR=json.load(open(sys.argv[1]));R=PR['root_lines'];ROL=json.load(open(sys.argv[2]));P=ROL['ports'];G=ROL['G'];OUTF=sys.argv[3]
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
blocks={tuple(json.loads(k.replace('(','[').replace(')',']'))):v for k,v in ROL['blocks'].items()}
own={int(t):tuple(F) for t,(r,c,F) in ROL['own_rows'].items()}
face=lambda d,p,e:[s for s in blocks[d]['sources'] if R[s][p[0]]*R[s][p[1]]==e]
fspan=lambda d,p,e:basis([P[s] for s in face(d,p,e)])
cap={t:hyper(P[t]) for c in blocks for t in blocks[c]['sources']}
tet={};blk={}
for c,z in blocks.items():
    for i,T in enumerate(z['tetrads']):
        for t in T:tet[t]=i;blk[t]=c
def parts(c):c=sorted(c);return [((c[0],c[1]),(c[2],c[3])),((c[0],c[2]),(c[1],c[3])),((c[0],c[3]),(c[1],c[2]))]
SEL=0
def eps(x,p):return R[x][p[0]]*R[x][p[1]]
def consumers(c,p,e):return [t for t in blocks[c]['sources'] if eps(t,p)==e]
# target stages
def partner(x):  # same tetrad, agrees on selected partition
    c=blk[x];p,q=parts(c)[SEL]
    return next(u for u in blocks[c]['tetrads'][tet[x]] if u!=x and eps(u,p)==eps(x,p) and eps(u,q)==eps(x,q))
def selfaces(x):
    c=blk[x];out=[]
    for p in parts(c)[SEL]:
        ds=[d for d in blocks if d!=c and set(p)<=set(d)]
        for d in ds:out+=list(fspan(d,p,eps(x,p)))
    return out
stage={}
for x in cap:
    u=partner(x)
    S1=basis(own[x]);S2=basis(list(own[x])+selfaces(x));S3=basis(list(own[x])+list(own[u])+selfaces(x)+selfaces(u))
    stage[x]=dict(S1=S1,S2=S2,S3=S3,partner=u)
print('stage dims (S1,S2,S3) distribution:',collections.Counter((len(v['S1']),len(v['S2']),len(v['S3'])) for v in stage.values()))
# incidences
tol=collections.Counter();detail=collections.defaultdict(list)
for c in blocks:
    for pi,(p,q) in enumerate(parts(c)):
        for pr in (p,q):
            for e in(-1,1):
                cons=consumers(c,pr,e);assert len(cons)==4
                selected=(pi==SEL)
                # foreign targets consuming key (pr,e): targets in the other two blocks containing pr
                others=[d for d in blocks if d!=c and set(pr)<=set(d)]
                foreign=[t for d in others for t in blocks[d]['sources'] if eps(t,pr)==e]
                for x in foreign+cons:
                    kind='own-block' if x in cons else 'foreign'
                    for k in('S1','S2','S3'):
                        ok=all(inside(stage[x][k],cap[y]) for y in cons)
                        tol[(selected,kind,k,ok)]+=1
                        if ok:detail[(c,pr,e)].append((x,k,kind))
for k in sorted(tol):print(k,tol[k])
# per non-selected incidence: number of foreign targets tolerated at S3 (post-BF) and at S2
cnt=collections.Counter()
for c in blocks:
    for pi,(p,q) in enumerate(parts(c)):
        if pi==SEL:continue
        for pr in(p,q):
            for e in(-1,1):
                d=detail[(c,pr,e)]
                cnt[(sum(1 for x,k,kind in d if k=='S3' and kind=='foreign'),sum(1 for x,k,kind in d if k=='S2' and kind=='foreign'),sum(1 for x,k,kind in d if k=='S1' and kind=='foreign'))]+=1
print('non-selected incidences: (#foreign tolerated at S3, at S2, at S1):',sorted(cnt.items()))

json.dump(dict(stage_dims=sorted(collections.Counter((len(v['S1']),len(v['S2']),len(v['S3'])) for v in stage.values()).items()),tolerance={str(k):v for k,v in sorted(tol.items())},nonselected_incidences={str(k):v for k,v in sorted(cnt.items())},tolerated=[[str(k),v] for k,v in detail.items()]),open(OUTF,'w'))
