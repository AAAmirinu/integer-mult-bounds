# Fused dyadic compression halos

This layout prepares the retained bulk Gaussian compression as complete
binary halo boxes. It uses dyadic side L, core stride C=L-2A, and a binary
main coarse range t_i/L. The main tensor has exactly T records and can use
the existing arbitrary-source bit router. Tail and periodic-wrap tiles
are gathered and repaired through a sparse, explicitly charged sort/join.

A fused input iterator replaces separate axis-by-axis halo passes. Its
actual input-head travel is below 4T under the stated overlap cutoff,
including the final rewind. At the chosen eventual parameters, the bad
tile volume is below T/p^5, so polynomial per-record repair is absorbed.
The output uses an inverse binary field permutation, fused padding removal
and an ordered merge; the full main tensor is never sorted.

**No new kappa is claimed.** The main-box Gaussian arithmetic remains a
separate obligation. This removes a layout/padding obstacle to joint-axis
work; it does not supply a joint-axis Gaussian solver. Expansion is outside
this package. See [PROOF.md](PROOF.md) for the conditional tape and analytic
transfer and its remaining assumptions.

```sh
python -B research/fused-dyadic-halos/verify.py /absolute/new/output
```

Finite checks compare explicit source-head trajectories with an exact
Cartesian variation formula, reconstruct complete operators on unequal
source/target shapes, and reject broken wrap/tail/merge/stride variants.
The local operator fixture is a periodic three-point contraction with
nearest-index selection, **not a Gaussian inverse**. Huge tensor census
cases use exact counts without executing those tensors and are labeled so.

The source phase-cell/microbox construction, normalization and router are
inherited from the retained RaD/hipotures reports and their cited work.
New fused layout, sparse repair, accounting and controls by chafreaky with
OpenAI Codex assistance. Apache-2.0.
