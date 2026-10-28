#!/usr/bin/env python3
"""Mutation controls for the certificate boundary. DLamdata/Codex, Apache-2.0."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('certificate', HERE / 'verify.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def require_rejection(argv, cwd, needle):
    run = subprocess.run(argv, cwd=cwd, text=True, capture_output=True, timeout=60)
    if run.returncode == 0 or needle not in run.stderr:
        raise ValueError(f'control did not reject with {needle!r}: {run.returncode}, {run.stderr[-400:]}')


with tempfile.TemporaryDirectory(prefix='leaf-saturation-controls-') as directory:
    root = Path(directory)
    package = root / 'research/direct-flow-leaf-saturation'
    package.mkdir(parents=True)
    for name in ('verify.py', 'SOURCES.json', 'RESULT.json'):
        shutil.copy2(HERE / name, package / name)
    sources = json.loads((HERE / 'SOURCES.json').read_text())
    for row in sources['files']:
        if row['usage'] == 'input':
            target = root / row['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / row['path'], target)
    source = root / 'research/direct-flow-leaf-walk/verify.py'
    original = source.read_bytes()
    source.write_bytes(original + b'\n# corrupt-source control\n')
    for mode in ([], ['-O']):
        require_rejection([sys.executable, *mode, '-B', str(package / 'verify.py')], root, 'source mismatch')
    source.write_bytes(original)
    expected = json.loads((package / 'RESULT.json').read_text())
    expected['parameters']['lambda'][0] = '0.0'
    receipt = package / 'corrupt-result.json'
    receipt.write_text(json.dumps(expected))
    require_rejection([sys.executable, '-O', '-B', str(package / 'verify.py'), '--expect', str(receipt)], root, 'expected receipt mismatch')

for name in ('paid', 'target'):
    P, W, M = v.bindings()
    histogram = P if name == 'paid' else W
    histogram[min(histogram)] += 1
    try:
        v.parameters(P, W, M)
    except ValueError as error:
        if 'invoice root bracket' not in str(error):
            raise
    else:
        raise ValueError('changed histogram passed fixed root certificate: ' + name)
print('PASS_MUTATION_CONTROLS source_bytes_normal_and_optimized corrupted_receipt paid_and_target_count_plus_one')
