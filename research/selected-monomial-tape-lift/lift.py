"""Record-level realization of the f-column lift of the selected caller's monomials.

Model (SPECIALIZATION.md s2-s3, compact-control-movement.tex).  An address of a field with
f columns on n logical axes is X = (x_1, ..., x_f), x_j in F_2^n, plus arbitrary spectator
bits.  A monomial m = (G, b, Q, alpha, a) acts on one column as
    |x> -> i^(a + q(x)) |G x xor b>,    q(x) = sum_i alpha_i x_i + 2 sum_{i<j} Q_ij x_i x_j  (mod 4),
in the order diag(Q, alpha), perm(G), xgate(b), phase(a) of prune_native.monomial, and its
lift m^(tensor f) acts as
    |X> -> i^(a f + sum_j q(x_j)) |(G x_1 xor b, ..., G x_f xor b)>.

Tape records.  Every record acts on all f columns at once and never reads or writes a
spectator bit; each is one retained primitive type:
    XROW(i, k)   x_{j,i} ^= x_{j,k} for every column j      (compact-control selected-bit addition,
                                                               slots k -> i; movement-paid)
    NOT(i)       x_{j,i} ^= 1 for every column j             (selected-bit translation; movement-paid)
    S(i)         phase i^(sum_j x_{j,i})                       (unit-S phase record)
    CZ(i, k)     phase (-1)^(sum_j x_{j,i} x_{j,k})            (controlled-sign phase record)
    I            phase i^f                                     (global i record, lifted to i^f)
A row swap is three XROW records.  The record list of a monomial is independent of f.

This module builds the record list of a monomial by Gaussian elimination (the grammar of
SPECIALIZATION.md s2), executes it on explicit addresses with the phase accumulated modulo 4,
and compares with the lift formula; it also realizes 145-axis axis permutations (the plan's
J routes) as transposition chains of XROW records.  Standard library only.
"""
import importlib.util
import json
import random
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CAP = ROOT / "research/coupled-helper-neutral-completion/capsule/workspace"
NORM = CAP / "swarm-provider-audit-sol-high-20261024/agents/budget/inputs/NORMALIZERS.json"
PLAN = CAP / "swarm-coupled-caller-sol-high-20261024/agents/challenge/WHOLECALLER-PLAN-v1.json"
CLIFFORD = ROOT / "research/t74-native-fast/vendor/native/new/code/borrow/vendor/clifford/clifford_exact.py"
N9 = 9
N145 = 145


def load_clifford():
    spec = importlib.util.spec_from_file_location("tape_lift_clifford_exact", CLIFFORD)
    ce = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ce)
    return ce


# ------------------------------------------------------------------ monomials
def parity(x):
    return x.bit_count() & 1


def mv(rows, x):
    return sum(parity(r & x) << i for i, r in enumerate(rows))


def qvalue(Q, alpha, x, n):
    return (sum(alpha[i] for i in range(n) if x >> i & 1)
            + 2 * sum(parity((Q[i] >> (i + 1)) & (x >> (i + 1))) for i in range(n) if x >> i & 1)) % 4


class Monomial:
    def __init__(self, n, matrix_rows, offset, quadratic_rows, linear_Z4, phase):
        self.n = n
        self.G = tuple(matrix_rows)
        self.b = offset
        self.Q = tuple(quadratic_rows)
        self.alpha = tuple(linear_Z4)
        self.a = phase % 4
        assert len(self.G) == len(self.Q) == len(self.alpha) == n
        for i in range(n):
            assert self.alpha[i] % 2 == (self.Q[i] >> i) & 1, "Z4 linear parity equals the Q diagonal"
            for j in range(n):
                assert (self.Q[i] >> j) & 1 == (self.Q[j] >> i) & 1, "symmetric Q"

    @classmethod
    def from_recipe(cls, r, n=N9):
        return cls(n, r["matrix_rows"], r["offset"], r["quadratic_rows"], r["linear_Z4"], r["phase"])

    @classmethod
    def from_axis_permutation(cls, perm, n):
        """x -> x' with x'_{perm[i]} = x_i, i.e. axis i moves to axis perm[i] (a J route)."""
        rows = [0] * n
        for i, t in enumerate(perm):
            rows[t] |= 1 << i
        return cls(n, rows, 0, [0] * n, [0] * n, 0)

    def one_column(self, x):
        """(image address, phase mod 4) of one column."""
        return mv(self.G, x) ^ self.b, qvalue(self.Q, self.alpha, x, self.n)

    def lift(self, X, f):
        """(image, phase) of the lifted monomial on X = list of f column addresses."""
        img, ph = [], (self.a * f) % 4
        for x in X:
            y, p = self.one_column(x)
            img.append(y)
            ph = (ph + p) % 4
        return img, ph

    # -------------------------------------------------------------- the record grammar
    def records(self):
        """Record list realizing the monomial (f-independent).  Order of application:
        phase records on the input address, then the row operations of G, then translations,
        then the global i records."""
        n = self.n
        out = []
        for i in range(n):
            out += [("S", i)] * self.alpha[i]
        for i in range(n):
            for k in range(i + 1, n):
                if (self.Q[i] >> k) & 1:
                    out.append(("CZ", i, k))
        # Gaussian elimination of G to the identity; the reversed op list realizes G
        M = list(self.G)
        ops = []
        for col in range(n):
            piv = next(r for r in range(col, n) if (M[r] >> col) & 1)
            if piv != col:
                M[piv], M[col] = M[col], M[piv]
                ops.append(("SWAP", piv, col))
            for r in range(n):
                if r != col and (M[r] >> col) & 1:
                    M[r] ^= M[col]
                    ops.append(("XROW", r, col))        # row r ^= row col
        assert M == [1 << i for i in range(n)]
        for op in reversed(ops):
            if op[0] == "SWAP":
                _, i, k = op
                out += [("XROW", i, k), ("XROW", k, i), ("XROW", i, k)]
            else:
                out.append(op)
        for i in range(n):
            if (self.b >> i) & 1:
                out.append(("NOT", i))
        out += [("I",)] * self.a
        return out


def record_counts(recs):
    c = Counter(r[0] for r in recs)
    return {"XROW": c["XROW"], "NOT": c["NOT"], "S": c["S"], "CZ": c["CZ"], "I": c["I"],
            "movement_records": c["XROW"] + c["NOT"], "phase_records": c["S"] + c["CZ"] + c["I"], "total": len(recs)}


# ------------------------------------------------------------------ tape execution on addresses
def execute(recs, X, f, spectators):
    """Apply the record list to the f column addresses X (list of ints) with spectator bits.
    Returns (new X, phase mod 4, spectators) -- spectators are carried, never touched."""
    X = list(X)
    ph = 0
    for r in recs:
        t = r[0]
        if t == "XROW":
            _, i, k = r
            for j in range(f):
                X[j] ^= ((X[j] >> k) & 1) << i
        elif t == "NOT":
            i = r[1]
            for j in range(f):
                X[j] ^= 1 << i
        elif t == "S":
            i = r[1]
            ph = (ph + sum((X[j] >> i) & 1 for j in range(f))) % 4
        elif t == "CZ":
            _, i, k = r
            ph = (ph + 2 * sum(((X[j] >> i) & 1) & ((X[j] >> k) & 1) for j in range(f))) % 4
        elif t == "I":
            ph = (ph + f) % 4
        else:
            raise ValueError(r)
    return X, ph, spectators


def check_monomial(m, f, addresses, spectator_bits=3, rng=None):
    """Execute the record list on the given column-address tuples and compare with the lift."""
    recs = m.records()
    rng = rng or random.Random(0)
    for X in addresses:
        spec = rng.getrandbits(spectator_bits)
        got_X, got_ph, got_spec = execute(recs, X, f, spec)
        want_X, want_ph = m.lift(X, f)
        if got_X != want_X or got_ph != want_ph or got_spec != spec:
            return False, {"X": X, "got": (got_X, got_ph), "want": (want_X, want_ph)}
    return True, record_counts(recs)


def all_addresses(n, f):
    N = 1 << n
    if f == 1:
        return [[x] for x in range(N)]
    if f == 2:
        return [[x, y] for x in range(N) for y in range(N)]
    raise ValueError("exhaustive only for f <= 2")


def random_addresses(n, f, count, seed):
    rng = random.Random(seed)
    return [[rng.getrandbits(n) for _ in range(f)] for _ in range(count)]


# ------------------------------------------------------------------ inventory of the selected caller
def wrappers():
    nz = json.loads(NORM.read_text(encoding="utf-8"))
    out = []
    for p, port in enumerate(nz["ports"]):
        for name, w in sorted(port["compiled_wrappers"].items()):
            out.append((f"port{p}:{name}", Monomial.from_recipe(w["recipe"])))
    return out


def central_elements(ce):
    """C0 = cgate on axis 0 and X0 = xgate on axis 0 are not monomials in prune_native's sense
    (cgate is a rank-one Gaussian); only X0 is a translation record.  We return X0 and the
    diagonal unit-S / Z elements used by the plan (phase records)."""
    return [("X0", Monomial(N9, [1 << i for i in range(N9)], 1, [0] * N9, [0] * N9, 0))]


def plan_words():
    """The 145-axis J routes of WHOLECALLER-PLAN-v1: for every main/helper/idle target its literal
    pre_word and post_word (lists of SWAP_BITS events), the declared permutation and inverse,
    and whether a central X follows the LEFT boundary (the correction of a negative Q power)."""
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    out = []
    for kind in ("main_targets", "helper_targets", "idle_jobs"):
        for idx, t in enumerate(plan[kind]):
            for key in ("pre_word", "post_word"):
                assert all(ev[0] == "SWAP_BITS" and len(ev) == 3 for ev in t[key]), (kind, idx, key)
            assert t["affine_translation"] == [] and t["absolute_phase"] == 0, "J routes are plain permutations"
            out.append({"name": f"{kind}[{idx}] rank {t['rank']}", "kind": kind, "pre": t["pre_word"], "post": t["post_word"],
                        "perm": tuple(t["permutation"]), "inv": tuple(t["inverse_permutation"]),
                        "central_X": bool(t.get("central_X_after_LEFT", False))})
    return out


def swap_records(word):
    """SWAP_BITS(i, k) is the row swap of axes i and k: three XROW records."""
    recs = []
    for _, i, k in word:
        recs += [("XROW", i, k), ("XROW", k, i), ("XROW", i, k)]
    return recs


def check_word(word, perm, inv, f, count, seed, n=N145):
    """Execute the literal SWAP_BITS word as XROW records and identify which declared axis
    permutation it realizes (the plan's `permutation` or `inverse_permutation`).
    Returns (ok, convention, record counts)."""
    recs = swap_records(word)
    cands = {"permutation": Monomial.from_axis_permutation(perm, n), "inverse_permutation": Monomial.from_axis_permutation(inv, n)}
    rng = random.Random(seed)
    alive = set(cands)
    for X in random_addresses(n, f, count, seed):
        spec = rng.getrandbits(3)
        got_X, got_ph, got_spec = execute(recs, X, f, spec)
        if got_spec != spec or got_ph != 0:
            return False, None, None
        for c in list(alive):
            if cands[c].lift(X, f) != (got_X, 0):
                alive.discard(c)
        if not alive:
            return False, None, None
    conv = sorted(alive)
    return True, conv, record_counts(recs)


def transposition_chain(perm):
    """Transpositions (i, k) whose product (applied left to right as axis swaps) is perm."""
    n = len(perm)
    content = list(range(n))      # content[pos] = original axis whose bit now sits at pos
    where = list(range(n))        # where[axis] = its current position
    out = []
    for t in range(n):
        s_axis = perm.index(t)    # output position t must hold original axis s_axis
        s = where[s_axis]
        if s != t:
            a, b = content[s], content[t]
            content[s], content[t] = b, a
            where[a], where[b] = t, s
            out.append((s, t))
    assert all(where[i] == perm[i] for i in range(n))
    return out


def permutation_records(perm):
    recs = []
    for i, k in transposition_chain(perm):
        recs += [("XROW", i, k), ("XROW", k, i), ("XROW", i, k)]
    return recs


def check_permutation(perm, f, count, seed):
    n = len(perm)
    m = Monomial.from_axis_permutation(perm, n)
    recs = permutation_records(perm)
    rng = random.Random(seed)
    for X in random_addresses(n, f, count, seed):
        spec = rng.getrandbits(3)
        got_X, got_ph, got_spec = execute(recs, X, f, spec)
        want_X, want_ph = m.lift(X, f)
        if got_X != want_X or got_ph != want_ph or got_spec != spec:
            return False, None
    return True, record_counts(recs)
