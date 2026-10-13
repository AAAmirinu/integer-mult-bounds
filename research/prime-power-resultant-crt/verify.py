#!/usr/bin/env python3
"""Independent exact reconstruction of the PR621 Sylvester identity.

Python >= 3.9, standard library only. No predecessor verifier is imported.
Finite-field evaluation and bounded CRT reconstruct integer coefficients;
integer polynomial arithmetic checks Bezout, and Bareiss checks the norm.
"""

import argparse
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RADICES = (3, 4, 5, 7, 8, 9, 11, 16, 25, 27)
SEED = 83


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":"),
                                     sort_keys=True).encode()).hexdigest()


def prime(value):
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    return all(value % d for d in range(3, isqrt(value) + 1, 2))


def prime_power(radix):
    require(radix >= 3, "radix must be at least three")
    ell = next(d for d in range(2, radix + 1) if radix % d == 0)
    rest = radix
    while rest % ell == 0:
        rest //= ell
    require(rest == 1, "radix is not a prime power")
    return ell


def split_primes(radix, seed):
    candidate = 1 + radix * ((1_000_000 + 997 * seed) // radix)
    while True:
        if prime(candidate):
            yield candidate
        candidate += radix


def primitive_root(radix, modulus):
    ell = prime_power(radix)
    require(prime(modulus) and (modulus - 1) % radix == 0,
            "field does not split the cyclotomic polynomial")
    for base in range(2, modulus):
        omega = pow(base, (modulus - 1) // radix, modulus)
        if pow(omega, radix // ell, modulus) != 1:
            require(pow(omega, radix, modulus) == 1, "wrong root order")
            return omega
    raise ValueError("no primitive root found")


def kernels(radix, omega, modulus, conjugate=True):
    # Tail products, evaluated independently in F_modulus.
    def tail(root):
        result = [1] * radix
        for j in range(radix - 2, -1, -1):
            result[j] = result[j + 1] * (1 - pow(root, j + 1, modulus)) % modulus
        require(result[0] == radix % modulus, "tail product is not radix")
        return result

    f = tail(omega)
    reverse_root = pow(omega, -1, modulus) if conjugate else omega
    return f, list(reversed(tail(reverse_root)))


def sylvester(f, star, modulus):
    n = len(f) - 1
    require(len(star) == n + 1 and n > 0, "invalid polynomial degrees")
    matrix = [[0] * (2 * n) for _ in range(2 * n)]
    for coefficients, start in ((f, 0), (star, n)):
        for offset in range(n):
            for degree, value in enumerate(coefficients):
                matrix[degree + offset][start + offset] = value % modulus
    return matrix


def elimination(matrix, modulus, rhs=None):
    """Row elimination; return determinant and, when nonsingular, solution."""
    a = [[value % modulus for value in row] for row in matrix]
    size = len(a)
    b = None if rhs is None else [value % modulus for value in rhs]
    determinant = 1
    for col in range(size):
        pivot = next((row for row in range(col, size) if a[row][col]), None)
        if pivot is None:
            return 0, None
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            if b is not None:
                b[col], b[pivot] = b[pivot], b[col]
            determinant = -determinant
        pivot_value = a[col][col]
        determinant = determinant * pivot_value % modulus
        inverse = pow(pivot_value, -1, modulus)
        for row in range(col + 1, size):
            scale = a[row][col] * inverse % modulus
            if scale:
                for j in range(col + 1, size):
                    a[row][j] = (a[row][j] - scale * a[col][j]) % modulus
                if b is not None:
                    b[row] = (b[row] - scale * b[col]) % modulus
            a[row][col] = 0
    if b is None:
        return determinant % modulus, None
    solution = [0] * size
    for row in range(size - 1, -1, -1):
        solution[row] = ((b[row] - sum(a[row][j] * solution[j]
                                     for j in range(row + 1, size)))
                         * pow(a[row][row], -1, modulus)) % modulus
    return determinant % modulus, solution


def determinant_and_adjugate(matrix, modulus):
    size = len(matrix)
    determinant, solution = elimination(matrix, modulus, [1] + [0] * (size - 1))
    if solution is not None:
        column = [determinant * value % modulus for value in solution]
    else:
        # A vanishing split-prime determinant is retained, never skipped.
        column = []
        for col in range(size):
            minor = [[value for j, value in enumerate(row) if j != col]
                     for row in matrix[1:]]
            cofactor, _ = elimination(minor, modulus)
            column.append((-1 if col % 2 else 1) * cofactor % modulus)
    require(all(sum(value * cofactor for value, cofactor in zip(row, column)) % modulus
                == (determinant if i == 0 else 0)
                for i, row in enumerate(matrix)), "finite-field adjugate identity")
    return determinant, column


def interpolate(points, values, modulus):
    """Lagrange interpolation, without a polynomial/field library."""
    size = len(points)
    require(len(values) == size and len(set(points)) == size, "bad interpolation data")
    result = [0] * size
    for i, point in enumerate(points):
        basis, denominator = [1], 1
        for j, other in enumerate(points):
            if i == j:
                continue
            nxt = [0] * (len(basis) + 1)
            for k, value in enumerate(basis):
                nxt[k] = (nxt[k] - other * value) % modulus
                nxt[k + 1] = (nxt[k + 1] + value) % modulus
            basis = nxt
            denominator = denominator * (point - other) % modulus
        scale = values[i] * pow(denominator, -1, modulus) % modulus
        for k, value in enumerate(basis):
            result[k] = (result[k] + scale * value) % modulus
    require(all(evaluate(result, point, modulus) == value % modulus
                for point, value in zip(points, values)), "interpolation identity")
    return result


def evaluate(coefficients, point, modulus):
    value = 0
    for coefficient in reversed(coefficients):
        value = (value * point + coefficient) % modulus
    return value


def crt_update(coefficients, total_modulus, residues, modulus):
    require(len(coefficients) == len(residues) and gcd(total_modulus, modulus) == 1,
            "bad CRT input")
    inverse = pow(total_modulus, -1, modulus)
    return [old + total_modulus * ((new - old) * inverse % modulus)
            for old, new in zip(coefficients, residues)]


def center(coefficients, modulus, bound):
    require(modulus > 2 * bound, "CRT modulus does not establish uniqueness")
    result = [value if value <= modulus // 2 else value - modulus
              for value in coefficients]
    require(all(abs(value) <= bound for value in result), "CRT coefficient bound violated")
    return result


def reduce_integer(coefficients, radix):
    ell = prime_power(radix)
    step, degree = radix // ell, radix - radix // ell
    result = list(coefficients) + [0] * max(0, degree - len(coefficients))
    for high in range(len(result) - 1, degree - 1, -1):
        value = result[high]
        if value:
            for j in range(ell):
                result[high - degree + j * step] -= value
    return result[:degree]


def multiply_integer(left, right, radix):
    result = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        if x:
            for j, y in enumerate(right):
                result[i + j] += x * y
    return reduce_integer(result, radix)


def conjugate_integer(coefficients, radix):
    result = [0] * radix
    for i, value in enumerate(coefficients):
        result[-i % radix] += value
    return reduce_integer(result, radix)


def integral_kernels(radix):
    degree = radix - radix // prime_power(radix)
    one = [1] + [0] * (degree - 1)
    f = [None] * radix
    f[-1] = one
    for j in range(radix - 2, -1, -1):
        factor = [1] + [0] * (j + 1)
        factor[-1] -= 1
        f[j] = multiply_integer(f[j + 1], factor, radix)
    require(f[0] == [radix] + [0] * (degree - 1), "integer product is not radix")
    return f, [conjugate_integer(value, radix) for value in reversed(f)]


def check_bezout(radix, resultant, column):
    f, star = integral_kernels(radix)
    n, degree = radix - 1, len(resultant)
    require(len(column) == 2 * n, "wrong cofactor count")
    output = [[0] * degree for _ in range(2 * n)]
    for coefficients, start in ((f, 0), (star, n)):
        for offset in range(n):
            for power, value in enumerate(coefficients):
                product = multiply_integer(value, column[start + offset], radix)
                output[power + offset] = [x + y for x, y in
                                          zip(output[power + offset], product)]
    require(output == [resultant] + [[0] * degree for _ in range(2 * n - 1)],
            "integer Bezout identity failed")


def bareiss(matrix):
    """Fraction-free determinant over Z; exact division is checked."""
    a = [list(row) for row in matrix]
    size = len(a)
    if not size:
        return 1
    previous, sign = 1, 1
    for col in range(size - 1):
        pivot = next((row for row in range(col, size) if a[row][col]), None)
        if pivot is None:
            return 0
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            sign = -sign
        diagonal = a[col][col]
        for row in range(col + 1, size):
            for j in range(col + 1, size):
                numerator = diagonal * a[row][j] - a[row][col] * a[col][j]
                quotient, remainder = divmod(numerator, previous)
                require(remainder == 0, "Bareiss division was not exact")
                a[row][j] = quotient
            a[row][col] = 0
        previous = diagonal
    return sign * a[-1][-1]


def integer_norm(coefficients, radix):
    degree = len(coefficients)
    columns = [reduce_integer([0] * shift + coefficients, radix)
               for shift in range(degree)]
    return bareiss([[columns[col][row] for col in range(degree)]
                    for row in range(degree)])


def check_case(radix, seed):
    ell = prime_power(radix)
    n, degree = radix - 1, radix - radix // ell
    powers = [power for power in range(1, radix) if gcd(power, radix) == 1]
    require(len(powers) == degree, "embedding count")
    # PROOF.md derives this bound for every canonical coefficient of R
    # and adj(S)e_0, under every prime-power choice.
    bound = 2 * ((1 << radix) - 1) ** (2 * n)
    count = (1 + 2 * n) * degree
    coefficients, total_modulus = [0] * count, 1
    transcript, modular_norms = [], []
    for modulus in split_primes(radix, seed):
        omega = primitive_root(radix, modulus)
        points = [pow(omega, power, modulus) for power in powers]
        evaluations = []
        for point in points:
            f, star = kernels(radix, point, modulus)
            determinant, column = determinant_and_adjugate(sylvester(f, star, modulus), modulus)
            evaluations.append([determinant] + column)
        residues = []
        for slot in range(1 + 2 * n):
            residues.extend(interpolate(points, [values[slot] for values in evaluations], modulus))
        coefficients = crt_update(coefficients, total_modulus, residues, modulus)
        total_modulus *= modulus
        modular_norm = 1
        for values in evaluations:
            modular_norm = modular_norm * values[0] % modulus
        modular_norms.append((modulus, modular_norm))
        transcript.append({"prime": modulus, "root": omega,
                           "evaluations_sha256": digest(evaluations),
                           "interpolated_sha256": digest(residues)})
        if total_modulus > 2 * bound:
            break
    centered = center(coefficients, total_modulus, bound)
    vectors = [centered[i:i + degree] for i in range(0, count, degree)]
    resultant, column = vectors[0], vectors[1:]
    require(any(resultant), "zero resultant")
    require(conjugate_integer(resultant, radix) == resultant, "resultant is not real")
    require(sum(resultant) % ell == (-1) ** (n * n) % ell, "prime-ideal residue")
    check_bezout(radix, resultant, column)
    norm = integer_norm(resultant, radix)
    require(norm > 0 and isqrt(norm) ** 2 == norm, "norm is not a positive square")
    require(all(norm % modulus == residue for modulus, residue in modular_norms),
            "integer norm disagrees with split embeddings")
    print("PASS radix", radix, "embeddings", degree, "CRT primes", len(transcript), flush=True)
    return {"radix": radix, "prime": ell, "primitive_powers": powers,
            "resultant": [str(value) for value in resultant],
            "resultant_norm": str(norm), "real_norm_absolute": str(isqrt(norm)),
            "bezout_coefficients_sha256": digest(column), "bezout_identity": True,
            "coefficient_bound": str(bound), "crt_modulus": str(total_modulus),
            "split_prime_transcript": transcript}, (resultant, column)


def rejected(function, message):
    try:
        function()
    except ValueError:
        return message
    raise ValueError("negative control accepted: " + message)


def controls(case_data):
    resultant, column = case_data
    wrong = list(resultant)
    wrong[0] += 1
    wrong_column = [list(value) for value in column]
    wrong_column[0][0] += 1
    checks = [rejected(lambda: center([1], 7, 4), "insufficient_CRT_modulus"),
              rejected(lambda: center([5], 23, 4), "CRT_coefficient_out_of_bound"),
              rejected(lambda: prime_power(6), "non_prime_power_radix"),
              rejected(lambda: primitive_root(5, 7), "nonsplit_field"),
              rejected(lambda: check_bezout(5, wrong, column), "changed_resultant"),
              rejected(lambda: check_bezout(5, resultant, wrong_column), "changed_cofactor")]
    modulus = next(split_primes(5, SEED))
    omega = primitive_root(5, modulus)
    f, star = kernels(5, omega, modulus)
    good, _ = determinant_and_adjugate(sylvester(f, star, modulus), modulus)
    _, bad_star = kernels(5, omega, modulus, conjugate=False)
    bad, _ = determinant_and_adjugate(sylvester(f, bad_star, modulus), modulus)
    require(good != bad, "missing-conjugation control was vacuous")
    checks.append("missing_conjugation_changes_resultant")
    unit = [-1, 0, 0, 1]
    unit_star = [1, 0, 0, -1]
    det, cofactors = determinant_and_adjugate(sylvester(unit, unit_star, modulus), modulus)
    require(det == 0 and len(cofactors) == 6, "unit-circle singular control")
    checks.append("unit_circle_common_root_is_singular")
    return checks


def source_bindings():
    manifest = json.loads((HERE / "SOURCE.json").read_text())
    for relative, expected in manifest["files"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, "source pin mismatch: " + relative)
    return manifest


def run():
    source = source_bindings()
    cases, data = [], {}
    for radix in RADICES:
        receipt, internals = check_case(radix, SEED)
        cases.append(receipt)
        data[radix] = internals
    # Compare all eight predecessor examples, including nontrivial powers.
    expected = json.loads((ROOT / "research/prime-power-cyclic-inverse/EXPECTED.json").read_text())
    comparisons = []
    for old in expected["cases"]:
        radix, power = old["radix"], old["primitive_power"]
        values = data[radix][0]
        substituted = [0] * radix
        for degree, value in enumerate(values):
            substituted[degree * power % radix] += value
        actual = reduce_integer(substituted, radix)
        require(actual == list(map(int, old["resultant"])), "predecessor resultant mismatch")
        current = next(case for case in cases if case["radix"] == radix)
        require(current["resultant_norm"] == old["resultant_norm"], "predecessor norm mismatch")
        comparisons.append([radix, power])
    return {"status": "PASS_INDEPENDENT_BOUNDED_INTEGER_CRT", "assignment_seed": SEED,
            "base_commit": source["base_commit"], "cases": cases,
            "primitive_embeddings_checked": sum(len(case["primitive_powers"]) for case in cases),
            "predecessor_exact_matches": comparisons, "negative_controls": controls(data[5]),
            "scope": "Finite determinant, adjugate/Bezout, prime-ideal residue and integer norm identities; no uniform theorem, paid program or kappa claim."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = run()
    rendered = json.dumps(result, indent=2) + "\n"
    if args.check:
        # JSON's bool/int and float/int distinctions matter to a certificate.
        require(digest(json.loads(args.check.read_text())) == digest(result), "receipt mismatch")
    if args.output:
        require(not args.output.exists(), "output already exists")
        args.output.write_text(rendered)
    print("PASS", result["primitive_embeddings_checked"], "primitive embeddings;",
          len(result["predecessor_exact_matches"]), "predecessor matches;",
          len(result["negative_controls"]), "negative controls")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print("FAIL:", error, file=sys.stderr)
        raise SystemExit(1)
