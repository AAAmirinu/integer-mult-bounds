"""Fresh full-pipeline A/B: only scalar admission differs between variants."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import runpy
import sys
import time

ROOT=Path(__file__).resolve().parent
SHA=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
OLD=ROOT.parent/'predecessor-performance/run_native.py'
PREVIOUS=ROOT.parent/'source-admission-performance'

def main():
    assert SHA(OLD)=='9730950a33e72812cbf47d2560d4929630c4b95350459bdb1054d5eac73ef52f'
    ap=argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--variant',choices=('baseline','optimized'),required=True)
    ap.add_argument('--output',type=Path,required=True)
    args,remaining=ap.parse_known_args()
    os.environ.update(SCALAR_ADMISSION_VARIANT=args.variant,SOURCE_PREFIX_MODE='admission',
        PYTHONHASHSEED='0',PYTHONPATH=str(ROOT.parent/'e8-pipeline-profile/pr358-source/vendor/source353354'))
    files=[Path(__file__),ROOT/'share_source.py',ROOT/'scalar_adapter.py',OLD,
        ROOT.parent/'producer-prefix-sharing/share_source.py']
    files.extend(PREVIOUS/name for name in ('share_source.py','profile_producer.py','profile_producer_fast.py','generator_adapter.py'))
    pins={str(p):SHA(p) for p in files}
    ns=runpy.run_path(str(OLD),run_name='scalar_native_driver')
    ns['main'].__globals__.update(PREFIX=ROOT,PREFIX_PIN=SHA(ROOT/'share_source.py'))
    sys.argv=[str(OLD),'--mode','scheduled','--output',str(args.output),*remaining]
    before=resource.getrusage(resource.RUSAGE_CHILDREN)
    began=time.perf_counter()
    ns['main']()
    after=resource.getrusage(resource.RUSAGE_CHILDREN)
    assert all(SHA(path)==digest for path,digest in pins.items())
    output=args.output.resolve()
    report=json.loads((output/'NATIVE-PERFORMANCE-RUN.json').read_text())
    report.update(variant=args.variant,source_implementation_hashes=pins,pythonhashseed='0',
        process_tree_cpu_seconds=(after.ru_utime+after.ru_stime)-(before.ru_utime+before.ru_stime),
        outer_seconds=time.perf_counter()-began)
    (output/'NATIVE-PERFORMANCE-RUN.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
