#!/usr/bin/env python3
"""Verify the bounded Lean 4.21 Phase 1 probe using ordinary Lake commands.

This is not the complete Task B verifier. See PORT-PHASE1.md.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import signal
import subprocess
import time
import tomllib

ROOT = Path(__file__).resolve().parent
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
FORBIDDEN = re.compile(
    r'\b(sorry|admit|axiom|native_decide|implemented_by|extern|unsafe|opaque)\b'
    r'|set_option\s+(?!maxHeartbeats\b|maxRecDepth\b)')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def footprint(root):
    records = [(p.relative_to(root).as_posix(), p.stat().st_size, sha(p))
               for p in sorted(root.rglob('*')) if p.is_file()]
    raw = json.dumps(records, separators=(',', ':')).encode()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'files': len(records),
            'bytes': sum(size for _, size, _ in records)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lake', default='lake', help='Lake executable selection only')
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    # Inspect inherited settings; never set or raise them. Lake itself supplies
    # its normal dependency search path to its child Lean processes.
    tuning = ['LEAN_PATH', 'LEAN_OPTS', 'LEAN_NUM_THREADS', 'LEAN_SYSROOT',
              'LEAN_SRC_PATH', 'MATHLIB_CACHE_DIR', 'LAKE_OVERRIDE_LEAN', 'LEAN_GITHASH']
    require(not any(os.environ.get(key) for key in tuning), 'External Lean tuning detected')
    stack = resource.getrlimit(resource.RLIMIT_STACK)
    require(0 < stack[0] <= 8388608, 'Raised OS stack limit detected')
    manifest = json.loads((ROOT / 'probe-manifest.json').read_text())
    for name, digest in manifest['files'].items():
        require(sha(ROOT / name) == digest, 'Changed probe source: ' + name)
    config = tomllib.loads((ROOT / 'lakefile.toml').read_text())
    require(config['lean_lib'][0]['roots'] == manifest['modules'], 'Wrong Lake roots')
    require(config['defaultTargets'] == ['InvocationProbe'], 'Wrong default target')
    for name in manifest['modules']:
        src = (ROOT / (name + '.lean')).read_text()
        # The manifested probe sources contain no nested block comments.
        src = re.sub(r'/-.*?-/', ' ', src, flags=re.S)
        src = re.sub(r'--[^\n]*', ' ', src)
        require(not FORBIDDEN.search(src), 'Forbidden source construct: ' + name)
    audit = (ROOT / 'ProbeAxioms.lean').read_text()
    wanted = re.findall(r'^#print axioms (\S+)\s*$', audit, re.M)
    require(wanted == manifest['audit_declarations'], 'Changed probe axiom inventory')
    require(len(wanted) == len(set(wanted)), 'Duplicate audit declaration')
    receipt = {'status': 'RUNNING', 'scope': 'Phase 1 probe only',
               'manifest_sha256': sha(ROOT / 'probe-manifest.json'),
               'started_utc': datetime.now(timezone.utc).isoformat(),
               'stack_limit': list(stack), 'environment_overrides': {}, 'commands': [],
               'fresh_local_build': not any(p.is_file() for p in
                                            (ROOT / '.lake/build').rglob('*'))}
    receipt['checkout_commit'] = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    receipt['tracked_checkout_clean_at_start'] = not subprocess.check_output(
        ['git', 'status', '--porcelain', '--untracked-files=no'], cwd=ROOT, text=True)

    def run(arguments, display_output=True):
        start = time.monotonic()
        print('$ lake ' + ' '.join(arguments), flush=True)
        process = subprocess.Popen([args.lake, *arguments], cwd=ROOT, text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   start_new_session=True)
        timed_out = False
        try:
            output, _ = process.communicate(timeout=2700)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGTERM)
            output, _ = process.communicate()
        # No environment override, stack change or extra Lean option is used.
        receipt['commands'].append({'command': ['lake', *arguments],
                                    'seconds': round(time.monotonic() - start, 3),
                                    'exit_code': process.returncode, 'timed_out': timed_out})
        if display_output or process.returncode or timed_out:
            print(output, end='', flush=True)
        require(not timed_out and process.returncode == 0, 'Lake command failed or exceeded 45 minutes')
        require('declaration uses \'sorry\'' not in output, 'Incomplete proof')
        return output

    try:
        version = run(['env', 'lean', '--version']).strip()
        require(version.startswith('Lean (version 4.21.0,'), 'Wrong Lean version')
        revision = run(['env', 'lean', '--githash']).strip()
        require(revision == manifest['lean_commit'], 'Wrong Lean revision')
        receipt['lean'] = version
        receipt['lean_commit'] = revision
        prefix = Path(run(['env', 'lean', '--print-prefix'], display_output=False).strip())
        receipt['toolchain'] = {
            'lean_binary_sha256': sha(prefix / 'bin/lean'),
            'lake_binary_sha256': sha(prefix / 'bin/lake'),
            'bundled_libraries': footprint(prefix / 'lib/lean')}
        build_output = run(['build'])
        modules = set(manifest['modules'])
        built = set(re.findall(r'\bBuilt (\S+)', build_output)) & modules
        replayed = set(re.findall(r'\bReplayed (\S+)', build_output)) & modules
        receipt['compiled_local_modules'] = sorted(built)
        receipt['replayed_local_modules'] = sorted(replayed)
        if receipt['fresh_local_build']:
            require(built == modules and not replayed, 'Fresh build did not compile every probe module')
        output = run(['env', 'lean', 'ProbeAxioms.lean'])
        rows = re.findall(
            r"^'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",
            output, re.M)
        require(len(rows) == len(wanted) and {name for name, _ in rows} == set(wanted),
                'Incomplete or extra axiom reports')
        require(all(set(filter(None, axioms.split(', '))) <= ALLOWED for _, axioms in rows),
                'Nonstandard axiom')
        receipt['audit_declarations'] = len(rows)
        for name, digest in manifest['files'].items():
            require(sha(ROOT / name) == digest, 'Probe source changed during build: ' + name)
        receipt['local_artifacts'] = footprint(ROOT / '.lake/build')
        receipt['module_olean_sha256'] = {
            name: sha(ROOT / '.lake/build/lib/lean' / (name + '.olean'))
            for name in manifest['modules']}
        receipt['dependencies'] = {}
        lake_manifest = json.loads((ROOT / 'lake-manifest.json').read_text())
        for package in lake_manifest['packages']:
            directory = ROOT / lake_manifest['packagesDir'] / package['name']
            head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=directory,
                                           text=True).strip()
            require(head == package['rev'], 'Wrong dependency commit: ' + package['name'])
            dirty = subprocess.check_output(['git', 'status', '--porcelain',
                                            '--untracked-files=no'], cwd=directory, text=True)
            require(not dirty, 'Modified dependency: ' + package['name'])
            extra = subprocess.check_output(['git', 'ls-files', '--others',
                                             '--exclude-standard', '-z'], cwd=directory).decode().split('\0')
            require(not any(name.endswith('.lean') for name in extra),
                    'Untracked Lean dependency source: ' + package['name'])
            paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=directory).decode().split('\0')
            records = [(name, sha(directory / name)) for name in sorted(filter(None, paths))]
            receipt['dependencies'][package['name']] = {
                'commit': head, 'tracked_source_sha256': hashlib.sha256(
                    json.dumps(records, separators=(',', ':')).encode()).hexdigest(),
                'build_artifacts': footprint(directory / '.lake/build')}
        receipt['status'] = 'PASS'
    except Exception as exc:
        receipt['status'] = 'FAIL'
        receipt['error'] = str(exc)
        raise
    finally:
        receipt['completed_utc'] = datetime.now(timezone.utc).isoformat()
        if args.receipt:
            args.receipt.write_text(json.dumps(receipt, indent=2) + '\n')
    print(f"PASS Phase 1 probe: {len(manifest['modules'])} modules; {len(wanted)} axiom reports")


if __name__ == '__main__':
    main()
