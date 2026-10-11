"""Acquire only the 839 exact PR358 blobs, or copy a local pinned package.

Network access happens only in this explicit acquisition command. Replay and
tests are offline. No complete repository checkout or historical output needed.
Prepared with OpenAI Codex assistance; Apache-2.0.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import shutil
import time
import urllib.request

ROOT=Path(__file__).resolve().parent
PROFILE=ROOT/'e8-pipeline-profile'
SOURCE=PROFILE/'pr358-source'
COMMIT='e76d7a94e6ad819e2aa9dc99083ecfa3e7842e0b'
TREE_PIN='8d5e573dd2cb25f1fd3979e7326a27e11375749e7938103022066a2fcf5d4d34'

def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def metadata():
    raw=(PROFILE/'pr358-tree.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=TREE_PIN:raise ValueError('source inventory changed')
    m=json.loads(raw)
    if m['commit']!=COMMIT or len(m['files'])!=839:raise ValueError('unsupported source inventory')
    for row in m['files']:
        p=Path(row['path'])
        if p.is_absolute() or '..' in p.parts:raise ValueError('unsafe source path')
    return m

def verify(root):
    root=Path(root)
    if root.is_symlink():raise ValueError('source root may not be a symlink')
    m=metadata();paths=list(root.rglob('*'))
    if any(p.is_symlink() for p in paths):raise ValueError('source symlink')
    if {p.relative_to(root).as_posix() for p in paths if p.is_file()}!={r['path'] for r in m['files']}:
        raise ValueError('source file inventory mismatch')
    for r in m['files']:
        data=(root/r['path']).read_bytes()
        if len(data)!=r['size'] or blob(data)!=r['sha']:raise ValueError('source blob mismatch: '+r['path'])
    return m

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--from',dest='local',type=Path,help='Copy an existing exact package instead of downloading')
    a=ap.parse_args();m=metadata()
    if SOURCE.exists():
        verify(SOURCE);print('PASS existing 839 pinned blobs');return
    if a.local:verify(a.local)
    SOURCE.mkdir(parents=True)
    def obtain(r):
        p=SOURCE/r['path'];p.parent.mkdir(parents=True,exist_ok=True)
        if a.local:data=(a.local/r['path']).read_bytes()
        else:
            url=f"https://raw.githubusercontent.com/CrocSwap/integer-mult-bounds/{COMMIT}/{m['prefix']}/{r['path']}"
            for attempt in range(4):
                try:
                    with urllib.request.urlopen(url,timeout=45) as response:data=response.read()
                    break
                except Exception:
                    if attempt==3:raise
                    time.sleep(attempt+1)
        if len(data)!=r['size'] or blob(data)!=r['sha']:raise ValueError('download blob mismatch: '+r['path'])
        p.write_bytes(data)
    try:
        with ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(obtain,m['files']))
        verify(SOURCE)
    except BaseException:
        shutil.rmtree(SOURCE);raise
    print('PASS acquired 839 pinned blobs, '+str(sum(r['size'] for r in m['files']))+' bytes')

if __name__=='__main__':main()
