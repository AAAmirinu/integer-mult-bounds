from pathlib import Path
import argparse
parser=argparse.ArgumentParser();parser.add_argument('base',type=Path);parser.add_argument('legal',type=Path);parser.add_argument('output',type=Path);args=parser.parse_args();BASE=args.base;ROOT=Path(__file__).parent
exec((ROOT/'grouped_library.py').read_text().replace("if cm and all(q.denominator", "if p in pivoteligible and cm and all(q.denominator"))
ns={'BASE':BASE};exec((ROOT/'closure_library.py').read_text(),ns);close=ns['close'];newlegal=json.loads(args.legal.read_text());base_score=score
results=[];best=None;exactcache={};tested=0;t0=time.time()
for Es,extra in newlegal.items():
 E=int(Es)
 if not extra:continue
 pivoteligible={r for r in pool if C.inside([E],c['frames'][first[r]])}
 incompatible={x['donor']:x for x in extra};allowed=list(pivoteligible|set(incompatible));dc={r:(incompatible[r]['chi'] if r in incompatible else chi(1)+chi(dim[r]-1)-chi(dim[r])) for r in allowed}
 def score(deps,d):
  D={r for p,cm in deps for r in cm};return sum(chi(dim[p]-1)-chi(dim[p]) for p,cm in deps)+sum(dc[r] for r in D)-.000615953010*len(deps)
 localbest=None
 for tr in range(300):
  rr=allowed[:];rng.shuffle(rr)
  if tr%3==1:rr.sort(key=lambda r:dc[r]+.003*rng.random())
  if tr%3==2:rr.sort(key=lambda r:r in pivoteligible)
  deps=prune(basis_dep(rr),1);tested+=1
  if not deps:continue
  D=tuple(sorted({r for p,cm in deps for r in cm}))
  if not set(D)&set(incompatible) or score(deps,1)>.01:continue
  key=(E,D)
  if key not in exactcache:exactcache[key]=close(E,D)
  delta=exactcache[key]
  if delta is None:continue
  exact=sum(chi(k)*v for k,v in delta.items())+sum(chi(dim[p]-1)-chi(dim[p]) for p,cm in deps)-.000615953010*len(deps)
  if localbest is None or exact<localbest['score']:
   localbest=dict(basis=[E],score=exact,donor_closure_delta=delta,new_incompatible_donors=sorted(set(D)&set(incompatible)),donors=D,pivots=[dict(pivot=p,coefficients={r:str(q) for r,q in cm.items()}) for p,cm in deps])
 if localbest:
  results.append(localbest)
  if localbest['score']<0:print('PROFIT',E,len(localbest['pivots']),len(localbest['donors']),localbest['score'],localbest['new_incompatible_donors'],flush=True)
  if best is None or localbest['score']<best['score']:best=localbest;print('BEST',E,len(best['pivots']),len(best['donors']),best['score'],flush=True)
 json.dump(dict(results=sorted(results,key=lambda z:z['score']),best=best,tested=tested,exactclosures=len(exactcache)),open(args.output,'w'),indent=2)
print('DONE',tested,'exact',len(exactcache),'seconds',time.time()-t0,flush=True)
