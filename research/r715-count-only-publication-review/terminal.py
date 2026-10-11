import pathlib,subprocess,json,hashlib
R=pathlib.Path(__file__).parent;W=R.parent;A=W/'R406-docs-revision-actual'
def need(b,m):
 if not b:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
records={}
for kind in ['84','28']:
 base=A/kind
 for mode in ['normal','optimized']:
  name='integer-mult-r406-docs'+kind+'-'+mode
  obj=json.loads(subprocess.check_output(['docker','inspect',name],timeout=20))[0]
  st=obj['State'];hc=obj['HostConfig'];need(st['Status']=='exited' and st['ExitCode']==0 and not st['OOMKilled'],'terminal container')
  need(hc['NanoCpus']==10**9 and hc['Memory']==2*1024**3 and hc['MemorySwap']==2*1024**3 and hc['NetworkMode']=='none' and hc['ReadonlyRootfs'],'resource isolation')
  mounts={m['Destination']:m for m in obj['Mounts']};need(all(not mounts[k]['RW'] for k in ['/source','/proposal','/parent','/runner.py']),'scientific input readonly')
  out=base/'data'/(mode+'-001');launcher=read(base/'data'/('launcher-'+mode+'-001.json'));receipt=read(out/'RECEIPT.json');outer=read(base/(mode+'-outer-001.json'))
  need(launcher['exit_code']==0 and not launcher['timeout'] and launcher['package_manifest_sha256']==receipt['package_manifest_sha256'],'launcher binding')
  need(outer['exit_code']==0 and outer['package_manifest_sha256']==receipt['package_manifest_sha256'] and outer['log_sha256']==sha(base/(mode+'-001.log')),'outer binding')
  need(('-OO' in launcher['command'])==(mode=='optimized'),'mode actual')
  records[kind+'/'+mode]={'container':name,'exit_code':st['ExitCode'],'oom':st['OOMKilled'],'manifest_sha256':receipt['package_manifest_sha256'],'receipt_sha256':sha(out/'RECEIPT.json'),'result_sha256':sha(out/'RESULT.json'),'actual_seconds':launcher['actual_seconds'],'launcher_sha256':sha(base/'data'/('launcher-'+mode+'-001.json')),'outer_sha256':sha(base/(mode+'-outer-001.json'))}
 new=(base/'data/normal-001/RESULT.json').read_bytes();need(new==(base/'data/optimized-001/RESULT.json').read_bytes(),'normal OO bytes')
 old=W/('R397-count84-actual' if kind=='84' else 'R392-response28-actual')/'data/normal-001/RESULT.json';need(new==old.read_bytes(),'doc-only identical mathematics')
(R/'REVISION002-TERMINALS-001.json').write_text(json.dumps({'status':'PASS_ACTUAL_REVISION002_TERMINAL_BINDINGS','containers':records,'normal_optimized_and_prior001_result_bytes_identical_each':True,'checker_sha256':sha(pathlib.Path(__file__))},indent=2)+'\n');print('PASS_ACTUAL_REVISION002_TERMINAL_BINDINGS')
