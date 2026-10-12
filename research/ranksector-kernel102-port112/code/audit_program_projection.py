"""Prove the expanded112 program is a disjoint projection of guarded120.
No emitter imports; both literal instruction streams and every register are read.
Prepared with OpenAI Codex assistance. Apache-2.0.
"""
from pathlib import Path
from collections import Counter
import copy,gzip,hashlib,json,sys
if not __debug__:raise RuntimeError('Assertions must remain enabled')
parent,local,dest=map(Path,sys.argv[1:]);read=lambda p:json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=read(parent/'split-centres/CANONICAL-WORD.json.gz');b=read(local/'CANONICAL-WORD.json.gz');old=read(parent/'split-centres/LOCAL-PROGRAMS.json.gz');new=read(local/'LOCAL-PROGRAMS.json.gz')
kept=[i for i,q in enumerate(a['ports'])if q in b['ports']];assert [a['ports'][i]for i in kept]==b['ports'] and(len(kept),a['v'],b['v'])==(112,120,112)
mp={('L',r):('L',j)for j,r in enumerate(kept)};mp.update({('L',120+r):('L',112+j)for j,r in enumerate(kept)});mp.update({('L',240+h):('L',224+h)for h in range(560)})
for i,r in enumerate(a['centers']):
 if('L',r)in mp:
  nr=mp['L',r][1];assert nr in b['centers'];mp['C',i]=('C',b['centers'].index(nr))
assert len(mp)==792 and len(b['centers'])==8
universe={('L',r)for r in range(800)}|{('C',r)for r in range(16)};removed=universe-set(mp);assert len(removed)==24

def project(events):
 result=[];deleted=Counter();paid=Counter()
 for ev in events:
  e=copy.deepcopy(ev);tag=e[0]
  if tag=='phase':result.append(e);continue
  if tag=='scalar':
   op=e[1];regs=[tuple(op[1])]+([tuple(op[2])]if op[0]in['add','copy']else[])
  elif tag=='center':regs=[('C',e[1])]
  elif tag in['climb','adapter','residual_adapter']:regs=[('L',e[2])]
  else:raise AssertionError(tag)
  assert set(regs)<=universe
  omit=any(r in removed for r in regs)
  if omit:
   assert all(r in removed for r in regs),('cross-component scalar',e)
   deleted[tag]+=1
   if tag in['climb','center']:paid[e[-1]]+=1
   continue
  if tag=='scalar':
   e[1][1]=list(mp[regs[0]])
   if len(regs)==2:e[1][2]=list(mp[regs[1]])
  elif tag=='center':e[1]=mp[regs[0]][1]
  else:e[2]=mp[regs[0]][1]
  result.append(e)
 return result,deleted,paid
reports={}
for ori in ['forward','backward']:
 projected,deleted,paid=project(old[ori]);assert projected==new[ori],ori;assert paid=={1:8,8:16}
 reports[ori]=dict(original_events=len(old[ori]),retained_events=len(projected),deleted_events=dict(deleted),deleted_children=dict(paid))
controls=[]
def reject(name,fn):
 try:fn()
 except AssertionError:controls.append(name)
 else:raise AssertionError('Accepted control '+name)
# A cross-component read must be rejected, even if its target is removed.
x=copy.deepcopy(old['forward']);idx=next(i for i,e in enumerate(x)if e[0]=='scalar'and e[1][0]=='add');x[idx][1][1]=list(next(iter(removed)));reject('cross_component_read',lambda:project(x))
# Literal program equality cannot survive deletion or a changed coefficient.
for name,change in [('missing_kept_instruction',lambda x:x.pop(next(i for i,e in enumerate(x)if e[0]=='scalar'))),('changed_kept_coefficient',lambda x:x[next(i for i,e in enumerate(x)if e[0]=='scalar'and e[1][0]=='add')][1].__setitem__(3,99))]:
 x=copy.deepcopy(new['forward']);change(x)
 def check():assert project(old['forward'])[0]==x
 reject(name,check)
guards={f:sha(parent/'lemmaG'/f)for f in ['PREOP-GUARDS-lg_instances.json','PREOP-GUARDS-lg_e2e.json','MUTANTS.json']}
receipt=read(parent/'RECEIPT.json');assert all(s['exit_code']==0 for s in receipt['steps'])
for f,h in guards.items():assert receipt['artifacts']['lemmaG/'+f]==h
report=dict(status='PASS_LITERAL_DISJOINT_PROJECTION_OF_GUARDED_PARENT',orientations=reports,negative_controls=controls,parent_guard_receipts=guards,source_hashes={str(p):sha(p)for p in [parent/'split-centres/LOCAL-PROGRAMS.json.gz',local/'LOCAL-PROGRAMS.json.gz',parent/'RECEIPT.json']},scope='Every retained expanded instruction, frame and coefficient equals the guarded120 program under an injective register rename. Removed registers form a disjoint component, so the restriction preserves every retained local operation and its range bound. The new whole-owner routing and global invoice require separate audits; all-size interfaces remain inherited.')
dest.write_text(json.dumps(report,indent=2)+'\n');print(report['status'])
