from pathlib import Path
import sys,gzip,json,shutil
code,retired,sliced,out=map(Path,sys.argv[1:]);assert not out.exists()
sys.path.insert(0,str(code));import gk_word as g
w=json.loads(gzip.decompress((sliced/'WORD.json.gz').read_bytes()));p=g.profile(w)
assert dict(p)=={int(r):n for r,n in w['report']['local_profile'].items()}
out.mkdir();(out/'FULL-WORD.json.gz').write_bytes(g.dump(w))
for src,name in [(retired/'SELECTION.json','SELECTION.json'),(retired/'RETIREMENT.json','RETIREMENT.json'),(sliced/'SLICE-RECEIPT.json','SLICE-RECEIPT.json')]:shutil.copyfile(src,out/name)
print('PASS_SLICED_PROFILE_AND_SOURCE_INSTALL',dict(p))
