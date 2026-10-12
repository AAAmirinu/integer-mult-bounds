#!/usr/bin/env python3
"""Check the portable review inventory and the A/B proof/receipt source bindings."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BASE = 'db0e57bc7f36b5ac0fc844ad7ce1396165ee6647'
DIRECTORIES = [
    'lean-whole-residual-hosting', 'lean-multi-host-framework',
    'lean-multi-host-source', 'lean-external-review',
    'lean-single-stream-obstruction', 'lean-source-invocation-audit',
    'lean-contribution-archive',
]
# Avoid a circular digest. The delivery SHA256SUMS covers both files.
EXCLUDED = {'research/lean-external-review/package-manifest.json',
            'research/lean-external-review/package-validation.json'}
ROOT_FILES = ['LICENSE', 'NOTICE', 'CONTRIBUTING.md']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def inventory():
    files = [ROOT / name for name in ROOT_FILES]
    for name in DIRECTORIES:
        files.extend(p for p in (ROOT / 'research' / name).rglob('*')
                     if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    require(all(not p.is_symlink() for p in files), 'Symlink in review sources')
    return {str(p.relative_to(ROOT)): sha(p) for p in sorted(files)
            if str(p.relative_to(ROOT)) not in EXCLUDED}


def object_sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def digest_string(value):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value) is not None


def footprint(record, label):
    require(digest_string(record['sha256']), label + ': invalid fingerprint')
    require(type(record['files']) is int and record['files'] >= 0 and
            type(record['bytes']) is int and record['bytes'] >= 0,
            label + ': invalid footprint counts')


def audit_inventory(receipt, names, allowed, label):
    require(list(receipt['axioms']) == names, label + ': axiom inventory mismatch')
    require(all(isinstance(axioms, list) and set(axioms) <= allowed
                for axioms in receipt['axioms'].values()), label + ': unexpected axioms')


def bindings(allow_pending_task_b=False):
    # Only these fresh receipts establish the current build claim. Original
    # replay-result.json and archived review receipts remain inventory-covered
    # historical evidence; neither they nor a metadata reanchor authorize reuse.
    a = ROOT / 'research/lean-multi-host-framework'
    b = ROOT / 'research/lean-multi-host-source'
    ma = json.loads((a / 'proof-manifest.json').read_text())
    mb = json.loads((b / 'proof-manifest.json').read_text())
    current_a = json.loads((HERE / 'validation/task-a.json').read_text())
    task_b_receipt = HERE / 'validation/task-b.json'
    current_b = json.loads(task_b_receipt.read_text()) if task_b_receipt.exists() else None
    receipts = [('Task A', current_a, a)]
    if current_b is not None:
        receipts.append(('Task B', current_b, b))
    for label, receipt, directory in receipts:
        require(receipt['status'] == 'PASS', label + ': fresh replay failed')
        require(receipt['trust_level'] == 0, label + ': replay was not at trust level zero')
        require(receipt['replay_mode'] == 'fresh' and receipt['reused_modules'] == 0,
                label + ': current receipt is not a fully fresh build')
        require(receipt['manifest_sha256'] == sha(directory / 'proof-manifest.json'),
                label + ': fresh receipt/current manifest mismatch')
        require(receipt['lean_commit'] == ma['lean_commit'] == mb['lean_commit'],
                label + ': Lean pin mismatch')
        require(receipt['lean'].startswith('Lean (version 4.33.0,'),
                label + ': wrong Lean version')
    require(current_a['fresh_modules_compiled'] == len(ma['sha256']),
            'Task A fresh module count mismatch')
    require(current_a['source_sha256'] == ma['sha256'], 'Task A receipt/source mismatch')
    audit_inventory(current_a, ma['theorems'], {'propext', 'Quot.sound'}, 'Task A')
    footprint(current_a['toolchain'], 'Task A toolchain')
    require(digest_string(current_a['toolchain']['lean_binary_sha256']),
            'Task A compiler fingerprint is invalid')
    for name, digest in ma['sha256'].items():
        parent = a if name not in {'CoordinateSwap', 'Hosting', 'PhysicalHosting'} else a.parent / 'lean-whole-residual-hosting'
        require(sha(parent / (name + '.lean')) == digest, 'Task A source mismatch: ' + name)

    module_names = [module['module'] for module in mb['modules']]
    require(len(set(module_names)) == len(module_names), 'Duplicate Task B module')
    require('SourceInvocation.actualContract' in mb['audit_declarations'],
            'Task B actualContract is absent from the permanent axiom inventory')
    # A pending package still binds every manifested source and its import
    # graph. It makes no claim that the pending Lean replay has succeeded.
    prior_sources = set()
    for module in mb['modules']:
        name = module['module']
        source = (b / module['source']).resolve()
        require(source.is_relative_to(ROOT), 'Dependency outside delivery: ' + name)
        require(sha(source) == module['sha256'], 'Task B manifested source mismatch: ' + name)
        code = re.sub(r'--[^\n]*', '', re.sub(r'/\-[\s\S]*?\-/', '', source.read_text()))
        require(re.findall(r'^import (\S+)$', code, re.M) == module['imports'],
                'Task B manifested import mismatch: ' + name)
        require(all(dep in prior_sources or dep == 'Std' or dep.startswith('Mathlib.')
                    for dep in module['imports']), 'Unordered or unmanifested dependency: ' + name)
        prior_sources.add(name)
    versions = json.loads((b / 'source-versions.json').read_text())
    require(versions['mathlib']['commit'] == mb['mathlib_commit'],
            'Mathlib pin mismatch')
    require(versions['lean']['commit'] == mb['lean_commit'], 'Source version Lean mismatch')
    require(json.loads((HERE / 'validation/source-binding.json').read_text())['status'] == 'PASS',
            'Source binding receipt failed')
    run = json.loads((HERE / 'validation/run-metadata.json').read_text())
    require(run['upstream_base_commit'] == BASE, 'Run metadata upstream base mismatch')
    for key, script, mode in [('task_a', a / 'replay.py', 'fresh'),
                              ('task_b', b / 'replay.py', 'fresh'),
                              ('source_binding', b / 'check_sources.py', 'fresh regeneration')]:
        require(run[key]['script_sha256'] == sha(script) and run[key]['mode'] == mode,
                'Current runner metadata mismatch: ' + key)
    if current_b is None:
        require(allow_pending_task_b,
                'Fresh Task B receipt is absent; --allow-pending-task-b reports an explicitly unfinished package')
        require(run['task_b'].get('status') == 'running',
                'Pending Task B requires run metadata explicitly marked running')
        return {'status': 'PENDING_TASK_B', 'task_b_verified': False,
                'task_b_notice': 'Fresh Task B replay in progress; receipt will be added to this PR.',
                'task_a_modules': len(ma['sha256']), 'task_b_modules': len(module_names),
                'task_a_theorem_closures': len(ma['theorems']),
                'task_b_planned_audit_declarations': len(mb['audit_declarations']),
                'task_a_replay_mode': 'fresh', 'task_b_replay_mode': 'pending',
                'task_a_receipt_sha256': sha(HERE / 'validation/task-a.json'),
                'task_b_receipt_sha256': None}
    require(current_a['lean'] == current_b['lean'], 'Task A/B compiler version mismatch')
    require(current_b['mathlib_commit'] == mb['mathlib_commit'], 'Task B receipt Mathlib pin mismatch')
    require(list(current_b['modules']) == module_names, 'Task B module inventory mismatch')
    require(current_b['fresh_modules_compiled'] == len(module_names) and
            current_b['fresh_module_names'] == module_names and
            current_b['reused_module_names'] == [] and current_b['legacy_module_names'] == [] and
            current_b['legacy_reused_modules'] == 0,
            'Task B fresh/reuse inventory mismatch')
    require(current_b['historical_external_environment'] == 'fingerprinted_at_compile',
            'Task B compile environment was not fingerprinted')
    require('SourceInvocation.actualContract' in mb['audit_declarations'],
            'Task B actualContract is absent from the permanent axiom inventory')
    audit_inventory(current_b, mb['audit_declarations'],
                    {'propext', 'Quot.sound', 'Classical.choice'}, 'Task B')

    external = current_b['external_environment']
    components = external['components']
    require(components['schema'] == 1 and object_sha(components) == external['sha256'],
            'Task B external environment fingerprint mismatch')
    footprint(components['toolchain'], 'Task B toolchain')
    require(all(current_a['toolchain'][key] == components['toolchain'][key]
                for key in ['sha256', 'files', 'bytes']) and
            current_a['toolchain']['lean_binary_sha256'] == components['lean_binary_sha256'] and
            digest_string(components['lean_binary_sha256']),
            'Task A/B toolchain footprint mismatch')
    lake_manifest = json.loads((b / 'mathlib-lake-manifest.json').read_text())
    expected_dependencies = {'Mathlib': mb['mathlib_commit']}
    for package in lake_manifest['packages']:
        require(package['type'] == 'git' and not package.get('subDir'),
                'Unsupported external dependency layout: ' + package['name'])
        expected_dependencies[package['name']] = package['rev']
    dependencies = components['dependencies']
    require(set(dependencies) == set(expected_dependencies),
            'External dependency inventory mismatch')
    for name, commit in expected_dependencies.items():
        require(dependencies[name]['commit'] == commit, 'External dependency pin mismatch: ' + name)
        for key in ['tracked_sources', 'build_artifacts', 'lake_configuration_artifacts']:
            footprint(dependencies[name][key], name + '/' + key)
    allowed_search = {name + '/.lake/build/lib/lean' for name in dependencies} | {'toolchain/lib/lean'}
    search = components['library_search_order']
    require(set(search) <= allowed_search and len(set(search)) == len(search) and
            'Mathlib/.lake/build/lib/lean' in search, 'Unexpected external library search order')

    prior = {}
    for module in mb['modules']:
        name = module['module']
        record = current_b['modules'][name]
        source = (b / module['source']).resolve()
        require(source.is_relative_to(ROOT), 'Dependency outside delivery: ' + name)
        require(sha(source) == module['sha256'] == record['sha256'],
                'Task B source/receipt mismatch: ' + name)
        require(record['environment_sha256'] == external['sha256'] and
                record['historical_external_environment'] == 'fingerprinted_at_compile' and
                'legacy_receipt' not in record, 'Task B module lacks fresh environment binding: ' + name)
        artifacts = record['artifacts']
        require(artifacts.get('.olean') == record['olean_sha256'] and
                set(artifacts) <= {'.olean', '.olean.private', '.olean.server', '.ir', '.ir.sig', '.so'} and
                all(digest_string(digest) for digest in artifacts.values()),
                'Task B artifact fingerprint mismatch: ' + name)
        local = [dep for dep in module['imports'] if dep in prior]
        require(all(dep in prior or dep == 'Std' or dep.startswith('Mathlib.')
                    for dep in module['imports']), 'Unordered or unmanifested dependency: ' + name)
        require(record['dependency_hashes'] == {dep: prior[dep]['olean_sha256'] for dep in local},
                'Task B dependency olean binding mismatch: ' + name)
        require(record['dependency_artifacts'] == {dep: prior[dep]['artifacts'] for dep in local},
                'Task B dependency artifact binding mismatch: ' + name)
        require(record['dependency_source_sha256'] == {dep: prior[dep]['sha256'] for dep in local},
                'Task B dependency source binding mismatch: ' + name)
        prior[name] = record

    return {'status': 'PASS', 'task_b_verified': True, 'task_a_modules': len(ma['sha256']), 'task_b_modules': len(module_names),
            'task_a_theorem_closures': len(ma['theorems']),
            'task_b_theorem_closures': len(mb['audit_declarations']),
            'task_a_replay_mode': 'fresh', 'task_b_replay_mode': 'fresh',
            'task_a_receipt_sha256': sha(HERE / 'validation/task-a.json'),
            'task_b_receipt_sha256': sha(HERE / 'validation/task-b.json')}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--write-manifest', action='store_true',
                   help='for package preparation only; reviewers should omit this')
    p.add_argument('--receipt', type=Path)
    p.add_argument('--allow-pending-task-b', action='store_true',
                   help='allow an absent Task B receipt only when explicitly marked running; result is PENDING_TASK_B')
    args = p.parse_args()
    files = inventory()
    counts = bindings(allow_pending_task_b=args.allow_pending_task_b)
    manifest_path = HERE / 'package-manifest.json'
    if args.write_manifest:
        manifest_path.write_text(json.dumps({
            'base_commit': BASE, 'validation_status': counts['status'],
            'historical_task_a_commit': '13611a8958fc71046a83d8431d2bd6335e6a3e2f',
            'historical_task_b_commit': 'f7330c5f5b1c5e85f91a98c95e8efc0e27c03490',
            'excluded_from_recursive_hash': sorted(EXCLUDED), 'sha256': files,
        }, indent=2) + '\n')
    expected = json.loads(manifest_path.read_text())
    require(expected['base_commit'] == BASE, 'Package manifest upstream base mismatch')
    require(expected['validation_status'] == counts['status'], 'Package validation status mismatch')
    require(files == expected['sha256'], 'Package inventory differs from package-manifest.json')
    result = {'status': counts['status'], 'completed_utc': datetime.now(timezone.utc).isoformat(),
              'manifest_sha256': sha(manifest_path), 'files_checked': len(files), **counts,
              'scope': 'Inventory, manifested sources and available fresh receipt bindings; PENDING_TASK_B means Task B verification is unfinished. This verifier does not run Lean or authenticate build provenance.'}
    if args.receipt:
        args.receipt.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
