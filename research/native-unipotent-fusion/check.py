#!/usr/bin/env python3
"""Exact native BIT fusion checks; Python standard library, no external files."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def outer(a, b):
    return [[x*y for y in b] for x in a]


def add(a, b, scale=1):
    return [[x+scale*y for x, y in zip(r, s)] for r, s in zip(a, b)]


def fractions(a):
    return [[F(x) for x in row] for row in a]


def lift(g):
    return [[(F(i % 3 == j % 3) +
              (g[i % 3][j % 3] if i//3 == j//3 else -g[i % 3][j % 3]))/2
             for j in range(6)] for i in range(6)]


def affine(dst, terms, diagonal=F(1)):
    return {'op': 'ORDERED_AFFINE', 'dst': dst, 'diagonal': str(diagonal),
            'terms': [[i, str(c)] for i, c in terms if c]}


def lower(s, v):
    """Independently derive the ordered rank-one word, rather than trusting JSON."""
    determinant = 1 + sum(x*y for x, y in zip(s, v))
    pivot = s[0]*v[-1]
    require(bool(determinant and pivot), 'singular rank-one lowering')
    word = [affine(i, [(0, -s[i]/s[0])]) for i in range(1, len(s)-1) if s[i]]
    word.append(affine(5, [(0, determinant-s[-1]*v[-1])] +
                       [(i, s[0]*v[i]) for i in range(1, 5)], pivot))
    word.append({'op': 'CHILD_C', 'fields': [0, 5],
                 'width': 'b=N/3', 'volume': 'V/3 on q'})
    word.extend(affine(i, [(0, s[i]/s[0])]) for i in range(1, 5) if s[i])
    word.append(affine(5, [(0, (determinant-s[0]*v[0])/pivot)] +
                       [(i, -v[i]/v[-1]) for i in range(1, 5)], -determinant/pivot))
    return word


def inverse_word(word):
    result = []
    for event in reversed(word):
        if event['op'] == 'CHILD_C':
            result.append(dict(event))
        else:
            d = F(event['diagonal'])
            result.append(affine(event['dst'], [(i, -F(c)/d) for i, c in event['terms']], 1/d))
    return result


def apply(address, word, modulus=None):
    z = list(address)
    spectators = z[6:]
    for event in word:
        if event['op'] == 'CHILD_C':
            require(event['fields'] == [0, 5], 'child endpoints')
            require(event['width'] == 'b=N/3' and event['volume'] == 'V/3 on q', 'child bill')
            z[0], z[5] = z[5], z[0]
        else:
            require(event['op'] == 'ORDERED_AFFINE', 'unknown ADDRESS event')
            dst = event['dst']
            d = F(event['diagonal'])
            require(bool(d) and all(0 <= i < dst for i, _ in event['terms']), 'ordered unit diagonal')
            x = d*z[dst]+sum(F(c)*z[i] for i, c in event['terms'])
            z[dst] = x if modulus is None else x.numerator*pow(x.denominator, -1, modulus) % modulus
    require(z[6:] == spectators, 'ADDRESS spectators')
    return tuple(z)


def matrix(word):
    columns = [apply([F(i == j) for i in range(6)], word) for j in range(6)]
    return [list(row) for row in zip(*columns)]


def execute(state, body, pullbacks):
    z = [row[:] for row in state]
    for event in body:
        if event['op'] == 'XOR':
            dst, src = event['dst'], event['src']
            z[dst] = [a ^ b for a, b in zip(z[dst], z[src])]
        else:
            require(event['op'] == 'QUERY', 'unknown BIT event')
            z[3] = [z[3][j] for j in pullbacks[event['kind']]]
    return z


def formula(state, pullback):
    z = [row[:] for row in state]
    for i, j in enumerate(pullback):
        z[0][i] = state[0][i] ^ state[3][i] ^ state[1][i] ^ state[3][j] ^ state[1][j]
        z[3][i] = state[3][j] ^ state[1][i] ^ state[1][j]
    return z


def prime_factors(n):
    n, factors, d = abs(n), set(), 2
    while d*d <= n:
        if n % d == 0:
            factors.add(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors


def check(program):
    u, t = list(map(F, [1, 0, 1])), list(map(F, [1, 0, -1]))
    s, r = u+[-x for x in u], t+[-x for x in t]
    g, gi = add(eye(3), outer(u, t), F(1, 2)), add(eye(3), outer(u, t), F(-1, 2))
    phi, phii = lift(g), lift(gi)
    word = lower(s, [x/4 for x in r])
    reverse = inverse_word(word)
    require(program['word'] == word and program['literal_ADDRESS_inverse'] == reverse, 'literal words')
    require(fractions(program['g_minus']) == g and fractions(program['gminus_inverse']) == gi, 'minus maps')
    require(fractions(program['Phi']) == phi and fractions(program['Phi_inverse']) == phii, 'lifted maps')
    require(matrix(word) == phi and matrix(reverse) == phii, 'exact ADDRESS multiplication')
    require(mm(g, gi) == eye(3) and mm(phi, phii) == eye(6), 'literal inverse')
    require(mm(g, g) != eye(3) and mm(phi, phi) != eye(6), 'non-involution control')
    require(mm(outer(u, t), outer(u, t)) == [[0]*3 for _ in range(3)], 'nilpotent rank-one part')
    reflections = []
    for actual, name, row in zip(program['reflection_pair'], ['R_Q', 'R_P'],
                                 [[F(3, 4), F(0), F(1, 4)], [F(1, 2), F(0), F(1, 2)]]):
        projector = outer(u, row)
        reflection = add(eye(3), projector, -2)
        body = lower(s, [-x for x in row]+row)
        require(actual['name'] == name and fractions(actual['P']) == projector, 'reflection projector')
        require(mm(projector, projector) == projector, 'idempotent projector')
        require(fractions(actual['R']) == reflection and fractions(actual['M']) == lift(reflection), 'reflection lift')
        require(actual['word'] == body and matrix(body) == lift(reflection), 'reflection word')
        require(mm(reflection, reflection) == eye(3), 'reflection involution')
        reflections.append((reflection, body))
    require(len(program['reflection_pair']) == 2, 'exactly two specified reflections')
    require(mm(reflections[1][0], reflections[0][0]) == g, 'R_P R_Q chronology')
    require(matrix(reflections[0][1]+reflections[1][1]) == phi, 'full baseline chronology')
    omitted = [e for e in word if e['op'] != 'CHILD_C']
    require(matrix(omitted) != phi, 'child omission negative control')
    bad = set()
    for body in [word, reverse]+[b for _, b in reflections]:
        require(sum(e['op'] == 'CHILD_C' for e in body) == 1, 'one child in each realization')
        require(sum(e['op'] == 'ORDERED_AFFINE' for e in body) == 6, 'six affines')
        for e in body:
            if e['op'] == 'ORDERED_AFFINE':
                d = F(e['diagonal'])
                bad |= prime_factors(d.numerator) | prime_factors(d.denominator)
                for _, c in e['terms']:
                    bad |= prime_factors(F(c).denominator)
    require(bad == {2}, 'exact bad-prime set')
    enc = [{'op': 'XOR', 'dst': 3, 'src': 1}, {'op': 'XOR', 'dst': 0, 'src': 3}]
    dec = list(reversed(enc))
    module = lambda kind: enc+[{'op': 'QUERY', 'kind': kind}]+dec
    expected = {'fused_BIT_module': module('g'), 'inverse_BIT_module': module('ginv'),
                'literal_unfused_pair': module('Q')+module('P'),
                'shared_chart_cancelled_pair': enc+[{'op': 'QUERY', 'kind': 'Q'}, {'op': 'QUERY', 'kind': 'P'}]+dec}
    for key, body in expected.items():
        require(program[key] == body, 'BIT chronology: '+key)
    checks, recovery = [], None
    for n in [5, 25, 7, 49]:
        seed = (1, 0, 0, 0, 0, 0, 11, 13)
        points = [tuple((seed[i]+k*pow(4, -1, n)*int(s[i])) % n for i in range(6))+(11, 13) for k in range(n)]
        require(len(set(points)) == n, 'full residue-ring orbit length')
        for k, address in enumerate(points):
            require(apply(address, word, n) == points[(k+1) % n], 'forward ADDRESS orbit')
            require(apply(address, reverse, n) == points[(k-1) % n], 'inverse ADDRESS orbit')
            require(apply(address, reflections[0][1], n) == points[(-3-k) % n], 'Q orbit')
            require(apply(address, reflections[1][1], n) == points[(-2-k) % n], 'P orbit')
        for j in range(6):
            v = tuple(int(i == j) for i in range(6))+(11, 13)
            require(apply(apply(v, word, n), reverse, n) == v, 'ADDRESS basis inverse and spectators')
        for j in [1, 4]:
            v = tuple(int(i == j) for i in range(6))
            require(apply(v, word, n) == v, 'fixed H1/D1 basis')
        require(any(apply(tuple(int(i == j) for i in range(6)), omitted, n) !=
                    apply(tuple(int(i == j) for i in range(6)), word, n) for j in range(6)), 'finite child omission')
        perms = {'g': [(k-1) % n for k in range(n)], 'ginv': [(k+1) % n for k in range(n)],
                 'Q': [(-3-k) % n for k in range(n)], 'P': [(-2-k) % n for k in range(n)]}
        for role in range(5):
            for k in range(n):
                state = [[0]*n for _ in range(5)]
                state[role][k] = 1
                result = execute(state, program['fused_BIT_module'], perms)
                require(result == formula(state, perms['g']), 'full dirty formula')
                require(execute(state, program['literal_unfused_pair'], perms) == result, 'literal unfused equality')
                require(execute(state, program['shared_chart_cancelled_pair'], perms) == result, 'cancelled baseline equality')
                require(execute(result, program['inverse_BIT_module'], perms) == state, 'retained dirty inverse')
                require(result[4] == state[4], 'VALUE spectator')
                identities = {key: list(range(n)) for key in perms}
                require(execute(state, program['fused_BIT_module'], identities) == state, 'whole identity query')
        fixed = (1, 2, 3, 1, 2, 3, 11, 13)
        require(apply(fixed, word, n) == tuple(x % n for x in fixed[:6])+fixed[6:], 'fixed ADDRESS point')
        for bits in range(16):
            state = [[(bits >> i) & 1] for i in range(4)]
            require(execute(state, program['fused_BIT_module'], {key: [0] for key in perms}) == state, 'fixed-point bits')
        if n == 5:
            entry = [[0]*n for _ in range(4)]
            entry[1][0] = 1
            out = execute(entry, program['fused_BIT_module'], perms)
            wiped = [row[:] for row in out]
            wiped[3] = [0]*n
            after = execute(wiped, program['inverse_BIT_module'], perms)
            require(out[0] == out[3] == [1, 1, 0, 0, 0], 'clean-entry output')
            require(after[0] == [0, 1, 0, 0, 1] and after[3] == [1, 0, 0, 0, 1], 'wipe loses DATA')
            require(after[:3] != entry[:3], 'early wipe forbidden')
            require(execute(out, program['fused_BIT_module'], perms) != entry, 'forward is not inverse')
            recovery = {'entry': entry, 'retained_forward_output': out, 'after_wipe_then_inverse': after}
        checks.append({'modulus': n, 'dirty_BIT_basis_columns': 4*n, 'VALUE_spectator_columns': n,
                       'ADDRESS_basis_columns': 6, 'fixed_point_BIT_assignments': 16})
    return {'status': 'PASS_EXACT_LOCAL_NATIVE_FUSION', 'bad_primes': sorted(bad),
            'rings': checks, 'total_dirty_BIT_columns': sum(x['dirty_BIT_basis_columns'] for x in checks),
            'total_VALUE_spectator_columns': sum(x['VALUE_spectator_columns'] for x in checks),
            'recovery_negative_control': recovery, 'fused_children': 1, 'specified_baseline_children': 2,
            'fused_affine_events': 6, 'baseline_serialized_affine_events': 12,
            'both_XOR_scans_after_chart_cancellation': 4,
            'child_width': 'N/3', 'child_volume': 'V/3 on q', 'three_DATA_plus_one_private_stock': '4/3',
            'private_initialization_volume': 'V/3', 'final_private_wipe_volume_after_completed_endpoint': 'V/3',
            'complete_DATA_c_or_C_supplier': False, 'kappa_claim': False, 'signed_VALUE_lift': False,
            'XOR_or_affine_optimality_claim': False, 'old_rho4_defined_on_half_integral_generator': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-results', action='store_true', help='regenerate deterministic results before freezing')
    args = parser.parse_args()
    result = check(json.loads((HERE/'PROGRAM.json').read_text()))
    encoded = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.write_results:
        (HERE/'RESULTS.json').write_text(encoded)
    else:
        require((HERE/'RESULTS.json').read_text() == encoded, 'recorded results differ')
        manifest = json.loads((HERE/'SHA256SUMS.json').read_text())
        require(set(manifest) == {'check.py', 'PROGRAM.json', 'PROOF.md', 'README.md', 'RESULTS.json', 'SOURCE-PINS.json'}, 'manifest file set')
        for name, expected in manifest.items():
            require(hashlib.sha256((HERE/name).read_bytes()).hexdigest() == expected, 'file hash: '+name)
    print(json.dumps({'status': result['status'], 'dirty_BIT_columns': result['total_dirty_BIT_columns'],
                      'VALUE_spectator_columns': result['total_VALUE_spectator_columns'],
                      'dependency_closed': True}, sort_keys=True))


if __name__ == '__main__':
    main()
