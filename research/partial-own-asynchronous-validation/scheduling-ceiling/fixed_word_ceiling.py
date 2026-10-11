"""A rigorous relaxed ceiling for the frozen local word and 72-call architecture.
This bounds arbitrary remainder allocations, not all multiplication algorithms.
"""
from pathlib import Path
from fractions import Fraction as Q
import hashlib,importlib.util,json,sys
base,out=map(Path,sys.argv[1:]);assert not out.exists()
def module(name):
 p=base/'work/pr361/code/engines'/(name+'.py');s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M,Other=module('moment'),module('base_two_moment')
checks=json.loads((base/'split-centres/LOCAL-CHECKS.json').read_text())
assert checks['forward']['paid_profile']==checks['backward']['paid_profile']
local={int(r):72*n for r,n in checks['forward']['paid_profile'].items()}
mass=73*7680-2496;localmass=sum(r*n for r,n in local.items());rest=mass-localmass
assert localmass==492624 and rest==65520 and rest%48==0
ideal=dict(local);ideal[48]=rest//48
assert sum(r*n for r,n in ideal.items())==mass
price=M.certify(ideal,73,7680,True);upper=Q(price['upper'])
lo,hi=M.moment(ideal,73,7680,upper,True)
a,b=Other.moment(73,7680,list(ideal.items()),upper)
c,d=Other.moment(73,7680,[(1,32*73*73*sum(ideal.values()))],upper)
assert lo>1 and a+c/10**16>1
result=dict(status='PASS_FIXED_WORD_RELAXED_CEILING_TWO_EXACT_ENGINES',
 local_checks_sha256=hashlib.sha256((base/'split-centres/LOCAL-CHECKS.json').read_bytes()).hexdigest(),
 local_mass=localmass,remainder_mass=rest,ideal_remainder_rank=48,ideal_remainder_count=1365,
 ideal_profile=ideal,rejected_b=str(upper),rejected_b_decimal=price['upper'],
 mercator_lower_margin=str(lo-1),base_two_lower_margin=str(a+c/10**16-1),
 kappa_upper=str(upper/(1+upper)),kappa_upper_decimal=M.decimal(upper/(1+upper)),
 scope='Only constructions retaining this local paid profile at all 72 calls, m=73, W=7680, deficit2496 and other child ranks at most48. Allows impossible ideal placement, so this is an upper bound, not an achievable candidate or a global algorithmic barrier.')
out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['rejected_b_decimal'],result['kappa_upper_decimal'])
