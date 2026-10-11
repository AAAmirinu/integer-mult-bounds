"""Full native combined experiment, same two-worker schedule and proof code."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import sys

ROOT=Path(__file__).resolve().parent
SHA=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
OLD=ROOT.parent/'predecessor-performance/run_native.py'

def main():
    assert SHA(OLD)=='9730950a33e72812cbf47d2560d4929630c4b95350459bdb1054d5eac73ef52f'
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    args,remaining=ap.parse_known_args()
    os.environ['SOURCE_PREFIX_MODE']='admission'
    # Original admission imports verify_source from its source directory.
    os.environ['PYTHONPATH']=str(ROOT.parent/'e8-pipeline-profile/pr358-source/vendor/source353354')
    files=(Path(__file__),ROOT/'combined/share_source.py',ROOT/'share_source.py',
           ROOT/'profile_producer_fast.py',ROOT/'profile_producer.py',ROOT/'generator_adapter.py',
           OLD,ROOT.parent/'producer-prefix-sharing/share_source.py')
    pins={str(p):SHA(p) for p in files}
    ns=runpy.run_path(str(OLD),run_name='combined_native_driver')
    ns['main'].__globals__.update(PREFIX=ROOT/'combined',PREFIX_PIN=SHA(ROOT/'combined/share_source.py'))
    sys.argv=[str(OLD),'--mode','scheduled','--output',str(args.output),*remaining]
    ns['main']()
    assert all(SHA(path)==digest for path,digest in pins.items())
    output=args.output.resolve()
    report=json.loads((output/'NATIVE-PERFORMANCE-RUN.json').read_text())
    report.update(variant='admission-and-generator',source_implementation_hashes=pins)
    (output/'NATIVE-PERFORMANCE-RUN.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
