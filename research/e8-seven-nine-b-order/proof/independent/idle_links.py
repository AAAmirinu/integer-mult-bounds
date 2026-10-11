"""Exact per-port binding of PR373 dyadic idle gaps to emitted seven-stage IR ids. OpenAI Codex, Apache-2.0."""
from pathlib import Path
import json,gzip,hashlib,importlib.util,sys
import sympy as sp
P=Path(__file__).resolve().parent;SRC=Path('/private/tmp/pr376-frozen-source-v1/research/e8-bit-seven-stage/code/bit/checkers/geometry_k.py');W=Path('/private/tmp/pr376-final-b-order-signed-v1/word.json.gz')
s=importlib.util.spec_from_file_location('geok',SRC);g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
w=json.load(gzip.open(W,'rt'));h=8;S=7;M=56;G=sp.eye(h)/2;L=[sp.Matrix(x)for x in w['lines']];geo=g.Geo(h,G,L[0],S);I=sp.eye(M);Z=sp.zeros(M)
ip=lambda a,b:(a.T*G*b)[0]
def reflect(q):return sp.eye(h)-q*(q.T*G)*2/ip(q,q)
isom={0:sp.eye(h)};queue=[0]
for a in queue:
 for b in range(len(L)):
  if b not in isom and abs(ip(L[a],L[b]))==1:
   q=L[a]-L[b]if ip(L[a],L[b])==1 else L[a]+L[b];isom[b]=reflect(q)*isom[a];queue.append(b)
assert len(isom)==120
canon=lambda x:json.dumps(x,separators=(',',':'),sort_keys=True).encode()
def mhash(A):return hashlib.sha256(canon([[str(z)for z in r]for r in A.tolist()])).hexdigest()
links=[]
# Geometry order from PR373: first four gaps for pair2, next four pair3, then terminal pair1,2,3.
meta=[(1,2),(1,3),(2,2),(2,3),(3,4),(3,5),(4,4),(4,5),(6,0),(6,1),(6,2),(6,3),(6,4),(6,5)]
for t in range(120):
 port=L[t];Q=geo.frame_projector(port.T);p=sp.diag(Q,*[sp.zeros(h)for _ in range(S-1)]);rho=[geo.rho(i,isom[t],isom[t].T)for i in range(S)];pieces={'P':Q,'K':sp.eye(h)-Q,'H':sp.eye(h),'0':sp.zeros(h)};data=lambda i,k:rho[i]*geo.stage_projector(i,pieces[k])*rho[i]
 pairs=[]
 for q in (2,3):pairs.extend([(p,data(2*q-3,'H')),(Z,data(2*q-3,'K')),(data(2*q-2,'P'),data(2*q-1,'P')),(data(2*q-2,'0'),data(2*q-1,'0'))])
 for q in (1,2,3):pairs.extend([(data(2*q,'H'),I),(data(2*q,'K'),I-p)])
 assert len(pairs)==14
 for gap,(a,b)in enumerate(pairs):
  assert a*b==b*a==a and (b-a)**2==b-a;r=int((b-a).trace());mid=geo.intermediate(a,b,27,L)if r>27 else None;chain=[a,mid,b]if mid is not None else[a,b]
  for child,(u,v)in enumerate(zip(chain,chain[1:])):
   d=v-u;rank=int(d.trace());assert d*d==d and u*v==v*u==u and 0<2*rank<56
   stage,bank=meta[gap];links.append(dict(port=t,id=gap*2+child,gap=gap,child=child,stage=stage,data_bank=bank,rank=rank,before_sha256=mhash(u),after_sha256=mhash(v),gap_sha256=mhash(d)))
 print('port',t,'PASS',flush=True) if t%30==0 else None
out=dict(status='PASS_ALL_120_PORTS_14_GAPS_AND_18_CHILD_IDS',word_sha256=hashlib.sha256(W.read_bytes()).hexdigest(),geometry_source_sha256=hashlib.sha256(SRC.read_bytes()).hexdigest(),links=links,AI='OpenAI Codex assistance; PR373 dyadic geometry by DaysSky/Claude; E8 Jacob Sussman. Apache-2.0.')
(P/'IDLE-GAP-LINKS.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print(len(links),'bound ids')
