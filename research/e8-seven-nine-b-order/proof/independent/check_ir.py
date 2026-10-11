"""Independent raw IR, chart-id, COPY lifetime, full prefix and physical namespace check.
OpenAI Codex assistance; inherited PR373/PR376 and source527 provenance retained. Apache-2.0.
"""
from pathlib import Path
from collections import Counter
import json,struct,hashlib
P=Path(__file__).resolve().parent;D=Path('/private/tmp/e8-seven-stage-native-v2/lowering-v1');C=Path('/private/tmp/e8-seven-stage-native-v2/charts/ALL-CHARTS.json');R=Path('/private/tmp/pr376-final-b-order-signed-v1/records')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rd=lambda p:json.loads(p.read_text())
raw=list(struct.iter_unpack('<6i',(R/'249-records.bin').read_bytes()));ir=list(struct.iter_unpack('<8i',(D/'GLOBAL-PROGRAM.bin').read_bytes()));charts=rd(C);st=rd(R/'249-states.json');fs={int(k):v for k,v in rd(R/'frames.json')['frames'].items()};links=rd(P/'IDLE-GAP-LINKS.json');L={(z['port'],z['stage'],z['data_bank'],z['id']):z for z in links['links']}
v=120;helpers=822;one=6*v+helpers;live=7*one;local=2*v+helpers;work=live
assert (st['n'],st['R'],st['h'])==(local,helpers,8)
ACTIVE=[(0,1),(1,0),(0,1),(3,2),(2,3),(5,4),(4,5)]
def addr(s,rep,r):
 if r==local:return work
 if r<2*v:
  block,index=divmod(r,v);return rep*one+ACTIVE[s][block]*v+index
 return rep*one+6*v+r-2*v
chart_keys={(c['before'],c['after'],c['rank']):i for i,c in enumerate(charts)}
def audit(stream):
 columns=[1<<i for i in range(live)]+[0];norm=[1]*live+[0];peak=1;paid=Counter();opcounts=Counter();opened=None;seen_idle=Counter();positive_moves=0;pos=0
 def consume(want=None):
  nonlocal pos,peak,opened,positive_moves
  assert pos<len(stream),'truncated';row=stream[pos];pos+=1
  if want is not None:assert row==want,('lowered-record mismatch',pos,row,want)
  op,x,y,c,r,k,s,rev=row;opcounts[op]+=1
  if op==0:
   assert r>0 and 0<=k<len(charts);ch=charts[k]
   key=(c,y,r)if rev else(y,c,r)
   if x==work:key=(c,y,r) # extraction: frame FULL -> ZERO
   assert (ch['before'],ch['after'],ch['rank'])==key,('chart-id mismatch',pos)
   paid[r]+=1;positive_moves+=1
  elif op in(1,5):
   assert 0<=x<live and 0<=y<=live and x!=y
   if y==work:assert opened is not None
   if opened is not None:assert x!=opened,'write borrowed source'
   if c&1:columns[x]^=columns[y]
   norm[x]+=abs(c)*norm[y]
  elif op==2:
   assert x==work and opened is None and norm[work]==0 and columns[work]==0
   assert 0<=y<live;opened=y;columns[work]=columns[y];norm[work]=norm[y]
  elif op==3:
   assert x==work and opened is not None and columns[work]==columns[opened]
   columns[work]=0;norm[work]=0;opened=None
  elif op==4:
   rep,inrep=divmod(x,one);bank,port=divmod(inrep,v);assert rep<7 and bank<6
   key=(port,s,bank,k);assert key in L and L[key]['rank']==r,'unbound idle child'
   assert y==-1 and c==0 and rev==0;seen_idle[key]+=1;paid[r]+=1
  elif op==7:
   assert opened is None;columns[x],columns[y]=columns[y],columns[x];norm[x],norm[y]=norm[y],norm[x]
  else:raise AssertionError(('unknown-op',op))
  peak=max(peak,norm[x]);return row
 for stage in range(7):
  rev=stage%2
  for rep in range(7):
   before=columns[rep*one:rep*one+6*v].copy();expected=before.copy();src,dst=ACTIVE[stage]
   for t in range(v):expected[dst*v+t]^=before[src*v+t]
   for op,a,b,c,f,z in reversed(raw)if rev else raw:
    x=addr(stage,rep,a)
    if op==0:
     old,new=(c,b)if rev else(b,c);consume((0,x,old,new,f,chart_keys[(b,c,f)],stage,rev))
    elif op==1:consume((1,x,addr(stage,rep,b),-c if rev else c,f,z,stage,rev))
    elif op==(3 if rev else 2):
     consume((2,work,x,0,c,0,stage,rev));consume((0,work,c,f,8,chart_keys[(f,c,8)],stage,rev))
    else:
     assert op==(2 if rev else 3);consume((3,work,-1,0,f,0,stage,rev))
   assert opened is None and columns[rep*one:rep*one+6*v]==expected,'wrong local shear'
   assert all(columns[rep*one+r]==1<<(rep*one+r)for r in range(6*v,one)),'local dirty restore'
  # Consume only bridge/idle rows here; exact stream identities are independently bound below.
  while pos<len(stream)and stream[pos][0]in(4,5):
   op,x,y,c,r,k,s,rev=consume();assert s==stage
   if op==5:
    rep,xr=divmod(x,one);rep2,yr=divmod(y,one);assert rep==rep2 and xr%v==yr%v
    edges={1:{(0,2):1,(3,1):-1},2:{(3,1):1,(0,2):-1},3:{(2,4):1,(5,3):-1},4:{(5,3):1,(2,4):-1},6:{(3,5):-1,(4,2):1,(1,3):-1,(2,0):1}}
    assert edges.get(stage,{}).get((xr//v,yr//v))==c and r==rev==0 and k==stage,'wrong bridge'
 for rep in range(7):
  for pair in range(3):
   for t in range(v):consume((7,rep*one+2*pair*v+t,rep*one+(2*pair+1)*v+t,-1,0,0,-1,0))
 assert pos==len(stream)and opened is None
 assert all(x==1<<i for i,x in enumerate(columns[:live]))and columns[-1]==0,'global F2 endpoint'
 assert set(seen_idle)==set(L)and all(n==7 for n in seen_idle.values()),'missing/duplicate idle child'
 return dict(records=pos,paid=dict(sorted(paid.items())),paid_calls=sum(paid.values()),rank_mass=sum(r*n for r,n in paid.items()),prefix=peak,bits=peak.bit_length(),opcode_counts=dict(opcounts),all_f2_columns=live,linked_local_move_occurrences=positive_moves,linked_idle_occurrences=sum(seen_idle.values()))
result=audit(ir);assert result['rank_mass']==602952 and result['paid_calls']==219695 and result['prefix']==1676572497474094192863
# The physical data namespace is packed contiguously; helper slots occupy a disjoint tail.
data=[dict(virtual_family=rep*one+b*v+t,physical_bank=rep*6*v+b*v+t)for rep in range(7)for b in range(6)for t in range(v)];assert len({d['virtual_family']for d in data})==len({d['physical_bank']for d in data})==5040
slots=rd(D/'BANK-SLOTS.json');occupied=set();keys=set()
for z in slots:
 s,rep=z['stage'],z['replica'];r=z['virtual_family']-rep*one-6*v;assert 0<=s<7 and 0<=rep<7 and 0<=r<helpers
 k=(s,rep,r);assert k not in keys;keys.add(k);flat=rep*helpers+r;assert(z['physical_bank'],z['offset'],z['width'],z['route'],z['chart'])==(5040+s*helpers+flat//7,8*(flat%7),8,['tau',s],'identity')
 for j in range(z['offset'],z['offset']+8):
  key=z['physical_bank'],j;assert key not in occupied;occupied.add(key)
assert len(keys)==7*7*helpers and occupied=={(bank,j)for bank in range(5040,live)for j in range(56)}
(P/'DATA-FAMILY-MAP.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
controls=[]
def reject(name,mutate):
 q=ir.copy();mutate(q)
 try:audit(q)
 except AssertionError as e:controls.append(dict(name=name,rejected=True,reason=str(e)[:200]))
 else:raise AssertionError('mutant accepted '+name)
idx=next(i for i,z in enumerate(ir)if z[0]==5)
reject('omit_first_bridge',lambda q:q.pop(idx))
idxc=next(i for i,z in enumerate(ir)if z[0]==0 and z[1]!=work)
def badchart(q):
 a=list(q[idxc]);a[5]=(a[5]+1)%len(charts);q[idxc]=tuple(a)
reject('substitute_move_chart',badchart)
idxi=next(i for i,z in enumerate(ir)if z[0]==4)
def badidle(q):
 a=list(q[idxi]);a[5]+=2;q[idxi]=tuple(a)
reject('wrong_idle_gap_id',badidle)
idxcp=next(i for i,z in enumerate(ir)if z[0]==2)
def badcopy(q):
 a=list(q[idxcp]);a[2]+=1;q[idxcp]=tuple(a)
reject('different_borrowed_center',badcopy)
idxa=next(i for i,z in enumerate(ir)if z[0]==1 and z[7]==1)
def badsign(q):
 a=list(q[idxa]);a[3]=-a[3];q[idxa]=tuple(a)
reject('wrong_reflected_add_sign',badsign)
result.update(status='PASS_INDEPENDENT_RAW_IR_F2_PREFIX_CHART_IDLE_COPY_AND_BANK_LINKS',program_sha256=sha(D/'GLOBAL-PROGRAM.bin'),charts_sha256=sha(C),idle_links_sha256=sha(P/'IDLE-GAP-LINKS.json'),bank_slots_sha256=sha(D/'BANK-SLOTS.json'),data_map_sha256=sha(P/'DATA-FAMILY-MAP.json'),bank_slot_count=len(slots),bank_coordinates=len(occupied),negative_controls=controls,scope='IR scalar families and completed physical bank namespace are distinct. DATA-FAMILY-MAP plus BANK-SLOTS binds all data families and every stage/replica helper window. This check verifies that address plan, exact local scalar stream, F2 endpoint and true raw prefix; it does not turn the finite plan into an all-size compiler proof.',AI='OpenAI Codex assistance, Apache-2.0')
(P/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
