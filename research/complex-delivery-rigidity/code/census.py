"""Usage: census.py FULL-WORD.json.gz OUT.json
Register census of a provider word: per register the class, A/B frame chain, gates (reads/writes), readers; per target the chain stops and
what is read at each stop; Phi attribution (r ln(m/r) per climb) per register class. Usage: census.py WORD.json.gz OUT.json"""
import sys,gzip,json,collections,math
from fractions import Fraction as Q
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
W=json.loads(gzip.decompress(open(sys.argv[1],'rb').read()));v=W['report']['v'];R=W['report']['R'];n=2*v+R;m=W['report'].get('m',73)
regs=lambda e:[e[1]]+([e[2]]if e[0]=='add'else[])
cls=lambda r:'src'if r<v else('tgt'if r<2*v else'hlp')
entering=set(map(int,W.get('start_extra',{})));hpe={int(k):tuple(basis(f))for k,f in W.get('helper_final',{}).items()}
centers=set(W['centers'])
cur={r:tuple(basis([W['ports'][r]]))if r<v else()for r in range(n)}
for r,f in W.get('start_extra',{}).items():cur[int(r)]=tuple(basis(f))
phi=lambda d:d*math.log(m/d)if d else 0.0
chain=collections.defaultdict(list)   # r -> [(phase, gate index, frame, dim, role)]
climbs=collections.defaultdict(list)  # r -> [(from dim,to dim,phase)]
Phi=collections.Counter();readers=collections.defaultdict(set);writes=collections.defaultdict(list)
for part in('A','B'):
    for i,e in enumerate(W[part]):
        f=tuple(basis(e[-1]))
        for r in regs(e):
            if cur[r]!=f:
                assert basis(list(cur[r])+list(f))==f,(r,cur[r],f)
                climbs[r].append((len(cur[r]),len(f),part));Phi[cls(r)]+=phi(len(f)-len(cur[r]));cur[r]=f
            chain[r].append((part,i,f,len(f),'dst'if r==e[1]else'src'))
        if e[0]=='add':
            readers[e[2]].add(e[1]);writes[e[1]].append((part,i,e[2],Q(e[3],e[4]),len(f)))
endB=dict(cur)
# final climbs
FULL=tuple(basis([1<<i for i in range(9)]))
final={r:(FULL if r>=2*v else tuple(basis([x for x in range(1,512)if not(x&W['ports'][r-v]).bit_count()%2]))if r>=v else FULL)for r in range(n)}
for r,f in hpe.items():final[r]=f
# tail (early cleanup) climbs for hpe helpers happen at frames given; approximate: climb to final
for r in range(n):
    if len(final[r])>len(cur[r]):climbs[r].append((len(cur[r]),len(final[r]),'final'));Phi[cls(r)+'_final']+=phi(len(final[r])-len(cur[r]))
tot=sum(Phi.values())
print('Phi by class:',{k:round(x)for k,x in Phi.items()},'total',round(tot))
# helper categories
cat=collections.Counter()
for r in range(2*v,n):
    rd=readers[r];kind=('none'if not rd else'tgt-only'if all(v<=x<2*v for x in rd)else'hlp-only'if all(x>=2*v for x in rd)else'mixed')
    cat[(kind,'entering'if r in entering else'cold','hpe'if r in hpe else'full')]+=1
print('helpers by (readers, entrance, end):');[print('  ',k,c)for k,c in sorted(cat.items())]
# per target chain
tch={}
for t in range(v):
    r=v+t;stops=[]
    for part,i,f,d,role in chain[r]:
        e=W[part][i];src=e[2]if e[0]=='add'else None
        stops.append(dict(phase=part,i=i,dim=d,src=src,srccls=cls(src)if src is not None else None,coef=[e[3],e[4]]if e[0]=='add'else[e[2],e[3]]))
    tch[t]=stops
dims=collections.Counter(tuple(c[1]for c in climbs[v+t])for t in range(v))
print('target climb chains (dims):',dims.most_common(6))
print('target reads by source class/dim:',collections.Counter((s['srccls'],s['dim'])for t in tch for s in tch[t]if s['src']is not None).most_common(20))
# per helper summary
H={}
for r in range(2*v,n):
    H[r]=dict(entering=r in entering,ent_dim=len(basis(W['start_extra'][str(r)]))if r in entering else 0,endB=len(endB[r]),final=len(final[r]),climbs=climbs[r],
      phi=sum(phi(b-a)for a,b,_ in climbs[r]),readers=sorted(readers[r]),nreads=sum(1 for part,i,f,d,role in chain[r]if role=='src'),nwrites=len(writes[r]),
      gates=[(part,i,d,role,(W[part][i][2]if role=='dst'else W[part][i][1]))for part,i,f,d,role in chain[r]])
json.dump(dict(targets=tch,helpers={str(k):dict(x,climbs=[list(c)for c in x['climbs']])for k,x in H.items()},Phi=dict(Phi)),open(sys.argv[2],'w'))
hp=sorted(H.values(),key=lambda x:-x['phi'])
print('helper phi: mean',round(sum(x['phi']for x in H.values())/R,2),'max',round(hp[0]['phi'],1),'min',round(hp[-1]['phi'],1))
print('helper climb-step count distribution:',collections.Counter(len(x['climbs'])for x in H.values()))
