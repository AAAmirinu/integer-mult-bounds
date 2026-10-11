"""Bounded exact complex-supplier observability and nested-flag screen.
Source-byte pinned, no formal proof or achieved kappa change is claimed.
"""
import gzip,json,collections,hashlib,sys
from fractions import Fraction as Q
from pathlib import Path
src=Path(sys.argv[1]);out=Path(sys.argv[2]);w=json.loads(gzip.decompress(src.read_bytes()));v=len(w['ports']);n=2*v+w['report']['R'];a=w['A'];pivs=set(map(int,w['start_extra']))
def span(a):
 s={0}
 for x in a:s|={v^x for v in list(s)}
 return frozenset(s)
def basis(s):
 b={}
 for x in sorted(s):
  for j,y in sorted(b.items(),reverse=True):
   if x>>j&1:x^=y
  if x:b[x.bit_length()-1]=x
 return list(b.values())
k=0
while k<len(a)and a[k][0]=='add'and a[k][2]in pivs and a[k][1]not in pivs:k+=1
first={}
for e in a[k:]:
 for r in [e[1]]+([e[2]]if e[0]=='add'else[]):first.setdefault(r,e[-1])
flags=[]
for p in sorted(pivs):
 donors=[e[1]for e in a[:k]if e[2]==p];common=span(first[p])
 for d in donors:common&=span(first[d])
 old=span(w['start_extra'][str(p)])
 if len(common)>len(old):flags.append(dict(pivot=p,old=sorted(old),common=basis(common),donors=donors))
r=[{}for i in range(n)]
for i in range(v):r[v+i][i]=Q(1)
def rev(e):
 t=e[1]
 if e[0]=='scale':r[t]={i:q*Q(e[2],e[3])for i,q in r[t].items()}
 else:
  s=e[2];q=Q(e[3],e[4])
  for i,c in list(r[t].items()):
   z=r[s].get(i,0)+c*q
   if z:r[s][i]=z
   else:r[s].pop(i,None)
for e in reversed(w['B']):rev(e)
for e in reversed(w['cut']):rev(e)
last={};epoch={}
for i,e in enumerate(a):
 if e[0]=='add':epoch[i]=last.get(e[2],-1)
 last[e[1]]=i
seen={};pairs=[];zeros=[]
for i in range(len(a)-1,-1,-1):
 e=a[i]
 if not r[e[1]]:zeros.append(i)
 if e[0]=='add':
  col=tuple(sorted((j,q*Q(e[3],e[4]))for j,q in r[e[1]].items()));neg=tuple((j,-q)for j,q in col);key=(e[2],epoch[i],col);op=(e[2],epoch[i],neg)
  for z in seen.get(op,[]):pairs.append((i,z))
  seen.setdefault(key,[]).append(i)
 rev(e)
full=span([1<<i for i in range(9)]);perp=lambda q:frozenset(x for x in range(512)if (x&q).bit_count()%2==0);dim=lambda s:len(s).bit_length()-1
S=[span([q])for q in w['ports']]+[span([])]*(n-v)
for rr,fs in w['start_extra'].items():S[int(rr)]=span(fs)
F=[full]*v+[perp(q)for q in w['ports']]+[full]*(n-2*v);frames={tuple(e[-1]):span(e[-1])for e in a+w['B']}
def profile(skip):
 cur=S.copy();p=collections.Counter()
 def climb(rr,f):
  old=cur[rr];assert old<=f
  if old!=f:p[dim(f)-dim(old)]+=1;cur[rr]=f
 for part in ['A','B']:
  if part=='B':
   for rr,cf in zip(w['centers'],w['center_frames']):
    assert cur[rr]==span(cf)
    served={span(w.get('target_levels',{}).get(str(e[1]-v),[]))for e in w['cut']if e[2]==rr};o=span(cf)
    for L in sorted(served,key=lambda x:-len(x)):
     assert L<=o
     if L!=o:p[dim(o)-dim(L)]+=1;o=L
  for i,e in enumerate(w[part]):
   if part=='A'and i in skip:continue
   for rr in [e[1]]+([e[2]]if e[0]=='add'else[]):climb(rr,frames[tuple(e[-1])])
 for rr,f in enumerate(F):climb(rr,f)
 return p
base=profile(set());reports=[]
for pair in pairs:
 pp=profile(set(pair));reports.append(dict(gates=pair,delta={z:pp[z]-base[z]for z in set(base)|set(pp)if pp[z]!=base[z]}))
allpair=profile(set(x for pair in pairs for x in pair))
res=dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),prefix_kernel_gates=k,entrance_pivots=len(pivs),flag_candidates=flags,individually_unobservable_gates=zeros,pair_candidates=reports,base_profile=base,all_pairs_profile=allpair,scope='Exact bounded finite screens only. Individual same-source same-write-epoch opposite-response pairs preserve the target map; joint scalar compatibility has not been certified. Frame profiles alone are not full physical certificates. No candidate screened here improves the paid moment.')
out.write_text(json.dumps(res,sort_keys=True,indent=2)+'\n');print(json.dumps(res,sort_keys=True))
