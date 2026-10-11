"""Exact data phases, signed bridges, and the inherited finite schedule.
Adapted from Zhihao Chen PR377, icekylinx PR433 and DaysSky PR442.
Chafreaky with OpenAI Codex assistance. Apache-2.0.
"""
M,H,K,L,T,V,R=89,9,5,11,8,120,560
W=2*K*V*T
def polynomial(terms):
 linear=[0]*M;quadratic=[0]*M
 for vector,sign in terms:
  assert 0<=vector<1<<M and sign in (-1,1)
  for i in range(M):
   if vector>>i&1:linear[i]=(linear[i]+sign)%4;quadratic[i]^=vector
 return linear,quadratic

def phases(ph,ports):
 assert ph['m']==M and ph['ports']==V and len(ph['recipes'])==V
 assert ph['terminal_omission_controls_rejected']==V and ph['cover_correction']['mandatory']
 checked=0
 for port,q in enumerate(ports):
  rec=ph['recipes'][port];assert rec['port']==port and rec['q']==q and q.bit_count()%2==1 and q.bit_count()!=H
  zero=next(i for i in range(H) if not q>>i&1);reflect=q^(1<<zero)
  order=[zero]+[i for i in range(H) if i!=zero]
  # Parent basis orders the remaining axes by swapping axis zero and 'zero'.
  order=list(range(H));order[0],order[zero]=order[zero],order[0]
  basis=[(1<<i)^(reflect if (reflect>>i)&1 else 0) for i in order]+[1<<i for i in range(H,M)]
  assert basis[0]==q and all((a&b).bit_count()%2==int(i==j) for i,a in enumerate(basis) for j,b in enumerate(basis))
  def desired(level,side):
   if level<0:return [(q,1)] if side==0 else []
   return [(1<<i,1) for i in range(H+8*level)]+([] if side==0 else [(q,-1)])
  def route(vector,level):
   if level==0:return vector
   off=H+8*(level-1);answer=0
   for i in range(H):
    if vector>>i&1:
     answer^=(q if q>>i&1 else 0)
     for j in range(8):
      if basis[j+1]>>i&1:answer^=1<<(off+j)
   for j in range(8):
    if vector>>(off+j)&1:answer^=basis[j+1]
   mask=((1<<H)-1)|(((1<<8)-1)<<off)
   answer^=vector&~mask;return answer
  assert len(rec['stage_alignment'])==L
  for s,alignment in enumerate(rec['stage_alignment']):
   columns=[route(1<<i,s) for i in range(M)]
   assert all(route(columns[i],s)==1<<i for i in range(M))
   assert all((a&b).bit_count()%2==int(i==j) for i,a in enumerate(columns) for j,b in enumerate(columns))
   for name,local,level,side,entry in [
    ('entry_X',[(q,1)],s-1,0,True),('entry_Y',[],s-1,1,True),
    ('exit_X',[(1<<i,1) for i in range(H)],s,0,False),
    ('exit_Y',[(1<<i,1) for i in range(H)]+[(q,-1)],s,1,False)]:
    terms=local+[(1<<i,1) for i in range(H,H+8*s)]
    actual=[(route(v,s),sgn) for v,sgn in terms];canonical=desired(level,side)
    a,b=(canonical,actual) if entry else (actual,canonical)
    la,qa=polynomial(a);lb,qb=polynomial(b);shift=alignment[name]
    assert 0<=shift<1<<M and qa==qb
    assert all((la[i]+2*((shift>>i)&1))%4==lb[i] for i in range(M));checked+=1
  expected=[]
  for j in range(1,K):
   for side in range(2):expected.extend([(-1,2*j-1,side),(2*j-1,2*j,side)])
  for j in range(K):
   for side in range(2):expected.append((2*j+2,L-1,side))
  assert len(rec['idle_children'])==len(expected)
  for child,(a,b,side) in zip(rec['idle_children'],expected):
   axes=child['orthogonal_axes'];assert child['rank']==len(axes)==8*(b-a)
   assert all(v in basis for v in axes) and len(set(axes))==len(axes)
   la,qa=polynomial([(v,1) for v in axes]);lb,qb=polynomial([(v,-sgn) for v,sgn in desired(a,side)]+desired(b,side))
   shift=child['translation_after'];assert 0<=shift<1<<M and qa==qb
   assert all((la[i]+2*((shift>>i)&1))%4==lb[i] for i in range(M));checked+=1
  la,qa=polynomial([(q,-1)]+desired(L-1,1));lb,qb=polynomial([(1<<i,1) for i in range(M)])
  assert rec['terminal_Y_translation']==q and qa==qb and la!=lb
  assert all((la[i]+2*((q>>i)&1))%4==lb[i] for i in range(M));checked+=1
 return checked

def bridge_controls(recipe):
 def matrix(skip):
  rows=[[int(i==j) for j in range(10)] for i in range(10)];count=0
  def add(d,s,c):rows[d]=[x+c*y for x,y in zip(rows[d],rows[s])]
  for e in recipe:
   if e['kind']=='local':
    p=e['pair'];add(2*p,2*p+1,-1) if e['reverse'] else add(2*p+1,2*p,1)
   elif e['kind']=='bridge':
    a,b,c=e['dst'],e['src'],e['coefficient']
    for d,s,sign in [(2*a,2*b,c),(2*b+1,2*a+1,-c)]:
     if count!=skip:add(d,s,sign)
     count+=1
   else:
    for j in range(5):rows[2*j],rows[2*j+1]=rows[2*j+1],[-x for x in rows[2*j]]
  assert count==24;return rows
 ident=[[int(i==j) for j in range(10)] for i in range(10)]
 assert matrix(-1)==ident
 for skip in range(24):assert matrix(skip)!=ident
 return list(range(24))

def schedule_check(t):
 assert (t['m'],t['h'],t['stages'],t['replicas'],t['live'],t['physical'])==(M,H,L,T,W,10178)
 assert t['cover']=='all matrices in O(89,2), in lexicographic row order'
 assert t['bank_padding'] is None and t['private_namespace']==dict(centers=[W,W+16],tableau=[W+16,W+576],coefficient=[W+576,W+578])
 rows=[[int(i==j) for j in range(2*K)] for i in range(2*K)];levels=[-1]*K;last={};locals_=[];idle={};wins={};bridges=0;terminal=False;translated=False;corrected=False
 def add(d,s,c):rows[d]=[x+c*y for x,y in zip(rows[d],rows[s])]
 for position,e in enumerate(t['execution_schedule']):
  assert not corrected;kind=e['kind']
  if kind=='local':
   s,p,rev=e['stage'],e['pair'],e['reverse'];assert not terminal and s==len(locals_) and p==max(0,(s-1)//2) and rev==bool(s%2)
   assert levels[p]==s-1;levels[p]=s;locals_.append((position,s,p));last[p]=position
   add(2*p,2*p+1,-1) if rev else add(2*p+1,2*p,1)
  elif kind=='bridge':
   a,b,c=e['dst'],e['src'],e['coefficient'];assert 0<=a<K and 0<=b<K and a!=b and c in (-1,1) and levels[a]==levels[b] and not terminal
   add(2*a,2*b,c);add(2*b+1,2*a+1,-c);last[a]=last[b]=position;bridges+=1
  elif kind=='idle':
   i,p,lo,hi=e['idx'],e['pair'],e['source_level'],e['target_level'];assert i==len(idle) and levels[p]==lo and lo<=hi<L and e['rank']==8*(hi-lo)
   levels[p]=hi;idle[i]=e;wins[i]={s for pos,s,pp in locals_ if last.get(p,-1)<pos<position and pp!=p}
   expected=[4*(i//2)+i%2,4*(i//2)+2+i%2] if i<8 else [16+2*(i-8),17+2*(i-8)]
   assert e['phase_children']==expected
  elif kind=='terminal_Y_translations':
   assert levels==[L-1]*K and not terminal and not translated and e==dict(kind=kind,**t['terminal_translations']);translated=True
  elif kind=='terminal':
   assert translated and not terminal
   for j in range(K):rows[2*j],rows[2*j+1]=rows[2*j+1],[-x for x in rows[2*j]]
   terminal=True
  else:
   assert kind=='translate_every_live_family' and terminal and e==t['cover_final_correction'];corrected=True
 assert corrected and rows==[[int(i==j) for j in range(2*K)] for i in range(2*K)] and len(locals_)==L and bridges==12
 assert [e for e in t['execution_schedule'] if e['kind'] in ('local','bridge','terminal')]==t['recipe']
 assert t['terminal_translations']==dict(pairs=list(range(K)),vector='port q transported by cover matrix')
 assert t['cover_final_correction']==dict(kind='translate_every_live_family',formula='delta_i=(weight(row_i(g))-1)/2 mod 2',families=[0,W],charged_calls_per_cover=W,must_follow_data_signed_exchange=True)
 assert t['hosting']['windows']=={str(i):[e['pair'],e['rank'],sorted(wins[i])] for i,e in idle.items() if e['rank'] and wins[i]}
 return len(locals_),bridges,len(idle)
