"""Construct free sink uncomputes on a gcert word: for helper r, after its last Y-influence, subtract an exact rational
combination of other helpers that sit at r's exact frame (no donor advance), so the final clean x-row of r is zero."""
import sys,json,gzip
from fractions import Fraction as Fr
from collections import Counter,defaultdict
import os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','complex','gx')); import gxcore as G
def cf(k): ng,a,b=k; return Fr(-a if ng else a,b)
def analyse(c):
  D=G.normal(json.loads(json.dumps(c)))
  dim=[len(x) for x in D['frames']]; v=D['v'];R=D['R'];n=2*v+R
  gates=D['A']+D['B']; nA=len(D['A']); NG=len(gates)
  val=[({r:Fr(1)} if r<v else {}) for r in range(n)]
  ver=defaultdict(list); cur=list(D['start']); lab=defaultdict(list)
  for r in range(n): ver[r].append((0,{})) if r>=v else ver[r].append((0,dict(val[r]))); lab[r].append((0,cur[r]))
  for i,g in enumerate(gates):
    t=i+1
    if i==nA:
      tot=[dict(val[s]) for s,_ in D['ret']]
      for tt in range(v):
        for kk,cc in G.scat_row(D,tt):
          for key,x in tot[kk].items(): val[v+tt][key]=val[v+tt].get(key,0)+cf(cc)*x
    for r in G.regs(g):
      if cur[r]!=g[1]: cur[r]=g[1]; lab[r].append((t,g[1]))
    src=dict(val[g[2]]) if g[0]=='out' else None
    for tg,s,k in G.adds(g):
      sv=src if g[0]=='out' else val[s]
      d=val[tg]
      for key,x in sv.items():
        d[key]=d.get(key,0)+cf(k)*x
        if d[key]==0: del d[key]
      ver[tg].append((t,dict(d)))
  w=defaultdict(dict)
  for y in range(v): w[v+y]={y:Fr(1)}
  tau={}
  for t in range(NG,-1,-1):
    for r in range(2*v,n):
      if r not in tau and any(w[r].values()): tau[r]=t
    if t==0: break
    g=gates[t-1]
    for tg,s,k in reversed(G.adds(g)):
      cc=cf(k)
      for y,x in list(w[tg].items()): w[s][y]=w[s].get(y,0)+cc*x
    if t-1==nA:
      for tt in range(v):
        for kk,c2 in G.scat_row(D,tt):
          s=D['ret'][kk][0]
          for y,x in w[v+tt].items(): w[s][y]=w[s].get(y,0)+cf(c2)*x
  fin=[dim[D['final'][r]]-dim[cur[r]] for r in range(n)]
  return D,dim,ver,lab,tau,fin,NG,val
def ivs(L,END):
  return [(fr,ts,(L[i+1][0] if i+1<len(L) else END+1)) for i,(ts,fr) in enumerate(L)]
def solve(target,cands):
  """cands: list of (key,vec). returns {key:coef} with sum coef*vec == target, exact, or None"""
  basis={}  # pivot -> (vec, combo)
  def red(x,combo):
    x=dict(x);combo=dict(combo)
    while x:
      p=min(x)
      if p not in basis: return x,combo
      c=x[p]; bv,bc=basis[p]
      for k,vv in bv.items():
        x[k]=x.get(k,0)-c*vv
        if x[k]==0: del x[k]
      for k,vv in bc.items():
        combo[k]=combo.get(k,0)-c*vv
        if combo[k]==0: del combo[k]
    return x,combo
  for key,vec in cands:
    x,cb=red(vec,{key:Fr(1)})
    if x:
      p=min(x);c=x[p]; basis[p]=({k:a/c for k,a in x.items()},{k:a/c for k,a in cb.items()})
  x,cb=red(target,{})
  if x: return None
  return {k:-a for k,a in cb.items()}  # target - sum(...)=0 => target = sum(-cb)
def find(c,r,exclude=(),an=None):
  D,dim,ver,lab,tau,fin,NG,val=an or analyse(c)
  t0=tau.get(r,-1)+1; target=val[r]
  if not target: return []
  Lr=[(fr,max(ts,t0),te) for fr,ts,te in ivs(lab[r],NG) if te>t0]
  v=D['v'];n=2*v+D['R']; cands=[]
  for u in range(2*v,n):
    if u==r or u in exclude: continue
    for fr,ts,te in ivs(lab[u],NG):
      for frr,a,b in Lr:
        if fr!=frr: continue
        lo,hi=max(ts,a),min(te,b)
        if lo>=hi: continue
        vs=ver[u]
        for j,(tv,vec) in enumerate(vs):
          vend=vs[j+1][0] if j+1<len(vs) else NG+1
          s0,s1=max(tv,lo),min(vend,hi)
          if s0<s1 and vec and s0>=1: cands.append(((u,s0,fr),vec))
  # prefer later times? keep order: fewer distinct gates -> sort by time
  sol=solve(target,cands)
  if sol is None: return None
  gates=defaultdict(list)
  for (u,s0,fr),a in sol.items():
    gates[(s0,fr)].append([u,-a.numerator,a.denominator])   # r -= a*u  => coefficient -a
  return [dict(sink_helper=r,cut_group=s0-1,frame=fr,uncompute=sorted(us)) for (s0,fr),us in sorted(gates.items())]
def nested(fr,a,b): return all(G.reduce(u,fr[b])==0 for u in fr[a])
def find_adv(c,r,exclude=(),noadv=()):
  """as find, but donors may also be advanced early along their own walk (fu < L_r < fn); returns (gates, splits)"""
  D,dim,ver,lab,tau,fin,NG,val=analyse(c)
  fr=D['frames']; t0=tau.get(r,-1)+1; target=val[r]
  if not target: return [],[]
  Lr=[(f,max(ts,t0),te) for f,ts,te in ivs(lab[r],NG) if te>t0]
  v=D['v'];n=2*v+D['R']
  touch=defaultdict(list)
  for i,g in enumerate(D['A']+D['B']):
    for x in G.regs(g): touch[x].append(i+1)
  free=[];adv=[]
  for u in range(2*v,n):
    if u==r or u in exclude: continue
    I=ivs(lab[u],NG)
    for j,(fu,ts,te) in enumerate(I):
      fn=I[j+1][0] if j+1<len(I) else D['final'][u]
      for f,a,b in Lr:
        lo,hi=max(ts,a),min(te,b)
        if lo>=hi: continue
        vs=ver[u]
        for k,(tv,vec) in enumerate(vs):
          vend=vs[k+1][0] if k+1<len(vs) else NG+1
          s0,s1=max(tv,lo),min(vend,hi)
          if s0>=s1 or not vec or s0<1: continue
          if fu==f: free.append(((u,s0,f),vec)); continue
          if u in noadv: continue
          # advance: need fu<f<=fn strictly nested and no touch of u in (s,te) at fu
          lt=max([x for x in touch[u] if x<te],default=0)
          s=max(s0,lt)
          if s>=s1 or s<1: continue
          if dim[fu]<dim[f] and nested(fr,fu,f) and (fn==f or (dim[f]<dim[fn] and nested(fr,f,fn))):
            cost=(dim[fu],dim[f],dim[fn])
            if fn==f: free.append(((u,s,f),vec))
            else: adv.append((cost,(u,s,f),vec))
  adv.sort(key=lambda x:(x[0][1]-x[0][0])*(x[0][2]-x[0][1]))
  cands=free+[(k,vec) for _,k,vec in adv]
  sol=solve(target,cands)
  if sol is None: return None,None
  costs={k:cost for cost,k,_ in adv}
  splits=[costs[k] for k in sol if k in costs]
  gates=defaultdict(list)
  for (u,s0,f),a in sol.items(): gates[(s0,f)].append([u,-a.numerator,a.denominator])
  return [dict(sink_helper=r,cut_group=s0-1,frame=f,uncompute=sorted(us)) for (s0,f),us in sorted(gates.items())],splits
