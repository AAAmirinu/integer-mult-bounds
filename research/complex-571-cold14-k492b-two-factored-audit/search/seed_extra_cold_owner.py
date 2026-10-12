"""Discovery seed only: shrink one cold residual, retain original placements.
Generated supplier bindings are refreshed only after independent localization.
"""
import argparse,json,gzip,hashlib
from collections import Counter,defaultdict
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--data',type=Path,required=True);ap.add_argument('--helper',type=int,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
p=json.loads((a.data/'PLAN.json').read_text());roles=json.loads(gzip.decompress((a.data/'OWNERS.json.gz').read_bytes()));reg=p['provider_registry']['jp8'];assert reg['widths'][a.helper]==9;reg['widths'][a.helper]=7
for k,d in {'1':1,'2':1,'5':-1}.items():reg['actual_paid_profile'][k]+=d
sel={c['time']:c['provider']for c in p['provider_calls']};dispatch={(c['stage'],c['replica']):c['provider']for c in p['provider_calls']}
for c in p['per_call_widths']:c['widths']=p['provider_registry'][dispatch[c['stage'],c['replica']]]['widths']
bins=defaultdict(list)
for z in roles:
 if sel[z['time']]=='jp8'and z['helper']==a.helper:assert z['width']==9;z['width']=7
 bins[z['owner_replica'],z['child'],z['port']].append(z)
idle=Counter()
for key,(cap,times)in p['windows'].items():
 o,ch=map(int,key.split(','))
 for port in range(112):
  off=0
  for z in sorted(bins[o,ch,port],key=lambda x:(x['time'],x['helper'])):z['offset']=off;off+=z['width']
  assert off<=cap
  if off<cap:idle[cap-off]+=1
profile=idle.copy()
for c in p['provider_calls']:profile.update({int(k):v for k,v in p['provider_registry'][c['provider']]['actual_paid_profile'].items()})
assert 73*p['live']-sum(k*v for k,v in profile.items())==p['deficit'];p['profile']={str(k):v for k,v in sorted(profile.items())};p['mode']='UNADMITTED_NEW_PROVIDER_DISCOVERY';raw=json.dumps(roles,sort_keys=True,separators=(',',':')).encode();p['assignment_sha256']=hashlib.sha256(raw).hexdigest();(a.out/'PLAN.json').write_text(json.dumps(p,indent=2)+'\n');(a.out/'OWNERS.json.gz').write_bytes(gzip.compress(raw,mtime=0));print('SEED',dict(idle))
