# Nine XORs are necessary and sufficient

This contribution was produced by Nick Petalas. Apache-2.0.

## Endpoint and alphabet

There are five registers containing independent arbitrary vectors over F2.
Register indices are zero-based. The only paid instruction is
`r_dst += r_src`, with distinct source and destination. Each instruction costs
one. The requested complete output is

```
y_i = x_i + x_(i+1 mod 5) + x_(i+2 mod 5),   0 <= i < 5.
```

No workspace, free permutation, basis change, initialization, erasure or
nonlinear/data-dependent instruction is allowed. The endpoint coefficient
matrix has row masks `(7,14,28,25,19)`, with bit j denoting input x_j.

## Attainment

The following ordered word has nine instructions. The left index is the
source; the right index is the destination.

```
0 -> 2
0 -> 4
3 -> 0
4 -> 3
1 -> 4
0 -> 1
2 -> 1
1 -> 0
3 -> 2
```

Literal substitution of symbolic row masks gives the required matrix. The
verifier also executes this word on all 32 independent scalar bit inputs.
These scalar inputs exhaust F2^5 and include a basis. A linear identity on
this basis holds on arbitrary vector payloads, coordinatewise. The word is
invertible because every instruction is an involution; reversing it recovers
all five arbitrary inputs. Thus nine is an upper bound.

## Exhaustive lower bound

Encode a 5-by-5 binary matrix by its five consecutive five-bit rows in a
25-bit unsigned integer. A directed addition from s to d changes the state
by XORing the s-th row into the d-th row. This is exactly `step` in verify.py.
There are twenty distinct allowed gates. They are all involutions.

For a center M, define B_0(M)={M}. Iteratively form all twenty neighbors of
every matrix at exact distance k, discard matrices seen at smaller distance,
and retain the new matrices as layer k+1. Induction on k proves that this
algorithm enumerates every state reachable by at most k+1 instructions:
a word of positive length consists of a shorter word followed by an allowed
gate. Discarding a repeated state cannot remove a shorter path or its possible
continuations. No length ordering, pivot heuristic or symmetry quotient prunes
the search. The domain has at most 2^25 matrices.

The exact layer sizes through radius four are

```
center                  radius 0   1    2     3      4    total
identity                       1  20  260  2570  19680    22531
target (7,14,28,25,19)          1  20  260  2570  19680    22531
```

The two complete balls have empty intersection. These counts and the empty
intersection are enumerated afresh by the standalone verifier, rather than
accepted from a saved search report.

If a word of length l<=8 connected the identity to the target, cut it after
min(l,4) gates. Its intermediate matrix would lie within four gates of the
identity. It would also lie within four gates of the target, by reversing
the remaining involutions. It would therefore belong to both balls, a
contradiction. Thus the minimum is at least nine. Together with the explicit
word, the exact minimum is nine.

This is a finite computer-assisted certificate with a written reduction to
arbitrary vector inputs. The exhaustive enumeration and its Python execution
are trusted; no proof kernel or independent human review is claimed.

## Checks and boundaries

A separate literal bit interpreter checks every input, full input recovery,
and a counterexample after deletion of each of the nine instructions. It does
not use the packed-matrix update to compute the truth table. An eight-gate
prefix of the witness supplies a positive control for the neighborhood method:
its known four-gate midpoint belongs to both radius-four balls. Nine malformed
input/program controls reject. All checks use explicit exceptions under -O.

The result is a scalar binary linear-circuit minimum. It is not a native
operator identity with phases, a physically priced adapter, a recursive paid
child minimum, a new kappa or a complete multiplication theorem. Ali Romman's
PR #5793 supplies the related bounded synthesis interface and its four-role
limit, cited as motivation. No predecessor executable or certificate is
imported, rechecked or modified. Classical shortest paths and the
meet-in-the-middle argument retain their usual mathematical credit. Global
literature priority for this endpoint is unclaimed.
