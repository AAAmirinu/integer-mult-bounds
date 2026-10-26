#!/usr/bin/env python3
"""Publish the exact verified commit; --check is entirely offline.

The external manifest is generated after committing to avoid a self-hash cycle.
No forks are created, branches forced, main altered, or PRs merged.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import quote, urlencode

ROOT = Path(__file__).resolve().parent
DEFAULT_MANIFEST = ROOT.parent/'connector-gap-handoff'/'VERIFIED.json'
REPO = 'CrocSwap/integer-mult-bounds'


def run(args, *, check=True, input=None):
    result = subprocess.run(args, cwd=ROOT, text=True, input=input,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result


def git(*args):
    return run(['git', *args]).stdout.strip()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def check(manifest):
    require(git('branch','--show-current') == manifest['branch'], 'Wrong branch; stop')
    require(git('rev-parse','HEAD') == manifest['commit'], 'Wrong commit; stop')
    require(git('rev-parse','HEAD^') == manifest['base'], 'Wrong single-commit base; stop')
    require(not git('status','--porcelain','--untracked-files=all'), 'Working tree is not clean; stop')
    require(git('remote','get-url','--push',manifest['remote']) == manifest['fork_url'], 'Configured fork changed; stop')
    require(manifest['fork_url'] == 'https://github.com/theon199/integer-mult-bounds.git', 'Unexpected fork')
    require(manifest['branch'] != 'main', 'Refusing main')
    require({'PR_DRAFT.md','publish_contribution.py'}.issubset(manifest['tracked_files']), 'Incomplete handoff manifest')
    for name, digest in manifest['tracked_files'].items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, 'Handoff file mismatch: '+name)
    patch = Path(manifest['patch'])
    require(patch.is_file() and hashlib.sha256(patch.read_bytes()).hexdigest() == manifest['patch_sha256'], 'Missing or changed single-commit patch')
    require(patch.read_text().startswith('From '+manifest['commit']+' '), 'Patch describes a different commit')
    title, _, body = (ROOT/'PR_DRAFT.md').read_text().partition('\n')
    require(title.startswith('# ') and body.strip(), 'Malformed PR_DRAFT.md')
    return title[2:], body.lstrip('\n')


def remote_head(manifest):
    output = git('ls-remote',manifest['remote'],'refs/heads/'+manifest['branch'])
    return output.split()[0] if output else None


def existing_prs(manifest):
    query = urlencode({'state':'all','head':manifest['owner']+':'+manifest['branch'],'per_page':100})
    result = run(['gh','api','repos/'+REPO+'/pulls?'+query])
    return [p for p in json.loads(result.stdout)
            if p['head']['label'] == manifest['owner']+':'+manifest['branch']]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Verify locally; do not contact GitHub')
    parser.add_argument('--manifest',type=Path,default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    title, body = check(manifest)
    if args.check:
        print('PASS_OFFLINE_PUBLICATION_CHECK',manifest['commit'])
        return
    handoff = args.manifest.resolve().parent
    # One immutable head. A different existing remote commit is not overwritten.
    prior_head = remote_head(manifest)
    require(prior_head in (None,manifest['commit']), 'Remote branch has a different commit; stop')
    if prior_head is None:
        run(['git','push',manifest['remote'],manifest['commit']+':refs/heads/'+manifest['branch']])
    require(remote_head(manifest) == manifest['commit'], 'Push not verified; no ready comparison URL')
    url = ('https://github.com/'+REPO+'/compare/main...'+manifest['owner']+':'+
           quote(manifest['branch'],safe='/')+'?'+urlencode({'expand':'1','title':title,'body':body}))
    (handoff/'COMPARE_URL.txt').write_text(url+'\n')
    receipt = {'branch':manifest['branch'],'commit':manifest['commit'],'pushed':True,
               'remote_commit_verified':True,'comparison_url':url,'pr_url':None}
    def finish():
        (handoff/'PUBLICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
        print('Remote head verified:',manifest['commit'])
        print('PR:',receipt['pr_url'] or 'not confirmed')
        print('Browser fallback (choose Create draft pull request):',url)
    try:
        existing = existing_prs(manifest)
        if existing:
            receipt['pr_url'] = existing[0]['html_url']
            receipt['pr_state'] = existing[0]['state']
            finish()
            return
    except RuntimeError as exc:
        receipt['error'] = 'Cannot check for duplicates; creation skipped: '+str(exc)
        finish()
        return
    # Record an attempt before making it; a later invocation will not repeat a denied POST.
    attempted = handoff/'PR_CREATION_ATTEMPT.json'
    if attempted.exists():
        receipt['error'] = 'A previous creation attempt exists; use the browser fallback.'
        finish()
        return
    attempted.write_text(json.dumps({'commit':manifest['commit'],'head':manifest['branch']})+'\n')
    payload = {'title':title,'body':body,'head':manifest['owner']+':'+manifest['branch'],
               'base':'main','draft':True,'maintainer_can_modify':True}
    created = run(['gh','api','--method','POST','repos/'+REPO+'/pulls','--input','-'],
                  input=json.dumps(payload),check=False)
    if created.returncode == 0:
        pr = json.loads(created.stdout)
        receipt['pr_url'] = pr['html_url']
        receipt['pr_state'] = pr['state']
        receipt['draft'] = pr['draft']
    else:
        receipt['error'] = created.stderr.strip()
        # A failed response can follow a successful request: verify both outcomes.
        receipt['remote_commit_verified'] = remote_head(manifest) == manifest['commit']
        try:
            existing = existing_prs(manifest)
            if existing:
                receipt['pr_url'] = existing[0]['html_url']
                receipt['pr_state'] = existing[0]['state']
        except RuntimeError as exc:
            receipt['duplicate_recheck_error'] = str(exc)
    finish()


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError, KeyError) as exc:
        print('STOP:',exc,file=sys.stderr)
        sys.exit(1)
