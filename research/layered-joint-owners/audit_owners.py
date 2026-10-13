"""Solver-free integer owner admission and rational native moment screen.
Checks the explicit parent windows, not their physical derivation. Fresh global
phase/controller/invoice/outer admission is a separate obligation.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
from decimal import Decimal,localcontext,ROUND_FLOOR
from functools import lru_cache
import argparse,copy,gzip,hashlib,json

if not __debug__:
 raise RuntimeError('Assertions are required; do not use python -O.')
BASELINE_HEAD='0805e78f5fecc700804d4766d7e3e1d7d7e6a2ba'
BASELINE_SHA256='01a8f5c5cd54e13662f2fe40d16c2a1d443dfc664a6c988fffea6e0bacdfc937'

read=lambda p:json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
packed=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
DYAD=1<<240
floor=lambda x:F(x.numerator*DYAD//x.denominator,DYAD)
ceil=lambda x:-floor(-x)
@lru_cache(None)
def log_bounds(x):
 assert x>=1;k=0
 while x>=2:x/=2;k+=1
 def log_atanh(y):
  z=(y-1)/(y+1);s=F(0);power=z
  for j in range(150):s+=2*power/(2*j+1);power*=z*z
  return s,s+2*power/(301*(1-z*z))
 l,u=log_atanh(x);a,b=log_atanh(F(2));return floor(l+k*a),ceil(u+k*b)
def exp_bounds(l,u):
 assert 0<=l<=u<F(1,10)
 def pol(x):
  s=t=F(1)
  for j in range(1,25):t*=x/j;s+=t
  return s,t
 lo,_=pol(l);hi,t=pol(u);return floor(lo),ceil(hi+t*u/25/(1-u/26))
def moment(H,b):
 lo=hi=F(0)
 for r,n in H.items():
  l,u=log_bounds(F(73,r));a,c=exp_bounds(b*l,b*u);lo+=F(r*n,73*7168)*a;hi+=F(r*n,73*7168)*c
 return floor(lo),ceil(hi)
def certificate(H):
 with localcontext() as ctx:
  ctx.prec=65;terms=[(Decimal(r*n)/Decimal(73*7168),(Decimal(73)/Decimal(r)).ln()) for r,n in H.items()];lo=Decimal(0);hi=Decimal('.01')
  for _ in range(220):
   mid=(lo+hi)/2
   if sum(p*(mid*l).exp() for p,l in terms)<1:lo=mid
   else:hi=mid
  q=int((lo*10**24).to_integral_value(rounding=ROUND_FLOOR))
 lo=F(q,10**24);hi=lo+F(1,10**24);lv=moment(H,lo);hv=moment(H,hi);assert lv[1]<1<hv[0]
 return {'native_lower':str(lo),'native_upper':str(hi),'lower_endpoint_moment_upper':str(lv[1]),'upper_endpoint_moment_lower':str(hv[0]),'nominal_outer_ceiling_lower':str(lo/(1+lo)),'nominal_outer_ceiling_upper':str(hi/(1+hi)),'scope':'Native homogeneous moment only; outer ceiling is not an assembled witness.'}

def audit(plan,roles,expected_widths):
 assert (plan['K'],plan['T'],plan['M'],plan['L'],plan['live'])==(4,8,73,9,7168)
 caps={};elig=defaultdict(set);families={};used=defaultdict(set);helpers=defaultdict(set);callfams=defaultdict(set)
 for key,(cap,times) in plan['windows'].items():
  rep,ch=map(int,key.split(','));assert 0<cap<=48 and len(times)==len(set(times))
  for port in range(112):
   g=(rep,ch,port);caps[g]=cap;families[g]=rep*896+(2*plan['pairs'][str(ch)]+plan['sides'][str(ch)])*112+port
   for t in times:elig[t].add(g)
 for t,gs in elig.items():assert len({families[g] for g in gs})==len(gs)
 for z in roles:
  t,h=z['time'],z['helper'];assert type(t) is int and 0<=t<72 and type(h) is int and 0<=h<492
  s,rep=plan['order'][t];assert (z['stage'],z['replica'])==(s,rep)
  g=(z['owner_replica'],z['child'],z['port']);assert g in elig[t]
  assert z['family']==families[g] and z['copy']==g[0]*112+g[2]
  assert h not in helpers[t] and z['family'] not in callfams[t];helpers[t].add(h);callfams[t].add(z['family'])
  assert not(g[0]==rep and plan['pairs'][str(g[1])]==max(0,(s-1)//2))
  w=z['width'];off=z['offset'];assert type(w) is int and w==expected_widths[h] and type(off) is int and off>=0 and off+w<=caps[g]
  cells=set(range(off,off+w));assert not cells&used[g];used[g]|=cells
 assert len(roles)==72*492 and all(helpers[t]==set(range(492)) for t in range(72))
 assert all(cells==set(range(len(cells))) for cells in used.values())
 idle=Counter(caps[g]-len(used[g]) for g in caps if caps[g]>len(used[g]))
 local={1:2542,2:414,3:434,4:154,5:56,8:8};H=Counter({r:72*n for r,n in local.items()});H.update(idle)
 assert sum(r*n for r,n in H.items())==520704 and 73*7168-sum(r*n for r,n in H.items())==2560
 return idle,H

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--baseline-owners',type=Path,required=True);ap.add_argument('--package',type=Path,required=True);ap.add_argument('--nomination',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 assert sha(a.baseline_owners)==BASELINE_SHA256, 'Unexpected PR656 seed owner map'
 p=a.package;plan=read(p/'data/PLAN.json');baseline=read(a.baseline_owners);roles=read(a.nomination/'OWNERS.json.gz');widths=plan['provider_registry']['gauge44']['widths'];assert Counter(widths)=={4:52,5:48,7:42,8:116,9:234}
 old,oldH=audit(plan,baseline,widths);new,H=audit(plan,roles,widths)
 profile={str(k):v for k,v in sorted(H.items())};assert profile==read(a.nomination/'PROFILE.json')
 fields=read(a.nomination/'PLAN-OWNER-FIELDS.json');assert fields['profile']==profile and fields['assignment_sha256']==hashlib.sha256(packed(roles)).hexdigest()
 assert fields['per_call_widths']==[{'stage':s,'replica':r,'widths':widths} for s,r in plan['order']]
 margins=[sum(n*max(r-k,0) for r,n in new.items())-sum(n*max(r-k,0) for r,n in old.items()) for k in range(49)];assert margins[0]==margins[-1]==0 and min(margins)>=0 and max(margins)>0
 controls=[]
 for name,change in [('wrong_width',lambda x:x[0].update(width=x[0]['width']+1)),('wrong_call_time',lambda x:x[0].update(time=(x[0]['time']+1)%72)),('duplicate_helper',lambda x:x[1].update(helper=x[0]['helper']))]:
  bad=copy.deepcopy(roles);change(bad)
  try:audit(plan,bad,widths)
  except (AssertionError,KeyError,IndexError):controls.append(name)
  else:raise AssertionError('Corruption accepted: '+name)
 result={'status':'PASS_SOLVER_FREE_JOINT_OWNER_COMBINATORICS_AND_NATIVE_MOMENT','source_baseline_head':BASELINE_HEAD,'geometry_and_native_head':'3e669dc7987cb2295a71664b77e110c0cd979a87','source_plan_sha256':sha(p/'data/PLAN.json'),'source_owners_sha256':sha(a.baseline_owners),'owners_sha256':sha(a.nomination/'OWNERS.json.gz'),'owners_semantic_sha256':hashlib.sha256(packed(roles)).hexdigest(),'baseline_idle':dict(sorted(old.items())),'candidate_idle':dict(sorted(new.items())),'global_profile':profile,'integer_stoploss_margins':margins,'exact_native_moment':certificate(H),'negative_controls_rejected':controls,'all_explicit_windows_and_capacities_checked':True,'all_families_distinct_and_outside_active_data':True,'all_helpers_and_offsets_checked':True,'remaining_admission':'Independently derive controller windows and actual73-column phase charts, finite invoice and complete outer witness. No new physical supplier claimed here.'}
 a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'native_moment':result['exact_native_moment'],'profile':profile,'controls':controls},indent=2))
if __name__=='__main__':main()
