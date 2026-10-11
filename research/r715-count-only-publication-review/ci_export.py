import pathlib,json,hashlib,ast,subprocess
R=pathlib.Path(__file__).parent;S=R.parent/'R404-corrected-publication';P=S/'publish';C=P/'.github/workflows/sharp-r715-fallback.yml'
def need(b,m):
 if not b:raise ValueError(m)
text=C.read_text()
for token in ["ref: ${{ github.event.pull_request.head.sha || github.sha }}","persist-credentials: false","timeout-minutes: 35","python: ['3.11', '3.14']","package: ['r715-sharp-fallback', 'r715-sharp-response28']","python -OO -B","test_complex_content.py","test_process_bound.py","git diff --exit-code","python -m pip freeze","OPENBLAS_NUM_THREADS: '1'","OMP_NUM_THREADS: '1'","MKL_NUM_THREADS: '1'"]:
 need(token in text,'CI contract '+token)
refs=['actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1','actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97','actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02']
need(all(x in text for x in refs),'pinned actions')
source=(S/'export.py').read_text();ast.parse(source);need("p.read_bytes().decode('utf-8')" in source,'byte-preserving export')
inventory=json.loads(subprocess.check_output(['python',str(S/'export.py'),'--list'],timeout=20))
for entry in inventory:
 raw=(P/entry['path']).read_bytes();need(entry['sha256']==hashlib.sha256(raw).hexdigest(),'export inventory raw hash');need(entry['git_blob_sha1']==hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),'export Git blob hash')
result={'status':'PASS_CI_AND_RAW_EXPORT_INSPECTION','ci_sha256':hashlib.sha256(C.read_bytes()).hexdigest(),'exporter_sha256':hashlib.sha256((S/'export.py').read_bytes()).hexdigest(),'export_files':len(inventory),'export_inventory':inventory,'actual_ci_run_claim':False,'dependency_note':'Inherited upstream requirements retained, resolution logged via pip freeze; no dependency reproducibility theorem or current GitHub CI execution claim.'}
(R/'CI-EXPORT-001.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS_CI_AND_RAW_EXPORT_INSPECTION',len(inventory))
