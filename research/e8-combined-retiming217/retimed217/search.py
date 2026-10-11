"""Greedy literal-gate frame-coordinate optimization at fixed scalar word.
For one gate the paid objective is concave in frame rank, so test both feasible
endpoints: span of preceding touched frames; intersection of following ones.
Fixed retained snapshot labels pin their final A instruction frame.
"""
import sys,json,math,time,copy
from pathlib import Path
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parent));import common as C
c=json.load(open('/private/tmp/pr404-grouped217/constructed/candidate.json'));original=copy.deepcopy(c);alpha=.00101937;chi=lambda r:r*((73/r)**alpha-1) if r else 0
def canonical(vs):
 piv={}
 for x in sorted(vs,reverse=True):
  for k,y in sorted(piv.items(),reverse=True):
   if x>>k&1:x^=y
  if x:
   k=x.bit_length()-1
   for j,y in list(piv.items()):
    if y>>k&1:piv[j]^=x
   piv[k]=x
 return tuple(y for k,y in sorted(piv.items(),reverse=True))
def span(bs):
 S={0}
 for x in bs:S|={y^x for y in S}
 return frozenset(S)
frames=[tuple(f) for f in c['frames']];spans=[span(f) for f in frames];ids={f:i for i,f in enumerate(frames)}
def intern(F):
 F=canonical(F)
 if F not in ids:ids[F]=len(frames);frames.append(F);spans.append(span(F))
 return ids[F]
gates=[(part,i,g,C.gate_roles(g)) for part in ['A','B'] for i,g in enumerate(c[part])];n=len(c['start']);ret={r:f for _,r,f in c['ret']};changes=[];t0=time.time()
for iteration in range(500):
 prev=[];cur=c['start'][:]
 for part,i,g,rs in gates:
  prev.append([cur[r] for r in rs])
  for r in rs:cur[r]=g[1]
 nxt=[None]*len(gates);cur=c['final'][:];pin=set()
 for j in range(len(gates)-1,-1,-1):
  part,i,g,rs=gates[j]
  if part=='A' and (j+1==len(gates) or gates[j+1][0]=='B'):
   for r,f in ret.items():cur[r]=f
   unseen=set(ret)
  if part=='A' and unseen.intersection(rs):pin.add(j);unseen.difference_update(rs)
  nxt[j]=[cur[r] for r in rs]
  for r in rs:cur[r]=g[1]
 best=None
 for j,(part,i,g,rs) in enumerate(gates):
  if j in pin:continue
  old=g[1];df=len(frames[old]);ds=[len(frames[f]) for f in prev[j]];dt=[len(frames[f]) for f in nxt[j]]
  prior=sum(chi(df-a)+chi(b-df) for a,b in zip(ds,dt))
  lower=canonical([x for f in prev[j] for x in frames[f]]);upper=canonical(frozenset.intersection(*(spans[f] for f in nxt[j])))
  assert C.inside(lower,frames[old]) and C.inside(frames[old],upper)
  for F in [lower,upper]:
   dr=len(F)
   if dr==df:continue
   score=sum(chi(dr-a)+chi(b-dr) for a,b in zip(ds,dt))-prior
   if score<-1e-12 and (best is None or score<best[0]):best=(score,j,F)
 if best is None:break
 sc,j,F=best;part,i,g,rs=gates[j];old=g[1];g[1]=intern(F);changes.append(dict(part=part,index=i,old=old,new=g[1],basis=F,score=sc))
 if iteration%10==0:print('ITER',iteration,'score',sc,'gate',part,i,'rank',len(frames[old]),'to',len(F),flush=True)
 c['frames']=[list(f) for f in frames];C.rehist_and_audit(c)
 json.dump(dict(changes=changes,cumulative_score=sum(x['score'] for x in changes),seconds=time.time()-t0),open('/private/tmp/grouped217-frameopt/SEARCH.json','w'),indent=2)
c['frames']=[list(f) for f in frames];C.rehist_and_audit(c);h=C.histogram(c);h.subtract(C.histogram(original));delta={r:n for r,n in h.items() if n};json.dump(c,open('/private/tmp/grouped217-frameopt/candidate.json','w'),sort_keys=True,separators=(',',':'));print('DONE',len(changes),'delta',delta,'score',sum(chi(r)*n for r,n in delta.items()),'seconds',time.time()-t0,flush=True)
