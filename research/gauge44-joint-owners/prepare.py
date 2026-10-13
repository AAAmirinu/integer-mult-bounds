"""Stage an owner-only delta for the unchanged, pinned Gauge44 verifier.

This staging command does not admit a result. Run discovery, freeze the
independently recomputed expectations, and then run strict admission.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import shutil


def read(path):
    data = path.read_bytes()
    return json.loads(gzip.decompress(data) if path.suffix == '.gz' else data)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parent', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    shutil.copytree(args.parent, args.out, ignore=shutil.ignore_patterns('__pycache__'))
    data = args.out / 'data'
    plan = read(data / 'PLAN.json')
    owners = args.candidate / 'OWNERS.json.gz'
    roles = read(owners)
    profile = read(args.candidate / 'PROFILE.json')
    assert len(roles) == 72 * 492
    assert sum(int(r) * n for r, n in profile.items()) == 520704
    plan['profile'] = profile
    plan['source_plan_sha256'] = digest(args.parent / 'data/PLAN.json')
    fields = read(args.candidate / 'PLAN-OWNER-FIELDS.json')
    plan['source_owners_sha256'] = fields['source_owners_sha256']
    plan['assignment_sha256'] = hashlib.sha256(
        json.dumps(roles, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    plan['solver_status'] = 'frozen joint-call nomination from PR649; full global admission required'
    # No dispatch, schedule, local provider, width or phase field changes.
    write(data / 'PLAN.json', plan)
    shutil.copyfile(owners, data / 'OWNERS.json.gz')
    spec = read(data / 'SPEC.json')
    spec['name'] = 'gauge44-joint-call-owners'
    spec['data']['plan_sha256'] = digest(data / 'PLAN.json')
    spec['data']['owners_sha256'] = digest(data / 'OWNERS.json.gz')
    write(data / 'SPEC.json', spec)
    write(args.out / 'DELTA-PROVENANCE.json', {
        'parent_plan_sha256': digest(args.parent / 'data/PLAN.json'),
        'parent_owners_sha256': digest(args.parent / 'data/OWNERS.json.gz'),
        'candidate_owners_sha256': digest(owners),
        'candidate_profile_sha256': digest(args.candidate / 'PROFILE.json'),
        'scope': 'Only PLAN owner/profile bookkeeping, explicit OWNERS, and expected SPEC change. All verifier code is copied unchanged.'})
    print(args.out)


if __name__ == '__main__':
    main()
