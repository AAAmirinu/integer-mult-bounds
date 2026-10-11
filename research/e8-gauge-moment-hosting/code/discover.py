"""Explore exact-moment-directed nine-stage hosting; floats nominate only.
Usage: discover.py VERIFIED_PR484_VARIANT NEW_OUT
Optional scipy/HiGHS discovery; no optimizer is called by verify.py.
Chafreaky with OpenAI Codex assistance; Apache-2.0.
"""
import gzip,json,math,sys
from pathlib import Path
from collections import Counter
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import milp,linprog,LinearConstraint,Bounds
variant=Path(sys.argv[1]).resolve();root=Path(sys.argv[2]).resolve();assert not root.exists();root.mkdir(parents=True)
word=json.load(gzip.open(variant/'split-centres/CANONICAL-WORD.json.gz'));parent=json.load(gzip.open(variant/'hosted/GLOBAL-TEMPLATE.json.gz'));windows={int(i):(p,r,st) for i,(p,r,st) in parent['hosting']['windows'].items()}
widths=Counter(9-len(word['frames'][f]) for f in word['start'][240:]);avail={(s,w):n for s in range(9) for w,n in sorted(widths.items())};keys=sorted(avail);rows={sw:len(windows)+i for i,sw in enumerate(keys)};wr={i:j for j,i in enumerate(sorted(windows))};rhs=np.array([120]*len(windows)+[avail[sw] for sw in keys]);var=[];ii=[];jj=[];vv=[];cost=[];b=.001326789535340266
c=lambda r:(r/73)**(1-b) if r else 0.
for idx,(_,rank,stages) in sorted(windows.items()):
 def emit(pat,total):
  j=len(var);var.append((idx,tuple(pat)));ii.append(wr[idx]);jj.append(j);vv.append(1);cost.append(8*c(rank-total)+sum(1-c(73-8*w) for _,w in pat))
  for sw in pat:ii.append(rows[sw]);jj.append(j);vv.append(1)
 def visit(k,pat,total):
  emit(pat,total)
  for l in range(k,len(stages)):
   for w in widths:
    if total+w<=rank:visit(l+1,pat+[(stages[l],w)],total+w)
 visit(0,[],0)
 print('patterns',idx,len(var),flush=True)
A=coo_matrix((np.array(vv,dtype=float),(ii,jj)),shape=(len(rhs),len(var))).tocsc();del ii,jj,vv
cost=np.array(cost);lo=np.array([120]*len(windows)+[0]*len(keys));print('SOLVE',len(var),flush=True)
# Integer objective is near a common linear rank term; scale to expose its
# small saving difference without changing the minimizer.
res=milp(cost*1e6,constraints=LinearConstraint(A,lo,rhs),integrality=np.ones(len(var)),bounds=Bounds(0,np.inf),options={'time_limit':180,'mip_rel_gap':1e-10})
print(res.message,'objective',res.fun,flush=True)
assert res.x is not None
x=np.rint(res.x).astype(int);assert np.max(abs(res.x-x))<1e-5 and np.all(A@x>=lo) and np.all(A@x<=rhs)
selection=[[idx,[list(sw) for sw in pat],int(x[j])] for j,(idx,pat) in enumerate(var) if x[j]];left=Counter(avail);profile=Counter({int(r):n*72 for r,n in word['local_profile'].items()})
for idx,pat,n in selection:
 r=windows[idx][1]-sum(w for s,w in pat)
 if r:profile[r]+=8*n
 for s,w in pat:left[s,w]-=n
for e in parent['idle_children']:
 if e['child'] not in windows and e['rank']:profile[e['rank']]+=8
for (s,w),n in left.items():
 assert n>=0
 if n:profile[73-8*w]+=n
W=7680+sum(left.values());mass=sum(r*n for r,n in profile.items());assert 73*W-mass==2496
lower,upper=0.,.01
for _ in range(100):
 mid=(lower+upper)/2
 if sum(n*(r/73)**(1-mid) for r,n in profile.items())<W:lower=mid
 else:upper=mid
summary=dict(status=res.message,patterns=len(var),target_b=b,exploratory_root=lower,live=W,bank_helpers={str(k):n for k,n in left.items() if n},profile=dict(sorted(profile.items())),selected=selection,mip_gap=float(res.mip_gap))
(root/'SCREEN.json').write_text(json.dumps(summary,indent=2)+'\n');(root/'SELECTION.json').write_text(json.dumps({'nine-gauge-moment':dict(rule='one-helper-per-family',patterns=sorted(selection),proxy_saving=0.0)},indent=1)+'\n');print('RESULT',lower,W,dict(sorted(profile.items())),flush=True)
