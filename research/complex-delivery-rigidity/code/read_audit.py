"""Target reads in the raw word: every target gate frame is inside the target's cap; which registers are read by more than one target,
and whether those targets ever share a block. Usage: read_audit.py FULL-WORD.json.gz ROLES.json blocks.json OUT.json"""
import sys,gzip,json,collections
from common import basis,inside,hyper
W=json.loads(gzip.decompress(open(sys.argv[1],'rb').read()));ROL=json.load(open(sys.argv[2]));BL=json.load(open(sys.argv[3]))
v=112;P=W['ports'];regs=lambda e:[e[1]]+([e[2]]if e[0]=='add'else[])
cap={t:hyper(P[t]) for t in range(v)}
tet={};blk={}
for c,b in BL.items():
    for x,tv in b['T'].items():tet[int(x)-8]=tv['tetrad'];blk[int(x)-8]=c
readers=collections.defaultdict(list);viol=0
for i,e in enumerate(W['B']):
    f=tuple(basis(e[-1]))
    if e[0]=='add' and v<=e[1]<2*v:
        t=e[1]-v
        if not inside(f,cap[t]):viol+=1
        if e[2]<v or e[2]>=2*v:readers[e[2]].append(t)
multi={r:ts for r,ts in readers.items() if len(ts)>1}
kinds=collections.Counter()
for r,ts in multi.items():
    kinds[(len(ts),'same-block' if len({blk[t] for t in ts})==1 else 'cross-block')]+=1
out=dict(cap_violations=viol,registers_read_by_more_than_one_target=len(multi),kinds=[[list(k),c] for k,c in sorted(kinds.items())])
print(json.dumps(out,indent=1));json.dump(out,open(sys.argv[4],'w'),indent=1)
