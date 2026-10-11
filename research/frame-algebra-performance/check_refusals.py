"""Ensure the full adapter rejects changed sources, reused outputs and -O."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from common import ROOT, verify_source


def main():
    source = verify_source(Path(sys.argv[1]))
    with tempfile.TemporaryDirectory(prefix='frame-refusals-') as temporary:
        root = Path(temporary)
        copied = root/'source'
        shutil.copytree(source, copied)
        output = root/'output'
        command = [sys.executable, '-B', str(ROOT/'run.py'), str(copied), str(output)]
        changed = copied/'code/stagelib.py'
        original = changed.read_bytes()
        changed.write_bytes(original+b'\n')
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0 or 'source hash mismatch: code/stagelib.py' not in result.stderr or output.exists():
            raise RuntimeError('tampered-source refusal did not occur before replay')
        changed.write_bytes(original)
        output.mkdir()
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0 or 'output must be a fresh directory' not in result.stderr:
            raise RuntimeError('reused output was accepted')
        output.rmdir()
        optimized = [sys.executable, '-B', '-O', *command[2:]]
        result = subprocess.run(optimized, capture_output=True, text=True)
        if result.returncode == 0 or 'verification requires assertions enabled' not in result.stderr or output.exists():
            raise RuntimeError('assertion-disabled replay was accepted')
        verify_source(copied)
    verify_source(source)
    print('PASS: changed source, reused output and assertion-disabled replay rejected')


if __name__ == '__main__':
    main()
