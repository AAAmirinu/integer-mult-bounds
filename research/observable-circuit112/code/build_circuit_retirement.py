"""Exact component retirement with a independently derived paid histogram.
Usage: CODE OLD_RANKSECTOR_DIRECTORY NEW_SELECTION NEW_OUTPUT_DIRECTORY.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import sys,json,gzip,hashlib
if not __debug__:raise RuntimeError('Assertions must remain enabled')
code,src,selp,out=map(Path,sys.argv[1:]);assert not out.exists()
sys.path.insert(0,str(code));import gk_word as g
read=lambda p:json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
base=read(src/'RETIMED-BASE.json.gz');old=read(src/'FULL-WORD.json.gz');before=read(src/'SELECTION.json');after=read(selp)
assert before['gauge']==after['gauge']
cols=g.responses(base);first=g.first_frames(base)
prior={tuple(c['E']):c for c in before['kernel']};post={tuple(c['E']):c for c in after['kernel']};assert len(prior)==len(before['kernel'])and len(post)==len(after['kernel'])and post.keys()<=prior.keys()
delta=Counter();retired=[]
def add(r,z):
 if r:delta[r]+=z
for E,a in prior.items():
 b=post.get(E,dict(donors=[],pivots=[]));D,P=set(a['donors']),set(a['pivots']);d,p=set(b['donors']),set(b['pivots'])
 assert d<=D and p<=P
 rd,rp=D-d,P-p;e=len(g.basis(E));used=set()
 for h in P:
  rel=g.solve_relation(cols,a['donors'],h);assert rel is not None;used.update(rel)
  if h in p:assert not rd&set(rel),('cross-component dependence',h)
 assert used==D
 used2=set()
 for h in p:
  rel=g.solve_relation(cols,b['donors'],h);assert rel is not None;used2.update(rel)
 assert used2==d
 if not rd and not rp:continue
 for h in rd|rp:
  f=len(first[h]);assert g.span(E)<=g.span(first[h]);add(f,1);add(f-e,-1)
 add(e,-len(rd));retired.append(dict(E=list(E),donors=sorted(rd),pivots=sorted(rp)))
w=g.build(base,after);op,np=g.profile(old),g.profile(w)
assert all(np[r]-op[r]==delta[r]for r in set(op)|set(np)|set(delta))
ow,nw=g.widths_of(old),g.widths_of(w)
assert sum(nw)-sum(ow)==sum(r*z for r,z in delta.items())
assert len(nw)==560 and sum(len(c['pivots'])for c in after['kernel'])==92
for part in ['A','B','cut','cleanup','precondition']:
 for ev in w[part]:
  q=Q(ev[3],ev[4])if ev[0]=='add'else Q(ev[2],ev[3]);assert not q.denominator&(q.denominator-1)
  if ev[0]=='scale':assert abs(q.numerator)>0 and not abs(q.numerator)&(abs(q.numerator)-1)
out.mkdir();(out/'FULL-WORD.json.gz').write_bytes(g.dump(w));(out/'SELECTION.json').write_text(json.dumps(after,indent=2)+'\n')
r=dict(status='PASS_EXACT_CIRCUIT_RETIREMENT_AND_PAID_HISTOGRAM',components=retired,local_delta=dict(sorted((r,z)for r,z in delta.items()if z)),new_profile=dict(np),old_widths=ow,new_widths=nw,rank_mass_added=sum(r*z for r,z in delta.items()),pivots=92,source_sha256=hashlib.sha256((src/'FULL-WORD.json.gz').read_bytes()).hexdigest(),selection_sha256=hashlib.sha256(selp.read_bytes()).hexdigest(),scope='Exact relations, direct component support, frame accounting and dyadic construction. Full scalar, phases, physical owners and assembly are checked separately.')
(out/'RETIREMENT.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],r['local_delta'])
