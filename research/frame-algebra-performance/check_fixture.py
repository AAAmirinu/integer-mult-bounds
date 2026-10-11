"""Rebuild the offline matrix corpus from a successful pinned full replay."""
import argparse
import gzip
import json
from pathlib import Path

from common import ROOT, SOURCE, sha, verify_outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('replay', type=Path)
    args = parser.parse_args()
    verify_outputs(args.replay)
    unique = {}
    for stage in ('TT', 'K', 'KR', 'KRO', 'F'):
        frames = json.loads((args.replay/stage/'frames.json').read_text())['frames']
        for frame in frames.values():
            row = {'B': frame['B'], 'A': frame['A']}
            key = json.dumps(row, sort_keys=True, separators=(',', ':'))
            unique[key] = row
    rebuilt = json.dumps(list(unique.values()), separators=(',', ':')).encode()
    fixture = ROOT/SOURCE['fixture']['path']
    if sha(fixture) != SOURCE['fixture']['sha256']:
        raise ValueError('fixture checksum mismatch')
    if rebuilt != gzip.decompress(fixture.read_bytes()):
        raise ValueError('offline fixture does not equal the replayed frame corpus')
    print('PASS: offline fixture equals all', len(unique), 'distinct replayed B/A pairs')


if __name__ == '__main__':
    main()
