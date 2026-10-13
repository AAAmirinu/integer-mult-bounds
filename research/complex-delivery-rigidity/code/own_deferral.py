"""Can a target's own-row read be moved later in B? Checks on the raw word: (a) own registers are never written after their last target read; (b) the frame they reach after the module's later reads leaves the target's cap (so the read cannot be
deferred). Usage: own_deferral.py FULL-WORD.json.gz ROLES.json OUT.json"""
import sys,gzip,json,collections
from common import basis,inside,hyper
W=json.loads(gzip.decompress(open(sys.argv[1],'rb').read()));ROL=json.load(open(sys.argv[2]));v=112;P=W['ports']
mp={int(k):x for k,x in ROL['regmap'].items()}
own={int(t)-8:(mp[r],tuple(F)) for t,(r,c,F) in ROL['own_rows'].items()}
regs=lambda e:[e[1]]+([e[2]]if e[0]=='add'else[])
B=W['B'];ownregs={r for r,_ in own.values()}
reads=collections.defaultdict(list)
for i,e in enumerate(B):
    if e[0]=='add' and v<=e[1]<2*v and e[2] in ownregs:reads[e[2]].append(i)
written_after=read_after=0
for r,idx in reads.items():
    for i,e in enumerate(B):
        if i>max(idx) and not(v<=e[1]<2*v):
            if e[1]==r:written_after+=1
            elif e[0]=='add' and e[2]==r:read_after+=1
cur={}
for e in B:
    if v<=e[1]<2*v:continue
    for r in regs(e):cur[r]=tuple(basis(e[-1]))
res=collections.Counter()
for t,(r,F) in own.items():
    f=cur.get(r,tuple(basis(F)));res[(inside(f,hyper(P[t])),len(f))]+=1
out=dict(own_registers=len(ownregs),own_registers_that_are_sources=sum(1 for r in ownregs if r<v),writes_to_own_registers_after_their_last_target_read=written_after,module_reads_of_own_registers_after_their_last_target_read=read_after,end_of_module_frame_inside_own_cap=[[list(k),c] for k,c in sorted(res.items())])
print(json.dumps(out,indent=1));json.dump(out,open(sys.argv[3],'w'),indent=1)
