"""Concrete E8 seven-stage word, literal replicas, projector links and bank slots.
PR234/source527: Henry Grant and eumemic; E8: Jacob Sussman; local bit word:
Dylan Crow/Claude; B3: DaysSky/Claude; helper reuse: PR376 contributors/Codex.
This independent finite lowering was prepared with OpenAI Codex. Apache-2.0.
"""
import argparse,json,struct,hashlib
from pathlib import Path
from collections import Counter
from fractions import Fraction
assert __debug__
p=argparse.ArgumentParser();p.add_argument('--records',type=Path,required=True);p.add_argument('--charts',type=Path,required=True);p.add_argument('--price',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(exist_ok=False)
read=lambda f:json.loads(f.read_text());sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
st=read(a.records/'249-states.json');fs=read(a.records/'frames.json')['frames'];ev=list(struct.iter_unpack('<6i',(a.records/'249-records.bin').read_bytes()))
H,V,R=st['h'],st['v'],st['R'];K,S,T=3,7,7;M=S*H;LOCAL=2*V+R;ONE=2*K*V+R;LIVE=T*ONE;WORK=LIVE
assert H==8 and V==120 and LOCAL==st['n'];dim={int(k):v['dim'] for k,v in fs.items()};ZERO=st['ZERO'];FULL=next(k for k,d in dim.items() if d==H)
assert all(st['initial'][str(r)]==ZERO and st['final'][str(r)]==FULL for r in range(2*V,LOCAL))
MOVE,ADD,COPY,ERASE,IDLE,BRIDGE,COMPLETE,EXCHANGE=range(8);PACK=struct.Struct('<8i')
ACTIVE=((0,1),(1,0),(0,1),(3,2),(2,3),(5,4),(4,5))
# Explicit unsplit chronology. Splits are linked to PR373's exact dyadic gap witnesses.
idle={1:((2,14,0),(3,14,1)),2:((2,7,2),(3,7,3)),3:((4,28,4),(5,28,5)),4:((4,7,6),(5,7,7)),6:((0,34,8),(1,34,9),(2,20,10),(3,20,11),(4,6,12),(5,6,13))}
bridges={1:((0,2,1),(3,1,-1)),2:((3,1,1),(0,2,-1)),3:((2,4,1),(5,3,-1)),4:((5,3,1),(2,4,-1)),6:((3,5,-1),(4,2,1),(1,3,-1),(2,0,1))}
def family(stage,rep,r):
 assert 0<=r<=LOCAL
 if r==LOCAL:return WORK
 if r<V:return rep*ONE+ACTIVE[stage][0]*V+r
 if r<2*V:return rep*ONE+ACTIVE[stage][1]*V+r-V
 return rep*ONE+2*K*V+r-2*V
localH=Counter();required=set();adds=copies=0
for op,x,y,c,f,z in ev:
 if op==MOVE and f:localH[f]+=1;required.add((y,c,f))
 elif op==ADD:adds+=1
 elif op==COPY:localH[z]+=1;copies+=1;required.add((ZERO,c,z))
assert copies==9
charts=read(a.charts/'ALL-CHARTS.json');index={(c['before'],c['after'],c['rank']):i for i,c in enumerate(charts)};assert set(index)==required and len(index)==len(charts)
for chart in charts:
 C=[[Fraction(x) for x in r] for r in chart['basis']];I=[[Fraction(x) for x in r] for r in chart['inverse']]
 assert len(C)==len(I)==H and all(len(r)==H for r in C+I)
 assert all(sum(C[i][k]*I[k][j] for k in range(H))==int(i==j) for i in range(H) for j in range(H))
counts=Counter();paid=Counter();stages=[];norm=[1]*LIVE+[0];f2=[1<<i for i in range(LIVE)]+[0];maxnorm=1
program=a.output/'GLOBAL-PROGRAM.bin'
with program.open('wb') as out:
 def emit(row):
  global maxnorm
  op,x,y,c,rank,chart,stage,rev=row
  if op in (ADD,BRIDGE):
   assert x!=y and 0<=x<LIVE and 0<=y<=LIVE
   norm[x]+=abs(c)*norm[y]
   if c%2:f2[x]^=f2[y]
  elif op==COPY:norm[x]=norm[y];f2[x]=f2[y]
  elif op==ERASE:norm[x]=0;f2[x]=0
  elif op==EXCHANGE:norm[x],norm[y]=norm[y],norm[x];f2[x],f2[y]=f2[y],f2[x]
  maxnorm=max(maxnorm,norm[x]);out.write(PACK.pack(*row));counts[op]+=1
 for stage in range(S):
  rev=stage%2==1;stageH=Counter();stage_adds=cp=er=0
  for rep in range(T):
   opened=False;source=None;images=[family(stage,rep,r) for r in range(LOCAL+1)];assert len(set(images))==LOCAL+1
   for op,x,y,c,f,z in (reversed(ev) if rev else ev):
    if op==MOVE:
     before,after=(c,y) if rev else (y,c);rank=f;key=(y,c,rank);idx=index[key] if rank else -1
     row=(MOVE,family(stage,rep,x),before,after,rank,idx,stage,int(rev));stageH[rank]+=int(rank>0)
    elif op==ADD:
     dst,src=family(stage,rep,x),family(stage,rep,y);assert dst!=WORK
     if src==WORK:assert opened and f==ZERO and z==3
     if opened:assert dst!=source
     row=(ADD,dst,src,-c if rev else c,f,z,stage,int(rev));stage_adds+=1
    elif op==(ERASE if rev else COPY):
     assert not opened;source=family(stage,rep,x);assert x>=2*V and dim[c]==H;opened=True;cp+=1
     emit((COPY,WORK,source,0,c,0,stage,int(rev)))
     rank=z if not rev else dim[c];assert rank==H and f==ZERO
     row=(MOVE,WORK,c,f,rank,index[(ZERO,c,rank)],stage,int(rev));stageH[rank]+=1
    else:
     assert op==(COPY if rev else ERASE) and opened and f==ZERO
     row=(ERASE,WORK,-1,0,f,0,stage,int(rev));opened=False;source=None;er+=1
    emit(row)
   assert not opened
   # Every local unit restores all dirty helpers in its actual F2 program.
   for r in range(2*K*V,ONE):assert f2[rep*ONE+r]==1<<(rep*ONE+r)
  assert cp==er==T*copies and stage_adds==T*adds
  stageH.pop(0,None);assert stageH==Counter({k:T*n for k,n in localH.items()});paid.update(stageH)
  stages.append(dict(stage=stage,reverse=rev,copies=cp,erasures=er,adds=stage_adds,paid=dict(stageH),max_prefix_l1=maxnorm))
  for rep in range(T):
   for bank,rank,gap in idle.get(stage,()):
    parts=[27,rank-27] if rank>27 else [rank]
    for childno,child in enumerate(parts):
     for t in range(V):emit((IDLE,rep*ONE+bank*V+t,-1,0,child,gap*2+childno,stage,0));paid[child]+=1
   for dst,src,c in bridges.get(stage,()):
    for t in range(V):emit((BRIDGE,rep*ONE+dst*V+t,rep*ONE+src*V+t,c,0,stage,stage,0))
 for rep in range(T):
  for bank in range(0,2*K,2):
   for t in range(V):emit((EXCHANGE,rep*ONE+bank*V+t,rep*ONE+(bank+1)*V+t,-1,0,0,-1,0))
assert all(x==1<<i for i,x in enumerate(f2[:-1])) and f2[-1]==0
assert counts[COPY]==counts[ERASE]==S*T*copies and counts[BRIDGE]==12*V*T and counts[EXCHANGE]==K*V*T
rankmass=sum(k*n for k,n in paid.items());deficit=M*LIVE-rankmass;assert deficit==T*((2*K)*V-S*copies*H)==1512
assert maxnorm < 2**104
price=read(a.price)
assert price['m']==M and price['W']==LIVE
ph=price['normalized_histogram'];assert {int(k):v for k,v in ph.items()}==dict(paid)
assert sum(int(k)*n for k,n in ph.items())==rankmass and M*price['W']-rankmass==deficit
# Physical slots are a separate address namespace from virtual family numbers.
per_stage=T*R//S;assert T*R%S==0;slots=[];seen=set()
for stage in range(S):
 for rep in range(T):
  for helper in range(R):
   flat=rep*R+helper;bank=flat//S;offset=H*(flat%S);physical=2*K*V*T+stage*per_stage+bank
   for j in range(offset,offset+H):assert (physical,j) not in seen;seen.add((physical,j))
   slots.append(dict(stage=stage,replica=rep,virtual_family=rep*ONE+2*K*V+helper,physical_bank=physical,offset=offset,width=H,route=['tau',stage],chart='identity'))
assert len(seen)==S*T*R*H and 2*K*V*T+S*per_stage==LIVE
# Each bank's S independent width-H transpositions cover exactly all M coordinates.
def permutation(order):
 p=list(range(2*M))
 for block in order:
  for j in range(H*block,H*(block+1)):p[j],p[M+j]=p[M+j],p[j]
 return p
want=[(j+M)%(2*M) for j in range(2*M)];assert permutation(range(S))==permutation(reversed(range(S)))==want
controls=[]
for block in range(S):
 for mode,seq in [('omit',[i for i in range(S) if i!=block]),('repeat',list(range(S))+[block])]:
  bad=sum(x!=y for x,y in zip(permutation(seq),want));assert bad==2*H;controls.append(dict(mode=mode,block=block,differing_columns=bad))
(a.output/'BANK-SLOTS.json').write_text(json.dumps(slots,separators=(',',':'))+'\n')
result=dict(status='PASS_EXPLICIT_SEVEN_STAGE_LOWERING_CHART_LINKS_F2_ENDPOINT_BANKS_AND_FULL_PREFIX',source={n:sha(a.records/n) for n in ['249-records.bin','249-states.json','frames.json']},charts_sha256=sha(a.charts/'ALL-CHARTS.json'),price_sha256=sha(a.price),program_sha256=sha(program),stages=stages,opcode_counts=dict(counts),literal_stock=LIVE,width=M,replicas=T,paid_histogram=dict(sorted(paid.items())),paid_calls=sum(paid.values()),rank_mass=rankmass,deficit=deficit,all_f2_columns=LIVE,banks_per_stage=per_stage,physical_banks=S*per_stage,role_stage_assignments=len(slots),bank_slots_sha256=sha(a.output/'BANK-SLOTS.json'),bank_controls=controls,full_seven_stage_cancellation_free_prefix=maxnorm,payload_bits=maxnorm.bit_length(),legacy_five_stage_payload_guard_used=False,scope='Exact renamed seven-stage raw-bit program with scalar F2 endpoint, dirty helpers, COPY lifetimes, all local paid MOVE chart links, and explicit completed-bank slots. Source-level signed decoder, all-port stage/idle geometry, finite invoice and all-size transfer require separate receipts.')
(a.output/'LOWERING-BANKS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'], 'records',sum(counts.values()), 'prefixbits',result['payload_bits'])
