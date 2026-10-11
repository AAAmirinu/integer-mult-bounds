"""Independent finite Git publication fixture; no scientific supplier execution."""
import pathlib,subprocess,hashlib,json,sys
R=pathlib.Path(__file__).parent;B=pathlib.Path('F:/integer-mult-frontier/work/R395-count-only-correction/response28/revision-001')
PKG=B/'research/r715-sharp-response28';PATCH=B/'contribution.patch'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def git(repo,*args):return subprocess.check_output(['git','-C',str(repo),*args],stderr=subprocess.STDOUT,timeout=30)
repo=R/'git-apply-fixture-28-second-001';need(not repo.exists(),'fixture exists');repo.mkdir()
git(repo,'init');git(repo,'config','core.autocrlf','true')
git(repo,'-c','core.autocrlf=false','apply','--whitespace=nowarn',str(PATCH))
git(repo,'add','research/r715-sharp-response28')
files={}
for p in sorted(PKG.rglob('*')):
 if not p.is_file()or'__pycache__'in p.parts:continue
 name='research/r715-sharp-response28/'+p.relative_to(PKG).as_posix();expected=p.read_bytes()
 need((repo/name).read_bytes()==expected,'applied working bytes '+name)
 blob=git(repo,'show',':'+name);need(blob==expected,'Git index bytes '+name)
 files[name]=hashlib.sha256(blob).hexdigest()
manifest=json.loads((PKG/'MANIFEST.json').read_bytes());need({k.split('research/r715-sharp-response28/')[1]:v for k,v in files.items()if not k.endswith('/MANIFEST.json')}==manifest,'complete applied manifest')
# Intentionally normalize the patch through universal-newline text I/O. The
# resulting Git application must no longer reproduce every exact package byte.
badpatch=R/'NORMALIZED-PATCH-CONTROL-28-001.patch';badpatch.write_bytes(PATCH.read_text().encode())
need(badpatch.read_bytes()!=PATCH.read_bytes(),'nonvacuous newline control')
badrepo=R/'git-normalized-control-28-001';badrepo.mkdir();git(badrepo,'init')
git(badrepo,'-c','core.autocrlf=false','apply','--whitespace=nowarn',str(badpatch))
changed=[p.relative_to(PKG).as_posix()for p in PKG.rglob('*')if p.is_file()and'__pycache__'not in p.parts and(badrepo/'research/r715-sharp-response28'/p.relative_to(PKG)).read_bytes()!=p.read_bytes()]
need(bool(changed),'normalized patch accepted byte-equivalent')
out=dict(status='PASS_GIT_PATCH_BYTES_FIXTURE_ONLY',scientific_replay=False,patch_sha256=hashlib.sha256(PATCH.read_bytes()).hexdigest(),manifest_sha256=hashlib.sha256((PKG/'MANIFEST.json').read_bytes()).hexdigest(),git_index_and_working_files=files,normalized_patch_control_rejected=True,normalized_patch_changed_files=changed,checker_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),python=sys.version)
(R/'PATCH-BYTES-REVIEW-28-001.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],len(files),len(changed))
