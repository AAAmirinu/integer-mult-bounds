"""Transfer a frozen asynchronous ownership plan to the unchanged-width word."""
from pathlib import Path
from collections import Counter
import sys, json, gzip, hashlib

package, base, changed, source, output, receipt = map(Path, sys.argv[1:7])
sys.path.insert(0, str(package/'code'))
import gk_word as G
read=lambda p:json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
old=G.build(read(base),read(package/'data/selections/gauge80-kernel42.json'))
new=read(changed)
keys=['centers','center_frames','target_levels','root_lines','ports','cut','precondition','start_extra','scatter']
assert all(old[k]==new[k] for k in keys)
assert G.widths_of(old)==G.widths_of(new)
old_local=G.profile(old);new_local=G.profile(new)
assert old_local==Counter({int(r):n for r,n in old['report']['local_profile'].items()})
assert new_local==Counter({int(r):n for r,n in new['report']['local_profile'].items()})
plan=read(source);profile=Counter({int(r):n for r,n in plan['profile'].items()})
for r,n in old_local.items():profile[r]-=72*n
for r,n in new_local.items():profile[r]+=72*n
assert all(n>=0 for n in profile.values())
assert 73*7680-sum(r*n for r,n in profile.items())==2496
plan['profile']=dict(sorted((r,n) for r,n in profile.items() if n))
output.write_text(json.dumps(plan,indent=2)+'\n')
assert {k:v for k,v in read(output).items() if k!='profile'}=={k:v for k,v in read(source).items() if k!='profile'}
result=dict(status='PASS_UNCHANGED_WIDTH_ASYNC_PLAN_TRANSFER',preserved_fields=keys,
            helper_widths=dict(sorted(Counter(G.widths_of(new)).items())),
            old_local_profile=dict(sorted(old_local.items())),new_local_profile=dict(sorted(new_local.items())),
            predicted_profile=plan['profile'],plan_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
            scope='Only local paid profile changes. The independent emitted-controller audit must reconstruct all owners, events and actual paid children.')
receipt.write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],flush=True)
