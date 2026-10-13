"""Finite paired-call majorization passes. Solver proposes; integers admit."""
from joint_owner_search import *

def write_outputs(out,inst,original,steps):
 out.mkdir(parents=True,exist_ok=True);raw=packed(inst.roles);owner=out/'OWNERS.json.gz';owner.write_bytes(gzip.compress(raw,mtime=0))
 profile={str(r):n for r,n in inst.baseline['profile'].items()}
 (out/'PROFILE.json').write_text(json.dumps(profile,indent=2)+'\n')
 fields={'profile':profile,'per_call_widths':[{'stage':s,'replica':r,'widths':inst.widths} for s,r in inst.plan['order']], 'assignment_sha256':hashlib.sha256(raw).hexdigest(),'assignment_sha256_semantics':'SHA256 sorted-key compact uncompressed OWNERS array','source_owners_sha256':sha(inst.source_owners_path),'provider_signatures':{'gauge44':{'widths':inst.widths,'profile':{int(r):n for r,n in inst.sig['actual_paid_profile'].items()},'source':'Frozen PR655 layered native signature'}}}
 (out/'PLAN-OWNER-FIELDS.json').write_text(json.dumps(fields,indent=2)+'\n')
 before=Counter(original['idle']);after=Counter(inst.baseline['idle'])
 margins=[sum(n*max(r-k,0) for r,n in after.items())-sum(n*max(r-k,0) for r,n in before.items()) for k in range(49)]
 assert min(margins)>=0 and margins[0]==margins[-1]==0
 receipt={'status':'PASS_FINITE_JOINT_OWNER_NOMINATION_PENDING_GLOBAL_ADMISSION','source_head':inst.source_head,'geometry_and_native_head':'3e669dc7987cb2295a71664b77e110c0cd979a87','source_plan_sha256':sha(PKG/'data/PLAN.json'),'source_owners_sha256':sha(inst.source_owners_path),'owners_semantic_sha256':hashlib.sha256(raw).hexdigest(),'owners_sha256':sha(owner),'baseline':original,'candidate':inst.baseline,'integer_stoploss_margins':margins,'strict_majorization':max(margins)>0,'accepted_steps':steps,'roles':len(inst.roles),'rank_mass':520704,'deficit':2560,'live':7168,'M':73,'remaining_admission':'Fresh native-provider binding, all actual73-column charts/controller audit, finite invoice, exact moment and outer assembly. No supplier/global optimality claim.'}
 (out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--owners',type=Path,required=True);ap.add_argument('--source-head',required=True);ap.add_argument('--pairs',type=int,default=120);ap.add_argument('--passes',type=int,default=3);ap.add_argument('--seconds',type=float,default=3);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 inst=Instance(a.owners);inst.source_owners_path=a.owners;inst.source_head=a.source_head;original=inst.baseline;steps=[];allreports=[]
 for passno in range(a.passes):
  scores=[]
  for x,y in itertools.combinations(range(72),2):
   score=sum(1 for g in inst.eligible[x]&inst.eligible[y] if 0<inst.caps[g]-inst.used[g]<inst.caps[g]);scores.append((score,x,y))
  accepted=0
  for _,x,y in sorted(scores,reverse=True)[:a.pairs]:
   report,roles=inst.solve(x,y,a.seconds);report['pass']=passno+1;allreports.append(report)
   if roles is not None and report['strict_majorization']:
    assert report['gain_b']>0
    steps.append(report);inst.roles=roles;inst.used=Counter();inst.bycall=defaultdict(dict)
    for z in roles:
     g=z['owner_replica'],z['child'],z['port'];inst.used[g]+=z['width'];inst.bycall[z['time']][z['helper']]=(g,z['width'])
    inst.baseline=inst.check(inst.roles);accepted+=1;write_outputs(a.out,inst,original,steps)
    print(json.dumps({'pass':passno+1,'pair':[x,y],'accepted':accepted,'b':inst.baseline['b'],'gain':inst.baseline['b']-original['b']}),flush=True)
  (a.out/'SEARCH.json').write_text(json.dumps({'per_pass_pair_limit':a.pairs,'pass_limit':a.passes,'time_limit_per_pair':a.seconds,'reports':allreports,'accepted':len(steps),'source_owners_sha256':sha(inst.source_owners_path),'source_plan_sha256':sha(PKG/'data/PLAN.json'),'source_head':inst.source_head,'geometry_and_native_head':'3e669dc7987cb2295a71664b77e110c0cd979a87'},indent=2)+'\n')
  print(json.dumps({'pass_completed':passno+1,'accepted':accepted,'b':inst.baseline['b']}),flush=True)
  if not accepted:break
 write_outputs(a.out,inst,original,steps)

if __name__=='__main__':main()
