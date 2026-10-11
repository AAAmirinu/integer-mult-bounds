"""Check a fixed-word packing dual using rational arithmetic only; no optimizer."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import copy,gzip,hashlib,importlib.util,itertools,json,sys
base,certificate,out=map(Path,sys.argv[1:]);assert not out.exists()
read=lambda p:json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def mod(n):
 s=importlib.util.spec_from_file_location(n,base/'work/pr361/code/engines'/(n+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M,O=mod('moment'),mod('base_two_moment');checks=read(base/'split-centres/LOCAL-CHECKS.json');canon=read(base/'split-centres/CANONICAL-WORD.json.gz');parent=read(base/'split-centres/GLOBAL-TEMPLATE.json.gz')
assert checks['forward']['paid_profile']==checks['backward']['paid_profile'];local={int(r):72*n for r,n in checks['forward']['paid_profile'].items()};widths=Counter(9-len(canon['frames'][canon['start'][240+h]])for h in range(560));stock=Counter()
for e in parent['idle_children']:stock[e['rank']]+=e['replicas']
ws=sorted(widths);rs=sorted(stock);patterns=[]
for r in rs:
 for p in itertools.product(*(range(r//w+1)for w in ws)):
  left=r-sum(n*w for w,n in zip(ws,p))
  if left>=0:patterns.append((r,p,left))
rest=sum(r*n for r,n in stock.items())-72*sum(w*n for w,n in widths.items());assert rest==64944 and sum(r*n for r,n in local.items())+rest==73*7680-2496

def check(z):
 assert z['calls']==72 and z['patterns']==len(patterns)==112
 assert {int(r):n for r,n in z['rank_stock'].items()}==stock and {int(w):n for w,n in z['helper_widths'].items()}==widths
 assert z['remainder_mass']==rest
 for file,h in z['source_artifacts'].items():assert hashlib.sha256((base/file).read_bytes()).hexdigest()==h
 b=Q(z['rejected_b']);assert 0<b<Q(1,100)and Q(z['kappa_upper'])==b/(1+b)
 eta={int(r):Q(v)for r,v in z['dual_rank'].items()};lam={int(w):Q(v)for w,v in z['dual_width'].items()};assert set(eta)==set(rs)and set(lam)==set(ws)
 cost={0:Q(0)}
 for r in sorted({left for rr,p,left in patterns}-{0}):
  ml,_=M.moment({r:1},73,7680,b,True);ol,_=O.moment(73,7680,[(r,1)],b);fl,_=O.moment(73,7680,[(1,32*73**2)],b)
  cost[r]=min(ml,ol+fl/10**16)*73*7680-r
 slacks=[cost[left]-eta[r]-sum(lam[w]*n for w,n in zip(ws,p))for r,p,left in patterns]
 assert min(slacks)>=0 and str(min(slacks))==z['min_exact_dual_slack']
 contribution=(rest+sum(stock[r]*eta[r]for r in rs)+sum(72*widths[w]*lam[w]for w in ws))/(73*7680)
 fixed=M.moment(local,73,7680,b,True)[0];other=O.moment(73,7680,list(local.items()),b)[0]+O.moment(73,7680,[(1,32*73**2*sum(local.values()))],b)[0]/10**16
 margins=[fixed+contribution-1,other+contribution-1];assert min(margins)>0
 assert list(map(str,margins))==[z['mercator_rejection_margin'],z['base_two_rejection_margin']]
 return dict(patterns_checked=len(patterns),margins=list(map(str,margins)),kappa_upper=z['kappa_upper'])
z=read(certificate);result=check(z);controls=[]
def reject(name,change):
 q=copy.deepcopy(z);change(q)
 try:check(q)
 except(AssertionError,KeyError):controls.append(name)
 else:raise AssertionError(name)
reject('increase rank dual beyond feasibility',lambda q:q['dual_rank'].__setitem__('8',str(Q(q['dual_rank']['8'])+1)))
reject('understate rank stock',lambda q:q['rank_stock'].__setitem__('48',q['rank_stock']['48']-1))
reject('wrong whole helper width inventory',lambda q:q['helper_widths'].__setitem__('9',q['helper_widths']['9']-1))
reject('claim smaller outer ceiling',lambda q:q.__setitem__('kappa_upper',str(Q(q['kappa_upper'])-Q(1,10**9))))
reject('omit one finite pattern',lambda q:q.__setitem__('patterns',111))
result.update(status='PASS_EXACT_PACKING_DUAL_AND_FIVE_CONTROLS',certificate_sha256=hashlib.sha256(certificate.read_bytes()).hexdigest(),mutations_rejected=controls,scope=z['scope']);out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],flush=True)
