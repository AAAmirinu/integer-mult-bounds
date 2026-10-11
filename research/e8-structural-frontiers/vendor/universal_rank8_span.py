"""Pattern-only lower bound on copied source-span for rank-eight completions.

This is independent of the frozen center gather matrix. It does not constrain
completions of rank > 8, or eliminate nonmonotone/joint bridge constructions.
OpenAI Codex assistance; Apache-2.0; read-only pinned supplier.
"""
from pathlib import Path
from collections import Counter
import gzip, hashlib, json, importlib.util, argparse, sys
from fractions import Fraction as Q

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1] / 'extension-repo'
SOURCE = REPO / 'research/e8-clean-reuse-extension/data/kernel-base.json.gz'
SOURCE_SHA256 = '785a6160912b8bf8535ccd438c7d13c0730f874d6a5d07ef530e50279e7cf7d8'
BUDGET_SOURCE = REPO / 'research/e8-clean-reuse-extension/data/complex-candidate.json.gz'
BUDGET_SHA256 = '0e3a9ceb4ab14a126a8e9e0d056322f9d2234ccda4f7472a8ad2849bd7a54131'
MOMENT_ENGINE = REPO / 'research/e8-coupled-bit-retiming/vendor/source377/work/pr361/code/engines/moment.py'
MOMENT_SHA256 = '81cbc864e106418fc7854322746f72180cb8110ff39f74450a3b8d55a82c1482'
sys.dont_write_bytecode = True


def pinned_bytes(path, expected):
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    assert actual == expected, 'Pinned input bytes changed: ' + path.name
    return raw


def clique(adj, chosen, candidates, goal):
    if len(chosen) == goal:
        return chosen
    if len(chosen) + candidates.bit_count() < goal:
        return None
    while candidates:
        bit = candidates & -candidates
        z = bit.bit_length() - 1
        candidates ^= bit
        result = clique(adj, chosen + [z], candidates & adj[z], goal)
        if result is not None:
            return result
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--budget-source', type=Path, default=BUDGET_SOURCE)
    parser.add_argument('--moment-engine', type=Path, default=MOMENT_ENGINE)
    parser.add_argument('--output', type=Path, default=HERE / 'UNIVERSAL-RANK8-SPAN.json')
    parser.add_argument('--immutable-root', type=Path,
                        help='Additional repository root where output is forbidden.')
    args = parser.parse_args()
    args.source = args.source.resolve()
    args.budget_source = args.budget_source.resolve()
    args.moment_engine = args.moment_engine.resolve()
    args.output = args.output.resolve()
    immutable_roots = {REPO.resolve()}
    if args.immutable_root:
        immutable_roots.add(args.immutable_root.resolve())
    for input_path in (args.source, args.budget_source, args.moment_engine):
        for ancestor in input_path.parents:
            if (ancestor / '.git').exists():
                immutable_roots.add(ancestor)
                break
    if any(args.output == root or root in args.output.parents for root in immutable_roots):
        parser.error('--output must be outside every immutable input repository')
    raw = pinned_bytes(args.source, SOURCE_SHA256)
    c = json.loads(gzip.decompress(raw))
    ports = c['ports']
    assert (c['h'], c['v'], len(ports)) == (9, 120, 120)
    assert len(set(ports)) == 120 and all(q.bit_count() % 2 for q in ports)
    odd = lambda a, b: (a & b).bit_count() % 2
    adj = [sum(1 << j for j, q in enumerate(ports)
               if j != i and odd(p, q)) for i, p in enumerate(ports)]
    witnesses = []
    bad = set()
    for a in range(1, 512):
        outside = sum(1 << i for i, q in enumerate(ports) if odd(a, q))
        witness = clique(adj, [], outside, 8)
        if witness is None:
            bad.add(a)
            continue
        assert len(set(witness)) == 8
        assert all(odd(a, ports[i]) for i in witness)
        assert all(odd(ports[i], ports[j]) for i in witness for j in witness)
        witnesses.append(dict(normal=a, outside_ports=outside.bit_count(),
                              identity_minor_ports=witness))

    # Every 3-dimensional normal subspace has a clique-certified normal.
    # An all-bad 3-space would have independent a,b,c and all seven nonzero
    # sums bad. Enumerate all possible ordered generating triples.
    pairs = [(a, b) for a in sorted(bad) for b in sorted(bad)
             if a < b and (a ^ b) in bad]
    generating_triples_checked = 0
    bad_three_spaces = set()
    for a, b in pairs:
        plane = {a, b, a ^ b}
        for d in sorted(bad - plane):
            generating_triples_checked += 1
            nonzero = tuple(sorted((a, b, a ^ b, d, a ^ d, b ^ d, a ^ b ^ d)))
            assert len(set(nonzero)) == 7
            if all(z in bad for z in nonzero):
                bad_three_spaces.add(nonzero)
    assert not bad_three_spaces
    assert (len(witnesses), len(bad)) == (391, 120)
    assert bad == {a for a in range(1, 512) if a.bit_count() in (2, 6)}
    bad_two_planes = {tuple(sorted((a, b, a ^ b))) for a, b in pairs}
    assert len(bad_two_planes) == 1120

    # Cost-only screen: replace exactly the eight rank9 private centers by
    # eight rank7 copies, and leave every other cost and W fixed. This is
    # an optimistic hypothetical invoice, not a candidate construction.
    z = json.loads(gzip.decompress(pinned_bytes(args.budget_source, BUDGET_SHA256)))
    assert z['R'] == 779
    h = Counter()
    for block in z['blocks'].values():
        for r, n in block.items():
            h[int(r)] += 72 * n
    for r in [16, 8, 32, 8, 48, 8, 48, 32, 16]:
        h[r] += 1920
    h[1] += 9 * z['R']
    assert h[9] >= 576
    h[9] -= 576
    h[7] += 576
    h = Counter({r: n for r, n in h.items() if n > 0})
    m, W = 73, 7680 + 9 * z['R']
    pinned_bytes(args.moment_engine, MOMENT_SHA256)
    spec = importlib.util.spec_from_file_location('universal_center_moment', args.moment_engine)
    M = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(M)
    lo, hi = M.moment(h, m, W, Q(1, 499), True)
    assert lo > 1
    result = dict(
        status='PASS_PATTERN_ONLY_RANK8_SOURCE_SPAN_LOWER_BOUND',
        source_sha256=SOURCE_SHA256,
        ports=ports,
        completion_hypothesis='Over any characteristic-zero field: rank(C)=8, C_tt=1, C_ts=0 for t!=s and binary q_t dot q_s=1.',
        clique_certified_normals=len(witnesses),
        clique_witnesses=witnesses,
        no_eight_clique_normals=sorted(bad),
        no_eight_clique_normals_weight_characterization=[2, 6],
        all_bad_two_plane_generating_pairs=len(pairs),
        distinct_all_bad_two_planes=len(bad_two_planes),
        independent_third_generators_checked=generating_triples_checked,
        all_bad_three_spaces=sorted(bad_three_spaces),
        support_span_lower_bound=7,
        eight_independent_copied_centers_rank_mass_lower_bound=56,
        conclusion='For any rank8 completion of the pattern, every nonzero row-space form has binary source support span at least7. This is weaker than frozen-basis bound9 and does not establish attainability7.',
        hypothetical_unchanged_side_budget=dict(
            description='Exactly eight rank7 copied centers replace eight rank9 copies; all other R779 calls, W and fallback fixed.',
            target_kappa='1/500', necessary_coarse='1/499', m=m, W=W,
            histogram={str(r): n for r, n in sorted(h.items())},
            budget_source_sha256=BUDGET_SHA256, moment_engine_sha256=MOMENT_SHA256,
            deficit=m*W-sum(r*n for r,n in h.items()),
            moment_lower=str(lo), moment_upper=str(hi),
            verdict='EXCLUDED_EVEN_IN_THIS_COST_MODEL',
            warning='No local word, coefficient/phase proof or center-frame compiler is constructed. The exclusion only applies to this unchanged-side invoice.'))
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('ports', 'clique_witnesses', 'no_eight_clique_normals')}, indent=2))


if __name__ == '__main__':
    main()
