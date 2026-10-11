"""Fetch the exact PR364 package into a fresh external directory."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import shutil
import time
import urllib.error
import urllib.request

from common import ROOT, SOURCE, sha, verify_source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--copy-from', type=Path, help='copy a verified local package instead of downloading')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() or output.is_relative_to(ROOT):
        parser.error('output must be a fresh directory outside this package')
    if args.copy_from:
        verify_source(args.copy_from)
    output.mkdir(parents=True)
    base = ('https://raw.githubusercontent.com/'+SOURCE['repository']+'/'+
            SOURCE['commit']+'/'+SOURCE['prefix']+'/')
    def fetch(name):
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('unsafe pinned path')
        target = output/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if args.copy_from:
            shutil.copyfile(args.copy_from/relative, target)
        else:
            for attempt in range(3):
                try:
                    with urllib.request.urlopen(base+name, timeout=60) as response:
                        target.write_bytes(response.read())
                    break
                except (urllib.error.URLError, TimeoutError):
                    if attempt == 2:
                        raise
                    time.sleep(.5 * (attempt+1))
        if sha(target) != SOURCE['files'][name]:
            raise ValueError('download hash mismatch: '+name)
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(fetch, SOURCE['files']))
    verify_source(output)
    print('PASS: verified', len(SOURCE['files']), 'immutable source files at', output)


if __name__ == '__main__':
    main()
