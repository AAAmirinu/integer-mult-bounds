"""Fresh, complete response-space admission, derived from pinned PR401.

Every old and new Gaussian child pair is recomputed. The original source
stays immutable and the literal adaptation is recorded. Apache-2.0;
prepared with substantial OpenAI Codex assistance.
"""
import difflib,hashlib,importlib.util,json,os,pathlib,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent
SOURCE=ROOT/'vendor/source401'
def read(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def dump(p,z):pathlib.Path(p).write_text(json.dumps(z,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')

def main(candidate,patterns,helper_base,signed_base,out):
    assert not out.exists();out.mkdir();work=out/'derived';work.mkdir()
    old=(SOURCE/'local/local_admit.py').read_text(encoding='utf-8');new=old
    before='assert v==120 and R==781 and h==9';assert new.count(before)==1
    new=new.replace(before,'assert v==120 and R==779 and h==9')
    before="inputs=[CP,BASE,SIGNED,REUSE,PHASE,Path(__file__),PRIOR/'CLIFFORD-REVIEW.json',PRIOR/'CLIFFORD-RECIPES.json']+list(ROOT.glob('*.py'))"
    assert new.count(before)==1
    new=new.replace(before,"inputs=[CP,BASE,SIGNED,PHASE,Path(__file__)]+list(ROOT.glob('*.py'))")
    lo=new.index('# Exact algebraic omission controls for every unit entrance gate.')
    hi=new.index('# Fully execute a changed scalar schedule',lo)
    new=new[:lo]+'''# Chronological omission controls, including ordered donor promotions.
# Each source is read before any earlier entrance write to that register.
# Hence deleting a shear leaks exactly its suffix response times its original
# independent source column. Replay the suffix, rather than assuming S-I squares
# to zero or that all entrance donors and pivots are globally disjoint.
original,_=raw_operator(old);head=c['A'][:headlen];written=set();sources=set()
for g in head:
 for t,s,q in flat([g]):
  assert s not in written and t!=s
  written.add(t);sources.add(s)
assert sources==set(ext)
response=[dict(original[v+i]) for i in range(v)];controls=[]
for gi in reversed(range(headlen)):
 for t,s,q in flat([head[gi]]):
  leak=[-q*row.get(t,Q(0)) for row in response]
  assert any(leak),'zero-response donor omission is not a valid control'
  controls.append(dict(group=gi,target=t,gauged_source=s,nonzero_Y_coordinates=sum(bool(a) for a in leak),one_nonzero_coefficient=str(next(a for a in leak if a))))
  for row in response:
   a=row.get(s,Q(0))+q*row.get(t,Q(0))
   if a:row[s]=a
   else:row.pop(s,None)
assert all(not row.get(s,Q(0)) for row in response for s in ext)
controls.sort(key=lambda z:z['group'])
''' +new[hi:]
    lo=new.index("priorreview=read(PRIOR/'CLIFFORD-REVIEW.json')");hi=new.index('newpairs=set()',lo)
    new=new[:lo]+'# Recompute every Gaussian pair; no cached phase admission.\noldpairs=set()\n'+new[hi:]
    local=work/'local_admit.py';local.write_text(new,encoding='utf-8',newline='\n')
    dump(out/'DERIVATION.json',dict(source='vendor/source401/local/local_admit.py',old_sha256=sha(SOURCE/'local/local_admit.py'),new_sha256=sha(local),difference=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True)))))
    env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None);checks=[]
    def run(name,cmd):
        print('RUN response-space '+name,flush=True);started=time.monotonic()
        with(out/(name+'.log')).open('w',encoding='utf-8',newline='\n')as f:
            subprocess.run(list(map(str,cmd)),env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
        checks.append(dict(name=name,seconds=time.monotonic()-started))
        print('PASS response-space '+name,flush=True)
    def py(name,script,*args):run(name,[sys.executable,'-B',script,*args])
    py('local',local,candidate,out/'local','--helper-baseline',helper_base,'--signed-baseline',signed_base,'--deps',SOURCE/'local/deps')
    lr=read(out/'local/RESULT.json')
    assert lr['reused_pinned_old_phase_pairs']==0 and lr['new_and_reflected_exact_phase_pairs']>0
    assert lr['unit_entrance_gates']==551
    assert len(lr['entrance_omission_algebraic_controls'])==551
    exe=out/('phase-replay.exe'if os.name=='nt'else'phase-replay')
    run('compile-phase',[env.get('CXX','g++'),'-O2','-std=c++17','-I'+str(SOURCE/'architecture/deps'),SOURCE/'architecture/phase-replay.cpp','-o',exe])
    py('phase',SOURCE/'architecture/phase.py',candidate,SOURCE/'local/deps',exe,out/'phase',SOURCE/'architecture/phase-replay.cpp')
    prior=SOURCE/'architecture/inputs/GLOBAL-TEMPLATE.json.gz'
    py('banks',SOURCE/'architecture/banks.py',candidate,patterns,out/'phase/RESIDUALS.json',out/'local/LOCAL-PROGRAMS.json.gz',out/'local/RESULT.json',prior,SOURCE/'local/deps',out/'banks',SOURCE/'architecture/inputs/DATA-PHASES.json')
    py('bank-audit',SOURCE/'architecture/audit.py',out/'banks',candidate,out/'phase/RESIDUALS.json',out/'local/LOCAL-PROGRAMS.json.gz',prior)
    py('bridge',SOURCE/'architecture/bridge.py',out/'banks')
    spec=importlib.util.spec_from_file_location('response_space_moments',SOURCE/'code/outer.py')
    M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
    ad=read(out/'banks/ADMISSION.json');ind=read(out/'banks/INDEPENDENT-ADMISSION.json')
    assert ad['template_sha256']==ind['template_sha256'] and ad['deficit']==2496
    price=M.coarse(ad['profile'],ad['m'],ad['live']);dump(out/'COARSE.json',price)
    result=dict(status='PASS_FRESH_SHARED_RESPONSE_SPACES_FULL_SUPPLIER',coarse=price['lower'],R=779,local_columns=1019,frames=lr['checks']['frames']if 'frames'in lr['checks']else len(read(candidate)['frames']),live=ad['live'],physical=ad['physical'],profile=ad['profile'],finite_invoice=ad['invoice'],gauges=lr['gauges'],entrance_rankmass=lr['entrance_rankmass'],banks_per_stage=ad['banks_per_stage'],all_fresh_phase_pairs=lr['new_and_reflected_exact_phase_pairs'],explicit_bank_boundary_adapters=ad['invoice']['explicit_bank_boundary_adapters'],checks=[e['name']for e in checks],scope='Conditional finite supplier; full all-size compiler, arbitrary-correlated dirt/bank, recursion, cover/routing and analytic interfaces remain assumptions.')
    dump(out/'VERIFICATION.json',result)
    print(result['status'],result['coarse'],flush=True)
    return result
