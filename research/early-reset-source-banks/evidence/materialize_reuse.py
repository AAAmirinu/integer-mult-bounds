import json,math,hashlib,sys
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
O=Path('/private/tmp/pr433-bit-retiming');base=json.loads((O/'base/bit426-source-centres/bit-source-centres.json').read_text());F=[set(f) for f in base['frames']]
# exact dimensions from exported original root data
L=base['lines']
def rank(ids):
 p={}
 for i in ids:
  v=list(map(Q,L[i]))
  for j,b in sorted(p.items()):
   if v[j]:q=v[j];v=[x-q*y for x,y in zip(v,b)]
  j=next((j for j,x in enumerate(v) if x),None)
  if j is not None:q=v[j];p[j]=[x/q for x in v]
 return len(p)
dim=list(map(rank,base['frames']))

def materialize(c,z):
 # New helper s aliases retired helper r only after an exact, explicitly billed
 # reset at an earlier boundary. Rebuild all dirty response and inverse cleanup.
 c=json.loads(json.dumps(c));r=z['retired_helper'];s=z['new_helper'];assert r!=s
 c[z['reset_part']].insert(z['reset_after_gate']+1,[z['frame'],r,z['reset_donors']])
 def alias(q):return r if q==s else q
 for p in ('A','B'):
  c[p]=[[f,alias(d),[alias(q) for q in ss]] for f,d,ss in c[p]]
 physical=[q for q in range(240+c['R']) if q!=s];idx={q:j for j,q in enumerate(physical)}
 for p in ('A','B'):
  c[p]=[[f,idx[d],[idx[q] for q in ss]] for f,d,ss in c[p]]
 c['R']-=1;c['start']=[c['start'][q] for q in physical];c['final']=[c['final'][q] for q in physical];c['ret']=[idx[q] for q in c['ret']]
 c['C']=[[1,d,ss] for f,d,ss in reversed(c['A']+c['B']) if d>=240]
 n=240+c['R'];val=[(1<<r) if r>=240 else 0 for r in range(n)]
 def go(gs):
  for f,d,ss in gs:
   assert d not in ss and len(ss)==len(set(ss))
   for s in ss:val[d]^=val[s]
 go(c['A']);cp=[val[q] for q in c['ret']]
 for t,ss in enumerate(c['scatter']):
  for j in ss:val[120+t]^=cp[j]
 go(c['B']);c['D']=[]
 for t in range(120):
  bits=val[120+t];ss=[j for j in range(240,n) if bits>>j&1]
  assert bits==sum(1<<j for j in ss)
  if ss:c['D'].append([0,120+t,ss])
 # Every free input column and every frame incidence.
 val=[1<<r for r in range(n)];cur=c['start'].copy();H=Counter({8:9})
 def main(gs):
  for f,d,ss in gs:
   assert d not in ss and len(ss)==len(set(ss))
   for r in [d]+ss:
    assert F[cur[r]]<=F[f],(r,cur[r],f)
    rank=dim[f]-dim[cur[r]]
    if rank:H[rank]+=1
    cur[r]=f
   for s in ss:val[d]^=val[s]
 main(c['D']);main(c['A']);cp=[val[q] for q in c['ret']]
 assert all(cur[q]==1 for q in c['ret']) and all(cur[q]==0 for q in range(120,240))
 for t,ss in enumerate(c['scatter']):
  for j in ss:val[120+t]^=cp[j]
 main(c['B']);main(c['C'])
 for r,f in enumerate(c['final']):
  assert F[cur[r]]<=F[f]
  if dim[f]>dim[cur[r]]:H[dim[f]-dim[cur[r]]]+=1
 want=[1<<r for r in range(n)]
 for t in range(120):want[120+t]^=1<<t
 assert val==want
 return c,H

if __name__=='__main__':
 candidates=json.loads((O/'EARLY-RESET-CANDIDATES.json').read_text())['candidates'];best=None;hits=[]
 for k,z in enumerate(candidates):
  try:c,H=materialize(base,z)
  except AssertionError as e:raise AssertionError((k,z,str(e)))
  # Compare at the present accepted coarse c. Lower normalized full64 moment
  # with the actual reduced live stock is a valid discovery objective.
  G=Counter({r:72*n for r,n in H.items()});G.update({7:5760,14:3840,28:3840,42:3840});W=7680+9*c['R'];assert 64*W-sum(r*n for r,n in G.items())==2496
  b=.001122122700265139;score=sum(r*n/(64*W)*(64/r)**b for r,n in G.items())+32*64*sum(G.values())/(10**16*W)*64**b
  if best is None or score<best[0]:
   best=(score,k,z,c,H);print('best',k,'score',score,'r',z['retired_helper'],'s',z['new_helper'],'reset',len(z['reset_donors']),'H',dict(sorted(H.items())),flush=True)
  hits.append({'candidate':k,'score_at_old_c':score,'local_profile':dict(sorted(H.items()))})
 score,k,z,c,H=best;blob=json.dumps(c,sort_keys=True,separators=(',',':')).encode();(O/'bit-r757.json').write_bytes(blob)
 (O/'REUSE-BEST.json').write_text(json.dumps({'status':'ONE_EARLY_RESET_FULL_LOCAL_PASS_NOT_GLOBAL_ADMITTED','candidate':k,'selection':z,'candidate_sha256':hashlib.sha256(blob).hexdigest(),'local_profile':dict(sorted(H.items())),'score_at_old_c':score,'searched':len(hits)},indent=2)+'\n')
 (O/'REUSE-ALL-LOCAL.json').write_text(json.dumps(hits)+'\n')
