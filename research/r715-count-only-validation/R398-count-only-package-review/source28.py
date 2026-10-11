"""Independent source closure and proposal scope inspection; no producer imports."""
import pathlib,json,hashlib,shutil,sys,ast
R=pathlib.Path(__file__).parent
REPO=pathlib.Path('F:/integer-mult-frontier/work/R383-response-transfer/source')
TREE=pathlib.Path('F:/integer-mult-frontier/work/R372-integration/pr473-f43-tree-001.json')
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inv(p):return {f.relative_to(p).as_posix():sha(f)for f in p.rglob('*')if f.is_file()and'__pycache__'not in f.parts}
package=pathlib.Path(sys.argv[1]);revision=sys.argv[2]if len(sys.argv)>2 else '001';out=R/('snapshot-'+revision);need(not out.exists(),'snapshot exists');shutil.copytree(package,out)
actual=inv(out);actual.pop('MANIFEST.json');manifest=json.loads((out/'MANIFEST.json').read_bytes());need(actual==manifest,'own manifest')
pin=json.loads((out/'SOURCE.json').read_bytes());closure=json.loads((out/'pins/CLOSURE.json').read_bytes())
need(pin['reference_head']==closure['reference_head']=='f43a0e9ad04a7b3683498274854ae2e35d4a8d7c','latest source head')
need(sha(out/'pins/CLOSURE.json')==pin['closure_sha256'],'closure hash')
tree=json.loads(TREE.read_bytes());need(not tree.get('truncated'),'truncated tree');entries={v['path']:v for v in tree['tree']}
for p,h in closure['files'].items():
 raw=(REPO/p).read_bytes();need(hashlib.sha256(raw).hexdigest()==h,'source sha256 '+p)
 blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();need(entries[p]['sha']==blob,'source Git tree '+p)
for p,expected in closure['package_inventories'].items():need(sorted(inv(REPO/p))==expected,'inventory '+p)
source=(REPO/(pin['parent_package']+'/code/assemble.py')).read_text();proposal=(out/'code/assemble.py').read_text()
marker='# ---------------- complex:'
sa=source.index(marker);pa=proposal.index(marker);need(source[sa:]==proposal[pa:],'complex/outer assembler scope changed')
old=source.index('root = M.certify(P, m, W, True)');new=proposal.index('from sharp_bit_moment import')
need(source[:old]==proposal[:new],'finite bit invoice scope changed')
for name in ['verify.py','code/protocol.py','code/assemble.py','code/sharp_bit_moment.py']:ast.parse((out/name).read_bytes())
workflow=pathlib.Path('F:/integer-mult-frontier/work/R372-integration/publish/.github/workflows/sharp-r715-fallback.yml')
result=dict(status='PASS_FINAL_SOURCE_CLOSURE_AND_PROPOSAL_SCOPE',package_manifest_sha256=sha(out/'MANIFEST.json'),package_source_sha256=sha(out/'SOURCE.json'),files=inv(out),closure_files=len(closure['files']),closure_packages=len(closure['package_inventories']),source_tree_sha256=sha(TREE),source_closure_sha256=sha(out/'pins/CLOSURE.json'),workflow_sha256=sha(workflow),checker_sha256=sha(pathlib.Path(__file__)),scope='Raw Git tree/byte closure, additive package manifest and exact unchanged invoice/complex/outer source; no supplier execution.')
(R/('SOURCE-REVIEW-'+revision+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result['closure_files'])
