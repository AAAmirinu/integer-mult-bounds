"""Independent source audit. DLamdata with OpenAI Codex assistance; Apache-2.0."""
import importlib.util, pathlib, collections, itertools, math, json
ROOT=pathlib.Path(__file__).resolve().parents[2]
def need(ok, message):
 if not ok: raise ValueError(message)
def load(relative,name):
 s=importlib.util.spec_from_file_location(name,ROOT/relative);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
old=load('research/direct-flow-leaf-walk/diagnostics/overlap_flow.py','audit_flow')
walk=load('research/direct-flow-leaf-walk/verify.py','audit_walk')
native=load('research/direct-mixed-flow/flow.py','native_flow')
receipt=json.loads((ROOT/'research/direct-mixed-flow/vendor/p7-RESULT.json').read_text())['strictification']
need({int(k):v for k,v in receipt['paid'].items()}==walk.P, 'paid source inventory')
need({int(k):v for k,v in receipt['targets'].items()}==walk.W, 'target source inventory')
rows=[]
for N in [121,604,605,606,3024,3025,3026,15124,15125,15126]:
 f=old.flow(N,walk.W,walk.P); G=f['G']
 exact=collections.Counter()
 for ranks in itertools.product(walk.P,repeat=G):
  rho=math.prod(ranks)
  if 121*rho>N:continue
  multiplicity=math.prod(walk.P[r] for r in ranks)
  for r,pr in walk.P.items():exact[r*rho]+=multiplicity*pr
 leaf=collections.Counter(f['X']);leaf.subtract(f['BX']);leaf=+leaf
 need(exact==leaf,(N,'leaf histogram'))
 actual=native.Flow(walk.W,walk.P,N).merged()
 other=actual['exits'].copy();other.subtract(actual['boundary_exits']);other=+other
 need(other==exact,(N,'original Flow class'))
 # Incorrectly truncating the last unconditioned rank must change the leaf law.
 wrong=collections.Counter({r:c for r,c in exact.items() if 121*r<=N})
 need(wrong!=exact,(N,'terminal truncation failure control'))
 rows.append({'N':N,'G':G,'leaf_ranks':len(exact),'terminal_truncation_rejected':True})
print(json.dumps({'status':'PASS_INDEPENDENT_SOURCE_LEAF_IDENTIFICATION','fixtures':rows},indent=2))
