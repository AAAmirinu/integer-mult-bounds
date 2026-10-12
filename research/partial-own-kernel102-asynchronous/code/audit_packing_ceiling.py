"""Recheck a fixed-word packing dual with both exact engines, without a solver."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as Q
import gzip,hashlib,importlib.util,itertools,json,sys
base,certificate,nomination,out=map(Path,sys.argv[1:]);assert not out.exists()
read=lambda p:json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
cert=read(certificate);nom=read(nomination);checks=read(base/'split-centres/LOCAL-CHECKS.json');canon=read(base/'split-centres/CANONICAL-WORD.json.gz');parent=read(base/'split-centres/GLOBAL-TEMPLATE.json.gz')
assert checks['forward']['paid_profile']==checks['backward']['paid_profile']==nom['profile']
assert cert['nomination_sha256']==hashlib.sha256(nomination.read_bytes()).hexdigest()
assert nom['word_sha256']==hashlib.sha256((base/'split-centres/FULL-WORD.json.gz').read_bytes()).hexdigest()
widths=Counter(9-len(canon['frames'][canon['start'][240+h]])for h in range(560));stock=Counter()
for e in parent['idle_children']:stock[e['rank']]+=e['replicas']
assert dict(widths)=={int(k):v for k,v in cert['helper_widths'].items()}=={int(k):v for k,v in nom['widths'].items()}
assert dict(stock)=={int(k):v for k,v in cert['rank_stock'].items()}
assert cert['calls']==72
ws=sorted(widths);patterns=[]
for r in sorted(stock):
 for counts in itertools.product(*(range(r//w+1)for w in ws)):
  left=r-sum(w*n for w,n in zip(ws,counts))
  if left>=0:patterns.append((r,counts,left))
assert len(patterns)==cert['patterns']==112
local={int(r):72*n for r,n in checks['forward']['paid_profile'].items()};rest=sum(r*n for r,n in stock.items())-72*sum(w*n for w,n in widths.items());assert rest==cert['remainder_mass']
assert sum(r*n for r,n in local.items())+rest==73*7680-2496

def module(name):
 spec=importlib.util.spec_from_file_location(name,base/'work/pr361/code/engines'/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
M,O=module('moment'),module('base_two_moment');b=Q(cert['rejected_b']);lambdas={int(k):Q(v)for k,v in cert['dual_width'].items()};eta={int(k):Q(v)for k,v in cert['dual_rank'].items()};cost={0:Q(0)}
for r in sorted({left for rank,counts,left in patterns}-{0}):
 ml,_=M.moment({r:1},73,7680,b,True);ol,_=O.moment(73,7680,[(r,1)],b);fl,_=O.moment(73,7680,[(1,32*73**2)],b)
 cost[r]=min(ml,ol+fl/10**16)*73*7680-r
slacks=[cost[left]-eta[rank]-sum(lambdas[w]*n for w,n in zip(ws,counts))for rank,counts,left in patterns];assert min(slacks)>=0
bound=(rest+sum(stock[r]*eta[r]for r in stock)+sum(72*widths[w]*lambdas[w]for w in ws))/(73*7680)
fixed=M.moment(local,73,7680,b,True)[0];other=O.moment(73,7680,list(local.items()),b)[0]+O.moment(73,7680,[(1,32*73**2*sum(local.values()))],b)[0]/10**16
assert fixed+bound>1 and other+bound>1
assert str(b/(1+b))==cert['kappa_upper']
r=dict(status='PASS_EXACT_FIXED_WORD_PACKING_CEILING',rejected_b=str(b),kappa_upper=str(b/(1+b)),patterns=len(patterns),minimum_dual_slack=str(min(slacks)),mercator_margin=str(fixed+bound-1),base_two_margin=str(other+bound-1),word_sha256=nom['word_sha256'],certificate_sha256=hashlib.sha256(certificate.read_bytes()).hexdigest(),scope='Only this emitted local word,72calls,m73,W7680 and unchanged idle stock. Every helper fits wholly inside one original idle child, leaving at most one paid remainder. Dropping timing/owner conflicts gives an optimistic relaxation. No bound on changed factories or algorithms.')
out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'],r['kappa_upper'])
