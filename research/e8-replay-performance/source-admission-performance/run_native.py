"""A/B the admitted-prefix handoff atop the previous best full schedule."""
import argparse
import hashlib
import os
from pathlib import Path
import runpy
import sys

ROOT=Path(__file__).resolve().parent
SHA=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
OLD=ROOT.parent/'predecessor-performance/run_native.py'
OLD_PIN='9730950a33e72812cbf47d2560d4929630c4b95350459bdb1054d5eac73ef52f'

def main():
    assert SHA(OLD)==OLD_PIN
    ap=argparse.ArgumentParser()
    ap.add_argument('--variant',choices=('baseline','admission'),required=True)
    args,remaining=ap.parse_known_args()
    os.environ['SOURCE_PREFIX_MODE']=args.variant
    ns=runpy.run_path(str(OLD),run_name='admitted_prefix_native')
    ns['main'].__globals__.update(PREFIX=ROOT,PREFIX_PIN=SHA(ROOT/'share_source.py'))
    sys.argv=[str(OLD),'--mode','scheduled',*remaining]
    ns['main']()
    import json
    output=Path(remaining[remaining.index('--output')+1]).resolve()
    report=json.loads((output/'NATIVE-PERFORMANCE-RUN.json').read_text())
    report.update(variant=args.variant,source_implementation_hashes={str(p):SHA(p) for p in
        (Path(__file__),ROOT/'share_source.py',ROOT/'profile_producer.py',OLD,ROOT.parent/'producer-prefix-sharing/share_source.py')})
    (output/'NATIVE-PERFORMANCE-RUN.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
