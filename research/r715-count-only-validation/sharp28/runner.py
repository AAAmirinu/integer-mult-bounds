"""Bound actual sharper assembly to a completed, immutable full parent replay."""
import argparse,datetime,hashlib,json,os,pathlib,signal,subprocess,sys,time
ap=argparse.ArgumentParser();ap.add_argument('--optimized',action='store_true');a=ap.parse_args()
DATA=pathlib.Path('/out');mode='optimized-001' if a.optimized else 'normal-001'
command=[sys.executable]+(['-OO'] if a.optimized else [])+['-B','/proposal/verify.py',str(DATA/mode),'--research-root','/source/research','--parent-output','/parent']
environment=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONINTMAXSTRDIGITS='0',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1');environment.pop('PYTHONOPTIMIZE',None)
started=time.monotonic();process=subprocess.Popen(command,env=environment,start_new_session=True);timeout=False
try:code=process.wait(timeout=300)
except subprocess.TimeoutExpired:
 timeout=True;os.killpg(process.pid,signal.SIGKILL);code=process.wait()
receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'TERMINAL_SHARP_ASSEMBLY_TIMEOUT' if timeout else 'TERMINAL_SHARP_ASSEMBLY_PASS' if code==0 else 'TERMINAL_SHARP_ASSEMBLY_FAILURE','head':'f43a0e9ad04a7b3683498274854ae2e35d4a8d7c','command':command,'python':sys.version,'exit_code':code,'timeout':timeout,'actual_seconds':time.monotonic()-started,'timeout_seconds':300,'controller_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'package_manifest_sha256':hashlib.sha256(pathlib.Path('/proposal/MANIFEST.json').read_bytes()).hexdigest(),'parent_receipt_sha256':hashlib.sha256(pathlib.Path('/parent/RECEIPT.json').read_bytes()).hexdigest(),'scope':'Actual completed full original response28 replay reused explicitly; fresh sharper bit moment and complete assembly, original physical program/invoices and all-size assumptions retained.'}
with (DATA/('launcher-'+mode+'.json')).open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(receipt),flush=True);sys.exit(124 if timeout else code)
