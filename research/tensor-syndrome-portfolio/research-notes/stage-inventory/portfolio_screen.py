from pathlib import Path
from collections import Counter
import sys,json,math
sys.dont_write_bytecode=True
K=int(sys.argv[1]);T=int(sys.argv[2]);L=2*K+1;M=1+7*L;O=Path(__file__).parent
d=json.loads(Path(sys.argv[3]).read_text());profile={int(r):n for r,n in d['local_profile'].items()};widths={int(r):n for r,n in d['width_counts'].items()};label=d.get('label','candidate');variants=d.get('variants',[])
av={w:widths.get(w,0)*T for w in sorted(set(widths)|{int(w)for v in variants for w in v['width_delta']})};win={}
for j in range(1,K):win[2*(j-1)]=(j,14*j,list(range(2*j)));win[2*(j-1)+1]=(j,7,[2*j])
for j in range(K-1):win[2*(K-1)+j]=(j,14*(K-1-j),list(range(2*j+3,L)))
def patterns(r):
 ws=sorted(av,reverse=True);out=[]
 def rec(j,left,p):
  if j==len(ws):out.append(tuple(p));return
  for n in range(left//ws[j]+1):rec(j+1,left-n*ws[j],p+[ws[j]]*n)
 rec(0,r,[]);return out
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
keys=[];col={}
def var(k):col[k]=len(keys);keys.append(k)
for i,(pair,r,ss)in win.items():
 for p in patterns(r):var(('y',i,p))
 for s in ss:
  for w in av:var(('z',i,s,w))
for ss in range(L):
 for vi,vv in enumerate(variants):var(('variant',ss,vi))
n=len(keys);c=np.zeros(n);rows=[];cols=[];vals=[];lo=[];hi=[]
def row(es,l,h):
 k=len(lo)
 for j,v in es:
  if v:rows.append(k);cols.append(j);vals.append(v)
 lo.append(l);hi.append(h)
cost=lambda r:r*math.log(M/r)if r else 0
for i,(pair,r,ss)in win.items():
 ps=patterns(r)
 for p in ps:c[col['y',i,p]]=cost(r-sum(p))
 row([(col['y',i,p],1)for p in ps],240*T,240*T)
 for w in av:row([(col['y',i,p],p.count(w))for p in ps]+[(col['z',i,s,w],-1)for s in ss],0,0)
for s in range(L):
 for w,nn in av.items():row([(col['z',i,s,w],1)for i,(_,_,ss)in win.items()if s in ss]+[(col['variant',s,vi],-vv['width_delta'].get(str(w),0))for vi,vv in enumerate(variants)],nn,nn)
 if variants:row([(col['variant',s,vi],1)for vi in range(len(variants))],0,T)
 for vi,vv in enumerate(variants):c[col['variant',s,vi]]=sum(n*cost(int(r))for r,n in vv['profile_delta'].items())
a=coo_matrix((vals,(rows,cols)),shape=(len(lo),n)).tocsr();res=milp(c,integrality=np.ones(n),bounds=Bounds(0,np.inf),constraints=LinearConstraint(a,lo,hi),options=dict(time_limit=25,mip_rel_gap=1e-8));assert res.x is not None
z=[round(t)for t in res.x];assert all(l-1e-7<=q<=h+1e-7 for q,l,h in zip(a@z,lo,hi))
ys=[[i,list(p),z[j]]for k,j in col.items()if k[0]=='y'for _,i,p in[k]if z[j]];zs=[[i,w,s,z[j]]for k,j in col.items()if k[0]=='z'for _,i,s,w in[k]if z[j]];hist=Counter()
for i,p,nn in ys:
 if win[i][1]>sum(p):hist[win[i][1]-sum(p)]+=nn
full=Counter({r:L*T*nn for r,nn in profile.items()});full.update(hist)
selected=[[ss,vi,z[col['variant',ss,vi]]]for ss in range(L)for vi in range(len(variants))if z[col['variant',ss,vi]]]
for ss,vi,nn in selected:full.update({int(r):nn*vv for r,vv in variants[vi]['profile_delta'].items()})
live=2*K*120*T;mass=sum(r*nn for r,nn in full.items());D=M*live-mass
lo_b,hi_b=0.,.01
for _ in range(60):
 b=(lo_b+hi_b)/2
 if sum(nn*(r/M)**(1-b)for r,nn in full.items())<live:lo_b=b
 else:hi_b=b
out=dict(status='EXACT_INTEGER_FEASIBLE_NATIVE_NOMINATION_ONLY',label=label,K=K,L=L,T=T,m=M,live=live,windows=win,variant_selection=selected,input=d,patterns=ys,stages=zs,width_counts=dict(widths),local_profile=profile,remainder=dict(sorted(hist.items())),profile=dict(sorted(full.items())),rank_mass=mass,deficit=D,native_status=int(res.status),native_gap=float(res.mip_gap),entropy_objective=float(res.fun),numeric_saving=lo_b)
assert D==(48*L-120)*T
(O/f'{label}-K{K}-T{T}.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items()if k not in ['patterns','stages','windows','input']}))
