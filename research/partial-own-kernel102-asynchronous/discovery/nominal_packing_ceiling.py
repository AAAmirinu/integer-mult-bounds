"""Nominate a dual, then certify every inequality with exact interval costs.
Ignores time, invocation conflicts and coordinate charts: an optimistic packing
relaxation of this fixed local word only. No solver status is trusted as proof.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import gzip,hashlib,importlib.util,itertools,json,math,sys
import numpy as np
from scipy.optimize import linprog
base,out,nomfile=map(Path,sys.argv[1:]);assert not out.exists()
read=lambda p:json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def mod(n):
 s=importlib.util.spec_from_file_location(n,base/'work/pr361/code/engines'/(n+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M,O=mod('moment'),mod('base_two_moment');checks=read(base/'split-centres/LOCAL-CHECKS.json');canon=read(base/'split-centres/CANONICAL-WORD.json.gz');parent=read(base/'split-centres/GLOBAL-TEMPLATE.json.gz')
assert checks['forward']['paid_profile']==checks['backward']['paid_profile'];local={int(r):72*n for r,n in checks['forward']['paid_profile'].items()};widths=Counter(9-len(canon['frames'][canon['start'][240+h]])for h in range(560));stock=Counter()
for e in parent['idle_children']:stock[e['rank']]+=e['replicas']
nomination=read(nomfile);local={int(r):72*n for r,n in nomination['profile'].items()};widths=Counter({int(w):n for w,n in nomination['widths'].items()});assert sum(widths.values())==560
ws=sorted(widths);rs=sorted(stock);variables=[]
for r in rs:
 for p in itertools.product(*(range(r//w+1)for w in ws)):
  used=sum(n*w for w,n in zip(ws,p))
  if used<=r:variables.append((r,p,r-used))
A=np.array([[int(r==rr)for r,p,left in variables]for rr in rs]+[[p[i]for r,p,left in variables]for i in range(len(ws))],dtype=float);rhs=np.array([stock[r]for r in rs]+[72*widths[w]for w in ws],dtype=float)
rest=sum(r*n for r,n in stock.items())-72*sum(w*n for w,n in widths.items());assert sum(r*n for r,n in local.items())+rest==73*7680-2496

def solve(b):
 def cost(r):return r*math.expm1(b*math.log(73/r))+32*73**2/10**16*math.exp(b*math.log(73))if r else 0
 c=np.array([cost(left)for r,p,left in variables]);res=linprog(c,A_eq=A,b_eq=rhs,bounds=(0,None),method='highs');assert res.success
 localcost=sum(n*(r+cost(r))for r,n in local.items());return (localcost+rest+res.fun)/(73*7680),res
lo,hi=0.00130,0.00146
for _ in range(24):
 b=(lo+hi)/2;v,_=solve(b)
 if v>1:hi=b
 else:lo=b
b=Q(math.ceil(hi*10**10)+2,10**10);_,nom=solve(float(b));lambdas=[Q(round(float(z)*10**12),10**12)for z in nom.eqlin.marginals[len(rs):]]
# Each cost is a rigorous LOWER bound on residual moment numerator minus rank,
# including the inherited count-linear fallback. Use BOTH engines' lower bounds.
cost={0:Q(0)}
for r in sorted({x[2]for x in variables}-{0}):
 ml,mh=M.moment({r:1},73,7680,b,True);ol,oh=O.moment(73,7680,[(r,1)],b);fl,fh=O.moment(73,7680,[(1,32*73**2)],b)
 cost[r]=min(ml,ol+fl/10**16)*73*7680-r
eta={r:min(cost[left]-sum(l*n for l,n in zip(lambdas,p))for rr,p,left in variables if rr==r)for r in rs}
slacks=[cost[left]-eta[r]-sum(l*n for l,n in zip(lambdas,p))for r,p,left in variables];assert min(slacks)>=0
fixed=M.moment(local,73,7680,b,True)[0];other=O.moment(73,7680,list(local.items()),b)[0]+O.moment(73,7680,[(1,32*73**2*sum(local.values()))],b)[0]/10**16
bound=(rest+sum(stock[r]*eta[r]for r in rs)+sum(72*widths[w]*l for w,l in zip(ws,lambdas)))/(73*7680)
assert fixed+bound>1 and other+bound>1
result=dict(status='EXACT_DUAL_REJECTS_FIXED_WORD_PACKING_RATE',rejected_b=str(b),rejected_b_decimal=M.decimal(b),kappa_upper=str(b/(1+b)),kappa_upper_decimal=M.decimal(b/(1+b)),rank_stock=dict(stock),helper_widths=dict(widths),calls=72,remainder_mass=rest,patterns=len(variables),dual_rank={str(r):str(v)for r,v in eta.items()},dual_width={str(w):str(v)for w,v in zip(ws,lambdas)},min_exact_dual_slack=str(min(slacks)),mercator_rejection_margin=str(fixed+bound-1),base_two_rejection_margin=str(other+bound-1),nomination_sha256=hashlib.sha256(nomfile.read_bytes()).hexdigest(),rank_stock_source_sha256=hashlib.sha256((base/'split-centres/GLOBAL-TEMPLATE.json.gz').read_bytes()).hexdigest(),scope='UNADMITTED structural candidate profile from the hashed nomination. Conditional exclusion only if that profile and width inventory hold:72calls,m73,W7680,deficit2496 and unchanged idle ranks; whole helpers assigned once each, one remainder per original idle child. Drops all time, owner-conflict and chart restrictions. Does not bound changed local words, split-child contracts or all algorithms.')
out.write_text(json.dumps(result,indent=2)+'\n');print(result['rejected_b_decimal'],result['kappa_upper_decimal'],len(variables),flush=True)
