"""Portable exact-rational entrance-search helpers. OpenAI Codex,2026-10-11.
Replay and GF(2) containment derive from PR404 shared/reconstruct.py;
retain upstream package notices. Discovery floats nominate,never certify kappa.
"""
from fractions import Fraction as Q

def inside(a,b):
 piv={}
 for u in b:
  while u:
   k=u.bit_length()-1
   if k in piv:u^=piv[k]
   else:piv[k]=u;break
 for u in a:
  while u:
   k=u.bit_length()-1
   if k not in piv:return False
   u^=piv[k]
 return True

def gate_roles(g):return [g[2]]+[r for r,a,b in g[3]]+(g[4] if len(g)>4 else [])
def first_frames(c):
 result={}
 for part in ['A','B']:
  for g in c[part]:
   for r in gate_roles(g):
    if r>=2*c['v'] and g[1] and r not in result:result[r]=g[1]
 return result

def replay(c):
 n=2*c['v']+c['R'];v=c['v'];rows=[{r:Q(1)} for r in range(n)]
 def add(t,source,q):
  for k,a in list(source.items()):
   z=rows[t].get(k,Q(0))+q*a
   if z:rows[t][k]=z
   else:rows[t].pop(k,None)
 for part in ['A','B']:
  if part=='B':
   totals={k:dict(rows[r]) for k,r,f in c['ret']}
   for t,es in enumerate(c['scat']['table']):
    for k,a,b in es:add(v+t,totals[k],Q(a,b))
  for g in c[part]:
   for r,a,b in g[3]:
    t,s=(g[2],r) if g[0]=='in' else (r,g[2]);add(t,dict(rows[s]),Q(a,b))
 return rows
