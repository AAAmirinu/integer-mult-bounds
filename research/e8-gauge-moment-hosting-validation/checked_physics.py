"""Additional before-operation int64 bounds on the unchanged PR484 E2E replay."""
import hashlib,json,os,runpy,sys
from pathlib import Path
code,base,out=map(lambda x:Path(x).resolve(),sys.argv[1:4]);out.mkdir(parents=True,exist_ok=False);sys.path.insert(0,str(code));os.environ['LG_BASE']=str(base);os.chdir(out)
from gd import GD
stats={'add_scaled':0,'scale':0,'C':0,'largest_intermediate_bound':0}
def magnitude(v):
 v.guard()
 return max(int(abs(v.re).max()),int(abs(v.im).max())) if v.re.size else 0
def check(kind,n):
 assert n < 1<<63,('possible int64 overflow before operation',kind,n)
 stats[kind]+=1;stats['largest_intermediate_bound']=max(stats['largest_intermediate_bound'],n)
oldadd,oldscale,oldprim=GD.add_scaled,GD.scale,GD.apply_prim
def add(self,src,num,den):
 assert den>0 and den&(den-1)==0
 e=den.bit_length()-1;D=max(self.d,src.d+e)
 check('add_scaled',(magnitude(self)<<(D-self.d))+abs(num)*(magnitude(src)<<(D-src.d-e)))
 return oldadd(self,src,num,den)
def scale(self,num,den):
 check('scale',magnitude(self)*abs(num));return oldscale(self,num,den)
def prim(self,p,inverse=False):
 if p[0]=='C':check('C',4*magnitude(self))
 return oldprim(self,p,inverse)
GD.add_scaled,GD.scale,GD.apply_prim=add,scale,prim
sys.argv=[str(code/'lg_e2e.py'),'gauge80-kernel42'];runpy.run_path(sys.argv[0],run_name='__main__')
e=json.load(open('E2E-gauge80-kernel42.json'));assert e['status']=='PASS' and not e['failures']
record=dict(status='PASS_PREOP_INT64_GUARDED_PHYSICAL_REPLAY',variant='gauge80-kernel42',basis_columns=e['columns'],dense_columns=e['dense'],orientations=2,statistics=stats,largest_intermediate_bound_bits=stats['largest_intermediate_bound'].bit_length(),source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [code/'gd.py',code/'lg_e2e.py',code/'lg_phys.py']},input_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (base/'gauge80-kernel42/split-centres').iterdir() if p.name in ['CANONICAL-WORD.json.gz','LOCAL-PROGRAMS.json.gz','CLIFFORD-RECIPES.json','RESIDUAL-ADAPTERS.json']},scope='Every executed addition, multiplication, left shift and C gate is bounded before int64 arithmetic; the original after-operation guards remain active. This is the published E2E sample, not every full-program basis column.')
(out/'PREOP-BOUNDS.json').write_text(json.dumps(record,indent=2)+'\n');print(record['status'],record['largest_intermediate_bound_bits'],flush=True)
