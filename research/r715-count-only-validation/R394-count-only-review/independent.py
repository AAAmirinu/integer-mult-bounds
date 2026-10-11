import sys
sys.dont_write_bytecode=True
sys_dummy=None
from pathlib import Path

from fractions import Fraction as F

from functools import lru_cache

import json,hashlib,subprocess,sys,time

def need(x,s):

 if not x:raise ValueError(s)

DY=1<<240

def down(x):return F(x.numerator*DY//x.denominator,DY)

def up(x):return -down(-x)

@lru_cache(None)

def log_bounds(x):

 def unit(y):

  z=(y-1)/(y+1);q=z*z;term=z;total=F(0)

  for j in range(100):total+=term/(2*j+1);term*=q

  return 2*total,2*total+2*term/(201*(1-q))

 k=0

 while x>=2:x/=2;k+=1

 a,b=unit(x);c,d=unit(F(2));return down(a+k*c),up(b+k*d)

def exp_bounds(lo,hi):

 need(0<=lo<=hi<F(1,10),'exponential enclosure domain')

 def poly(x):

  t=total=F(1)

  for j in range(1,33):t*=x/j;total+=t

  return total,t

 l,_=poly(lo);u,t=poly(hi);return down(l),up(u+t*hi/33/(1-hi/34))

def constraints(a,b,e,t,k):
 need(0<a<b<F(1,32),'supplier domain')

 need(0<e<F(1,8) and 0<t<1,'parameter domain')

 q=a*(1-2*e);c=q+e/4;eps=(1-e)/(1+q);minimum=eps*q

 # Under b>a, internal saving is a. Balanced identities give

 # prefix = minimum+eta and Gaussian=min(prefix-delta,r-delta).

 r=minimum+e/2;d=e/8;leaf=(1-t)*b

 values=[a,b-a,F(1,32)-b,t,1-t,leaf-a,q,a-q,leaf-q,c,1-c,e/4,e*a,b-a+e*a,e*a,e*a,leaf-q,e/4,q,eps,minimum+e,minimum+e,e*(1-eps/4),eps*c,minimum+e,minimum+7*e/8,minimum+3*e/8,e/2,eps-(1-r)/2,minimum+e,r,1-r,F(1,4)-r,d,F(1,8)-d,eps-a,e,8-eps+r-d-minimum,F(1),F(10**6)-F(51*20161,25)]

 names=['bit_positive','complex_above_bit','complex_below_one_over32','beta_positive','beta_below_one','leaf_saving_above_bit','q_positive','q_below_internal','q_below_leaf','c_positive','c_below_one','q_below_reservations','lambda_above_tau','lambda_above_sigma','lambda_above_internal','lambda_prime_above_lambda','compact_leaf','compact_reservations','lambda_prime_below_one','epsilon_positive','epsilon_below_one','guard_width','K_geometry','K_dominates_log','record_suffix','phase_local','phase_boundary','gamma_sublinear','cell_above_band','prime_interval_packing','alpha_positive','alpha_below_one','alpha_below_one_fourth','delta_positive','delta_below_one_eighth','short_record_fallback','small_field_exposure','artificial_boundary','literal_scalar_guard','row_product_gap']

 margins={'balanced_prefix':minimum+e,'coordinate_movement':a,'compact_phase_layer':minimum,'bulk_exposure':a,'Gaussian_arithmetic':minimum+3*e/8,'scalar_work':minimum+7*e/8,'dimension':eps}

 result=dict(zip(names,values));result.update({n+'_above_kappa':v-k for n,v in margins.items()})

 need(len(result)==47 and min(result.values())>0,'strict outer constraint')

 need(min(margins.values())==minimum,'minimum margin identity')

 return minimum,result

BASE=Path(__file__).resolve().parent
HEAD='f43a0e9ad04a7b3683498274854ae2e35d4a8d7c'
PKG='research/r715-response-replica28'
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(path):return (BASE/'sources'/path).read_bytes()
def moment(P,m,W,s,children,fraction):
 need(all(type(r)is int and type(n)is int and 0<r<m and n>0 for r,n in P.items()),'invalid exact profile')
 lo=hi=F(0)
 for r,n in P.items():
  a,b=log_bounds(F(m,r));x,y=exp_bounds(s*a,s*b);lo+=F(r*n,m*W)*x;hi+=F(r*n,m*W)*y
 a,b=log_bounds(F(m));x,y=exp_bounds(s*a,s*b);z=F(children*sum(P.values()),m*W)*fraction
 return lo+z*x,hi+z*y
def ceiling(x):return (x.numerator+x.denominator-1)//x.denominator
def derive_outer(c,b,charged):
 eta=beta=grid=F(1,10**18);s=min(c,(1-beta)*b)-F(1,10**24);x0=F(384599,10**10);cut=[]
 need(x0<s<c and s<(1-beta)*b,'supplier seed slack')
 for j in range(1,7):
  old=s-s**(j-1)*(s-x0);a=s-s**j*(s-x0)
  need(a==s*(1-s)+s*old and old<a<s<1-a,'bootstrap hypotheses')
  gap=min(s-a,1-a-s,1-a-s*(1-old),1-s)
  n=max(ceiling(36/gap**2),ceiling(2*(4+charged)/gap))
  need(n*gap**2>=36 and n*gap>=2*(4+charged),'finite cutoff')
  cut.append({'gap':str(gap),'cutoff_log2':str(n)})
 q=a*(1-2*eta);cap=(1-eta)*q/(1+q);tick=cap/grid;k=grid*((tick.numerator-1)//tick.denominator)
 _,checks=constraints(a,b,eta,beta,k)
 return {'kappa':str(k),'saving':str(s),'strict_outer_constraints':{n:str(x) for n,x in checks.items()},'bootstrap':cut,'charged_coefficient_bits':charged},(a,b,eta,beta,k,cap)
def verify_profile(P,m,W,mass):
 need(all(type(r)is int and type(n)is int and 0<r<m and n>0 for r,n in P.items()),'invalid exact profile')
 need(sum(r*n for r,n in P.items())==mass,'rank mass changed')
# This text is appended to the reused, independently written R371 engine.
def score(name):
 source=(BASE/(name+'-EXPECTED.json')).read_bytes();x=json.loads(source)
 P={int(r):n for r,n in x['bit_profile'].items()};PC={int(r):n for r,n in x['complex_profile'].items()}
 m=78;W=x['bit']['live'];charged=x['bit']['charged_two_level_coefficient_bits']
 expected={'response28':(33600,28,6272,2112),'replica84':(100800,84,10304,3456)}[name]
 need(type(W)is int and (W,W//1200,charged,x['bit']['charged_prefix_bits'])==expected,'typed actual invoice')
 verify_profile(P,m,W,x['bit']['rank_mass']);verify_profile(PC,89,8400,x['complex']['rank_mass'])
 need(m*W-sum(r*n for r,n in P.items())==408*expected[1],'raw rank deficit')
 need(x['bit']['physical']==W+9 and x['external_row_allowance']==20161,'stock and row invoice')
 N=2*m;children=6*N*(N-1)+3*N+6*(N-1);fraction=F(1,10**16);oldchildren=32*m*m
 need(children==146478 and oldchildren==194688 and children<oldchildren,'Gaussian exact count')
 parent=F(x['bit_lower']);grid=10**24;b=F(x['complex_lower'])
 pv=moment(P,m,W,parent,oldchildren,fraction);pu=moment(P,m,W,parent+F(1,grid),oldchildren,fraction)
 need(pv[1]<1<pu[0],'parent bit root signs')
 inherited,_=derive_outer(parent,b,charged)
 need(inherited['kappa']==x['kappa'] and inherited['bootstrap']==x['bootstrap'] and inherited['strict_outer_constraints']==x['strict_outer_constraints'],'all parent outer arithmetic exact')
 lo=parent.numerator*grid//parent.denominator;hi=lo+10**15;iterations=0
 need(moment(P,m,W,F(lo,grid),children,fraction)[1]<1< moment(P,m,W,F(hi,grid),children,fraction)[0],'new root bracket')
 while hi-lo>1:
  mid=(lo+hi)//2;v=moment(P,m,W,F(mid,grid),children,fraction);iterations+=1
  if v[1]<1:lo=mid
  elif v[0]>1:hi=mid
  else:raise ValueError('ambiguous dyadic sign')
 lower,upper=F(lo,grid),F(hi,grid);lv=moment(P,m,W,lower,children,fraction);uv=moment(P,m,W,upper,children,fraction)
 need(lv[1]<1<uv[0],'new adjacent exact signs')
 changed,state=derive_outer(lower,b,charged);gain=F(changed['kappa'])-F(x['kappa']);need(gain>0,'positive count-only gain')
 cl=moment(PC,89,8400,b,32*89*89,fraction);cu=moment(PC,89,8400,b+F(1,10**18),32*89*89,fraction)
 need(cl[1]<1<cu[0],'unchanged complex signs')
 preliminary={'profile':name,'root_lower':str(lower),'root_upper':str(upper),'kappa':changed['kappa'],'gain':str(gain),'bad_fraction':str(fraction),'children':children}
 print(json.dumps(preliminary),flush=True)
 controls=[];a,b,e,t,k,cap=state
 need(k<cap<=k+F(1,10**18),'grid-tight strict kappa')
 for label,ee,tt,kk in [('next_grid',e,t,k+F(1,10**18)),('zero_eta',F(0),t,k),('zero_beta',e,F(0),k),('unit_beta',e,F(1),k)]:
  try:constraints(a,b,ee,tt,kk)
  except ValueError as err:controls.append({'name':label,'reason':str(err)})
  else:raise ValueError('negative accepted '+label)
 for label,edit in [('omitted_child',lambda q:q.__setitem__(1,q[1]-1)),('integer_to_float',lambda q:q.__setitem__(1,float(q[1])))]:
  q=dict(P);edit(q)
  try:verify_profile(q,m,W,x['bit']['rank_mass'])
  except ValueError as err:controls.append({'name':label,'reason':str(err)})
  else:raise ValueError('negative accepted '+label)
 need(moment(P,m,W,lower,oldchildren,fraction)[0]>1,'old charge at count-only root rejected')
 controls.append({'name':'restore_old_charge','reason':'old-charge moment lower exceeds1'})
 need(json.loads(json.dumps(2**80+1))==2**80+1 and int(float(2**80+1))!=2**80+1,'large integer float corruption')
 controls.append({'name':'large_integer_float_loss','reason':'float loses1'})
 need(charged==expected[2] and charged!=2432,'wrong cutoff invoice rejected')
 controls.append({'name':'old_cutoff_invoice','reason':'actual charge differs from2432'})
 return {'preliminary':preliminary,'raw_expected_sha256':sha(source),'typed_invoice':{'m':m,'W':W,'physical':x['bit']['physical'],'charged_bits':charged,'row_allowance':20161},'iterations':iterations,'root':{'lower':str(lower),'upper':str(upper),'lower_residual_upper':str(lv[1]-1),'upper_residual_lower':str(uv[0]-1)},'parent_root_signs':{'lower_residual_upper':str(pv[1]-1),'upper_residual_lower':str(pu[0]-1)},'complex_root_signs':{'lower_residual_upper':str(cl[1]-1),'upper_residual_lower':str(cu[0]-1)},'outer':{'inherited':inherited,'count_only':changed},'controls':controls,'grid_tight':True}
def main():
 started=time.monotonic();rows=[score(n) for n in ('response28','replica84')]
 out={'status':'PASS_INDEPENDENT_CONDITIONAL_COUNT_ONLY_ARITHMETIC','reviewer':'AI subagent baseline_audit','checker_sha256':sha(Path(__file__).read_bytes()),'source_lock_sha256':sha((BASE/'SOURCE-LOCK-001.json').read_bytes()),'python':sys.version,'optimization':sys.flags.optimize,'command':sys.argv,'workers':1,'profiles':rows,'elapsed_seconds':time.monotonic()-started,'scope':'ONLY Gaussian fallback children194688->146478; original bad fraction1e-16 and retained O-cover/all-size hypotheses unchanged; no GL q80 bound and no native supplier replay'}
 need(out['elapsed_seconds']<180,'bounded experiment')
 dest=BASE/('optimized-001.json' if sys.flags.optimize else 'normal-001.json');need(not dest.exists(),'immutable fresh receipt');dest.write_text(json.dumps(out,indent=2)+'\n')
 print(out['status'],out['elapsed_seconds'],flush=True)
if __name__=='__main__':main()
