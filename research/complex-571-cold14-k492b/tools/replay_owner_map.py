"""Replay recorded simultaneous placements and the two proved helper-width changes.
Nomination checks only; unchanged physical and exact global audits admit it.
Jeremy Diviney with OpenAI Codex assistance; Apache-2.0.
"""
import argparse,gzip,hashlib,json
from collections import Counter,defaultdict
from pathlib import Path

def main():
 if not __debug__:raise RuntimeError('Assertions required; run without -O')
 ap=argparse.ArgumentParser();ap.add_argument('--base-data',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();p=Path(__file__).resolve().parents[1];d=json.loads((p/'data/OWNER-MOVES.json').read_text());sha=lambda b:hashlib.sha256(b).hexdigest();raw=(a.base_data/'OWNERS.json.gz').read_bytes();assert sha(raw)==d['base_owners_sha256'];assert sha((a.base_data/'PLAN.json').read_bytes())==d['base_plan_sha256'];roles=json.loads(gzip.decompress(raw));byid={(r['time'],r['helper']):r for r in roles};assert len(byid)==len(roles)==35424
 plan=json.loads((p/'data/PLAN.json').read_text());base=json.loads((a.base_data/'PLAN.json').read_text());assert plan['order']==base['order']and plan['windows']==base['windows']
 dispatch={c['time']:c['provider']for c in plan['provider_calls']};assert dispatch=={c['time']:c['provider']for c in base['provider_calls']}
 for r in roles:
  if dispatch[r['time']]=='jp8'and r['helper']in (357,366):assert r['width']==9;r['width']=7
  assert r['width']==plan['provider_registry'][dispatch[r['time']]]['widths'][r['helper']]
 seen=set()
 for t,h,before,after in d['moves']:
  assert (t,h)not in seen;seen.add((t,h));r=byid[t,h];assert [r[k]for k in ('owner_replica','child','port')]==before;o,ch,port=after;assert 0<=o<8 and 0<=port<112;assert t in plan['windows'][f'{o},{ch}'][1];family=o*896+(2*plan['pairs'][str(ch)]+plan['sides'][str(ch)])*112+port;r.update(owner_replica=o,child=ch,port=port,family=family,copy=o*112+port)
 bins=defaultdict(list);families=set()
 for r in roles:
  k=r['family'],r['time'];assert k not in families;families.add(k);bins[r['owner_replica'],r['child'],r['port']].append(r)
 idle=Counter()
 for key,(cap,times)in plan['windows'].items():
  o,ch=map(int,key.split(','))
  for port in range(112):
   off=0
   for r in sorted(bins[o,ch,port],key=lambda r:(r['time'],r['helper'])):assert r['time']in times;r['offset']=off;off+=r['width']
   assert off<=cap
   if off<cap:idle[cap-off]+=1
 paid=idle.copy()
 for c in plan['provider_calls']:paid.update({int(k):v for k,v in plan['provider_registry'][c['provider']]['actual_paid_profile'].items()})
 assert dict(paid)=={int(k):v for k,v in plan['profile'].items()};assert 73*plan['live']-sum(k*v for k,v in paid.items())==plan['deficit'];roles.sort(key=lambda r:(r['time'],r['helper']));raw=json.dumps(roles,sort_keys=True,separators=(',',':')).encode();assert sha(raw)==d['result_owners_content_sha256'];a.out.mkdir(parents=True,exist_ok=False);(a.out/'OWNERS.json.gz').write_bytes(gzip.compress(raw,mtime=0));print('NOMINATION REPRODUCED;',len(seen),'placements; full verification required')

if __name__=='__main__':main()
