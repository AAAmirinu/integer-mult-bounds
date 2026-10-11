"""Reproduce the selected frame-only bit change from the pinned PR370 word."""
from pathlib import Path
import gzip,json,sys,time,importlib.util
import retime
ROOT=Path(__file__).resolve().parent
def generate():
    sys.path.insert(0,str(ROOT/'vendor/source376'))
    import frame_replay,reuse_replay
    source=(ROOT/'data/baseline.json.gz').read_bytes()
    frames=json.loads((ROOT/'vendor/source376/frame-selection.json').read_text())
    reuse=json.loads((ROOT/'vendor/source376/reuse-selection.json').read_text())
    first=frame_replay.reconstruct(source,frames)
    assert len(frame_replay.negative_controls(source,frames))==3
    raw=reuse_replay.reconstruct(first,reuse)
    assert len(reuse_replay.negative_controls(first,reuse))==3
    assert json.loads(raw)==json.load(gzip.open(ROOT/'data/reused-baseline.json.gz','rt'))
    word=json.loads(raw);accepted=0
    for cycle in range(3):
        word,changes=retime.retime(word,'retime_both',sweeps=10);accepted+=len(changes)
        word,changes=retime.pairs(word,sweeps=3);accepted+=len(changes)
        word,changes,_=retime.groups(word,size=3,sweeps=3,limit=100000);accepted+=len(changes)
    assert accepted==70,'Accepted move count changed'
    expected=json.load(gzip.open(ROOT/'data/retimed.json.gz','rt'))
    assert word==expected,'Selected deterministic frame assignment did not reproduce'
    return word
if __name__=='__main__':
    start=time.perf_counter();word=generate();raw=json.dumps(word,sort_keys=True,separators=(',',':')).encode()
    Path(sys.argv[1]).write_bytes(gzip.compress(raw,mtime=0));print('PASS deterministic coupled-frame regeneration',round(time.perf_counter()-start,2),'seconds')
