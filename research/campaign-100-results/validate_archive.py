#!/usr/bin/env python3
"""Validate archive integrity and indexing, not the mathematical conclusions."""
from collections import Counter
from pathlib import Path, PurePosixPath
import csv
import gzip
import hashlib
import json
import tarfile


def main():
    root = Path(__file__).resolve().parent

    def read(name):
        return json.loads((root / name).read_text())

    def digest(data):
        return hashlib.sha256(data).hexdigest()

    def safe(name):
        p = PurePosixPath(name)
        assert not p.is_absolute() and '..' not in p.parts, name
        return root / name

    rows = read('results.json')
    assert [r['id'] for r in rows] == list(range(1, 101))
    counts = dict(Counter(r['status'] for r in rows))
    assert counts == read('COUNTS.json')
    with (root / 'results.csv').open(newline='') as stream:
        csv_rows = list(csv.DictReader(stream))
    assert len(csv_rows) == len(rows)
    for r, c in zip(rows, csv_rows):
        assert c == {**{k: str(v) for k,v in r.items() if k != 'evidence'},
                     'evidence': '; '.join(r['evidence'])}
        assert r['outcome'] and r['idea']
        for evidence in r['evidence']:
            assert safe(evidence).is_file(), evidence
    for entry in read('PROVENANCE.json'):
        data = safe(entry['archive']).read_bytes()
        if entry.get('encoding') == 'gzip':
            data = gzip.decompress(data)
        assert len(data) == entry['bytes'] and digest(data) == entry['sha256'], entry['archive']
    inventory = read('RAW-INVENTORY.json')
    for archive in sorted({r['archive'] for r in inventory}):
        entries = {r['member']: r for r in inventory if r['archive'] == archive}
        with tarfile.open(safe(archive), 'r:gz') as tf:
            members = tf.getmembers()
            assert len(members) == len(entries)
            assert {m.name for m in members} == set(entries)
            for m in members:
                safe(m.name)
                assert m.isfile(), m.name
                data = tf.extractfile(m).read()
                e = entries[m.name]
                assert len(data) == e['bytes'] and digest(data) == e['sha256'], m.name
    manifest = read('MANIFEST.json')
    actual = {str(p.relative_to(root)): digest(p.read_bytes()) for p in root.rglob('*')
              if p.is_file() and p.name != 'MANIFEST.json'}
    assert actual == manifest
    print(json.dumps({'status': 'PASS_ARCHIVE_INTEGRITY', 'ideas': len(rows),
                      'files': len(actual), 'raw_members': len(inventory),
                      'status_counts': counts}, sort_keys=True))


if __name__ == '__main__':
    main()
