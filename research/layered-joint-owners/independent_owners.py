"""Independent solver-free whole-owner and all-p moment audit.
No import from optimizer, emitter, or source checker. Discovery is not admission.
"""
from pathlib import Path
from collections import Counter,defaultdict
import argparse,json,gzip,hashlib,tempfile,copy
if not __debug__:
 raise RuntimeError('Assertions must remain enabled')

read=lambda p:json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def audit(main,parent,owners_path,comparison_paths=None):
 pkg=parent;t=read(pkg/'evidence/global/GLOBAL-TEMPLATE.json.gz');plan=read(pkg/'data/PLAN.json');canon=read(pkg/'evidence/local/CANONICAL-WORD.json.gz')
 phasefile=main/'research/frame-sa504/inputs/data-base/work/complex-nine-native/DATA-PHASES.json';ph=read(phasefile)
 assert sha(phasefile)==t['exact_data_phase_recipe_sha256']=='c5916ff312678f12aba403847643fbbc29f643acec60bdf836fa56cd3e8251fa'
 assert (t['m'],t['live'],t['physical'],canon['v'],canon['h'],canon['R'])==(73,7168,7670,112,9,492)
 assert sha(pkg/'evidence/local/CANONICAL-WORD.json.gz')==t['local_providers']['gauge44']['canonical_word_sha256']
 widths=[len(canon['frames'][canon['final'][224+h]])-len(canon['frames'][canon['start'][224+h]]) for h in range(492)]
 assert widths==plan['provider_registry']['gauge44']['widths']==t['local_providers']['gauge44']['widths']
 assert Counter(widths)==Counter({4:52,5:48,7:42,8:116,9:234})
 localprofile={int(r):n for r,n in canon['local_profile'].items()}
 assert localprofile=={int(r):n for r,n in plan['provider_registry']['gauge44']['actual_paid_profile'].items()}
 # Establish indivisible call blocks and all literal replica-local touches.
 order=[tuple(x) for x in plan['order']]
 assert order==[(c['stage'],c['replica']) for c in t['calls']] and len(set(order))==72
 assert all([s for s,r in order if r==rep]==list(range(9)) for rep in range(8))
 stagepair={e['stage']:e['pair'] for e in t['recipe'] if e['kind']=='local'}
 positive_children={i for i,x in enumerate(ph['recipes'][0]['idle_children']) if x['rank']};assert positive_children==set(range(18))
 last={};windows={};callpos={};pairs={};sides={};block=-1
 for pos,e in enumerate(t['execution_schedule']):
  if 'replica' not in e:continue
  rep=e['replica']
  if e['kind']=='local_cover_sweep':
   block+=1;assert e['time']==block and order[block]==(e['stage'],rep)
   callpos[e['time']]=pos;last[rep,stagepair[e['stage']]]=pos
  assert e['time']==block
  if e['kind']=='bridge':last[rep,e['src']]=last[rep,e['dst']]=pos
  elif e['kind']=='idle_cover_sweep':
   for side,ch in enumerate(e['child_indices']):
    if ch not in positive_children:continue
    pairs[ch]=e['pair'];sides[ch]=side;windows[rep,ch]=(last.get((rep,e['pair']),-1),pos)
 assert block==71 and len(windows)==8*18
 caps={}
 for rep in range(8):
  for ch in range(18):
   dims={int(x['idle_children'][ch]['rank']) for x in ph['recipes']};assert len(dims)==1;cap=dims.pop()
   lo,hi=windows[rep,ch];allowed=[tm for tm,pos in callpos.items() if lo<pos<hi]
   assert plan['windows'][f'{rep},{ch}']==[cap,allowed]
   for port in range(112):caps[rep,ch,port]=cap
 assert plan['pairs']=={str(k):v for k,v in pairs.items()} and plan['sides']=={str(k):v for k,v in sides.items()}
 bases={}
 for port,q in enumerate(canon['ports']):
  assert ph['recipes'][port]['port']==port and q==ph['recipes'][port]['q']
  z=next(i for i in range(9) if not(q>>i)&1);u=q^(1<<z);ix=list(range(9));ix[0],ix[z]=ix[z],ix[0]
  B=[(1<<i)^(u if u>>i&1 else 0) for i in ix]+[1<<i for i in range(9,73)]
  assert len(set(B))==73 and all((x&y).bit_count()%2==int(i==j) for i,x in enumerate(B) for j,y in enumerate(B))
  bases[port]=B
 def mapping(path):
  roles=read(path);seen=set();percall=defaultdict(set);used=defaultdict(set);occupied=[];cross=0;small=0;sigmas=set();dig=hashlib.sha256()
  for z in sorted(roles,key=lambda z:(z['time'],z['helper'])):
   tm,h=z['time'],z['helper'];assert 0<=tm<72 and 0<=h<492
   s,r=order[tm];assert (z['stage'],z['replica'])==(s,r);assert (tm,h) not in seen;seen.add((tm,h))
   rep,ch,port=z['owner_replica'],z['child'],z['port'];assert 0<=rep<8 and 0<=ch<18 and 0<=port<112
   assert z['copy']==rep*112+port
   f=rep*896+(2*pairs[ch]+sides[ch])*112+port;assert f==z['family'] and 0<=f<7168
   assert f not in percall[tm];percall[tm].add(f)
   datafamilies={v[0] for v in t['calls'][tm]['owners'][:224]};assert f not in datafamilies
   assert windows[rep,ch][0]<callpos[tm]<windows[rep,ch][1]
   w=widths[h];assert z['width']==w and 0<=z['offset'] and z['offset']+w<=caps[rep,ch,port]
   cells=set(range(z['offset'],z['offset']+w));g=rep,ch,port;assert not cells&used[g];used[g]|=cells
   B=bases[port];pending=list(map(int,ph['recipes'][port]['idle_children'][ch]['orthogonal_axes']));assert len(pending)==caps[g]
   assert len(set(pending))==len(pending) and all(x in B for x in pending)
   active=[B.index(x) for x in pending[z['offset']:z['offset']+w]];spectators=[i for i in range(73) if i not in active][:9-w]
   perm=active+spectators+[i for i in range(73) if i not in active and i not in spectators]
   assert sorted(perm)==list(range(73)) and len(set(active+spectators))==9
   sigma=tuple(B[i] for i in perm);assert sigma[:w]==tuple(pending[z['offset']:z['offset']+w])
   sigmas.add(sigma);d=hashlib.sha256(json.dumps(sigma,separators=(',',':')).encode()).hexdigest();dig.update(json.dumps([s,r,h,f,d],separators=(',',':')).encode()+b'\n')
   cross+=r!=rep;small+=w<9
  assert len(roles)==len(seen)==35424 and all(len(v)==492 for v in percall.values())
  assert all(v==set(range(len(v))) for v in used.values())
  idle=Counter(caps[g]-len(used[g]) for g in caps) # zero-pad every same catalog coordinate
  profile=Counter({r:72*n for r,n in localprofile.items()})+Counter({r:n for r,n in idle.items() if r})
  assert sum(r*n for r,n in profile.items())==520704 and 73*7168-520704==2560 and 73**2>2*max(profile)**2
  return {'owners_sha256':sha(path),'idle':dict(sorted(idle.items())),'profile':dict(sorted(profile.items())),'cross_replica':cross,'entering_or_cold_lower_width':small,'sigmas':len(sigmas),'sigma_digest':dig.hexdigest(),'roles':roles}
 old=mapping(pkg/'data/OWNERS.json.gz');new=mapping(owners_path)
 assert old['profile']=={int(k):v for k,v in read(pkg/'evidence/audit/OWNERS-AND-PROFILE.json')['paid_profile'].items()}
 assert old['sigma_digest']==read(pkg/'evidence/global/HOSTED.json')['sigma_stream_sha256']
 def compare(base):
  om={(z['time'],z['helper']):z for z in base['roles']}
  changed=[z for z in new['roles'] if z!=om[z['time'],z['helper']]]
  di={k:new['profile'].get(k,0)-base['profile'].get(k,0) for k in sorted(set(new['profile'])|set(base['profile']))};di={k:v for k,v in di.items() if v}
  assert sum(k*v for k,v in di.items())==0
  margins=[sum(n*max(r-k,0) for r,n in new['idle'].items())-sum(n*max(r-k,0) for r,n in base['idle'].items()) for k in range(74)]
  assert margins[0]==margins[-1]==0 and min(margins)>=0 and max(margins)>0
  return {'baseline':{k:v for k,v in base.items() if k!='roles'},'profile_delta':di,'stoploss_delta':margins,'changed_records':len(changed),'changed_by_call':dict(Counter(z['time'] for z in changed)),'strict_all_p_improvement':True}
 comparisons={'PR656':compare(old)}
 for name,path in (comparison_paths or {}).items():
  assert name not in comparisons and name
  comparisons[name]=compare(mapping(path))
 reference=comparisons['PR656']
 return {'status':'PASS_SOLVER_FREE_LITERAL_WHOLE_FAMILY_AND_ALL_P_MOMENT_AUDIT','source_plan_sha256':sha(pkg/'data/PLAN.json'),'source_template_sha256':sha(pkg/'evidence/global/GLOBAL-TEMPLATE.json.gz'),'canonical_word_sha256':sha(pkg/'evidence/local/CANONICAL-WORD.json.gz'),'data_phases_sha256':sha(phasefile),'candidate_input':owners_path.name,'baseline':reference['baseline'],'candidate':{k:v for k,v in new.items() if k!='roles'},'profile_delta':reference['profile_delta'],'stoploss_delta':reference['stoploss_delta'],'changed_records':reference['changed_records'],'changed_by_call':reference['changed_by_call'],'comparisons':comparisons,'scope':'Independent mapping/capacity/literal-bridge-window/active-family/spectator-map/profile and strict all-p moment proof against every named baseline. Does not replay unchanged local scalar/Clifford providers, global coefficient invoice, or outer admission.'}

def mutation_controls(main,parent,owners_path,work):
 rows=read(owners_path);tests=[]
 def reject(name,fn):
  x=copy.deepcopy(rows);fn(x)
  with tempfile.TemporaryDirectory(prefix='owner-mutation-',dir=work) as td:
   q=Path(td)/'OWNERS.json.gz';q.write_bytes(gzip.compress(json.dumps(x,separators=(',',':')).encode(),mtime=0))
   try:audit(main,parent,q)
   except (AssertionError,IndexError,KeyError,ValueError):tests.append(name);return
   raise AssertionError('Mutation accepted: '+name)
 reject('wrong helper residual width',lambda x:x[0].__setitem__('width',x[0]['width']-1))
 reject('offset exceeds actual pending child',lambda x:x[0].__setitem__('offset',73))
 reject('family formula alias',lambda x:x[0].__setitem__('family',x[0]['family']^1))
 reject('duplicate complete-call helper',lambda x:x[1].__setitem__('helper',x[0]['helper']))
 def overlap(x):
  groups=defaultdict(list)
  for z in x:groups[z['owner_replica'],z['child'],z['port']].append(z)
  zs=next(v for v in groups.values() if len(v)>1)
  zs[1]['offset']=zs[0]['offset']
 reject('overlapping footprints across complete calls',overlap)
 # Preserve named family but borrow it after its literal idle window ends.
 def window(x):
  z=x[0];plan=read(parent/'data/PLAN.json');allowed=plan['windows'][f"{z['owner_replica']},{z['child']}"][1]
  tm=next(t for t in range(72) if t not in allowed);z.update(time=tm,stage=plan['order'][tm][0],replica=plan['order'][tm][1])
 reject('whole-family borrowing outside literal idle window',window)
 return tests

def main():
 a=argparse.ArgumentParser(description=__doc__)
 a.add_argument('--main',type=Path,required=True,help='Pinned main checkout containing the exact DATA-PHASES artifact')
 a.add_argument('--parent',type=Path,required=True,help='Pinned PR656 baseline snapshot from a fresh PR656 replay')
 a.add_argument('--owners',type=Path,required=True)
 a.add_argument('--out',type=Path,required=True)
 a.add_argument('--compare',action='append',default=[],metavar='NAME=OWNERS_PATH',help='Additional baseline owner map, independently checked under the same literal controller and provider')
 a.add_argument('--mutation-controls',action='store_true')
 x=a.parse_args();comparisons={}
 for value in x.compare:
  name,sep,path=value.partition('=');assert sep and name and path and name not in comparisons and name!='PR656'
  comparisons[name]=Path(path)
 r=audit(x.main,x.parent,x.owners,comparisons)
 if x.mutation_controls:r['mutation_controls_rejected']=mutation_controls(x.main,x.parent,x.owners,x.out.parent)
 x.out.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:r[k] for k in ('status','candidate_input','profile_delta','changed_records','scope')},indent=2))
if __name__=='__main__':main()
