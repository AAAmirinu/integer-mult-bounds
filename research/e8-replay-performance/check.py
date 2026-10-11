"""Offline acquisition, exact-code pins and all focused adapter controls."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
from fetch import verify,SOURCE
from replay import integrity
ROOT=Path(__file__).resolve().parent

def main():
    if not __debug__:raise RuntimeError('assertions required')
    integrity();verify(SOURCE)
    original=json.loads((ROOT/'ORIGINAL-CODE.json').read_text())
    for p,digest in original.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==digest,p
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONHASHSEED='0')
    env.pop('PYTHONOPTIMIZE',None)
    files=['producer-prefix-sharing/test_sharing.py','predecessor-performance/test_adapter.py',
           'source-admission-performance/test_admission.py','source-admission-performance/test_generator.py',
           'scalar-admission-performance/test_scalar.py','test_package.py']
    for p in files:subprocess.run([sys.executable,'-B',str(ROOT/p),'-v'],check=True,env=env)
    integrity();verify(SOURCE);print('PASS all packaged offline controls')

if __name__=='__main__':main()
