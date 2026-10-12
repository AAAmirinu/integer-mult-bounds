# Observable slicing and allocation-aware circuit retirement on 112 ports

Conditional **kappa = 0.001467978682990812**, exactly `366994670747703/250000000000000000`. This is **4.674157% above our previous checked deliverable** and **0.046974% above the frozen PR473 ranksector112 candidate**. The complex supplier binds at `735068406246315949703/500000000000000000000000`; the unchanged cited PR493 bit supplier is `391360506745414227149/250000000000000000000000`.

The new contribution is joint response-circuit selection and physical reallocation. Retiring seven pivots makes some helpers wider but removes costly entrance work. A literal map pays for all 504 extra residual axes across 72 complete calls. Exact observable slicing removes another 420 scalar instructions, with no separate exponent credit. PR523's eight-port restriction and PR473's 112-port integration are credited and reused.

Four mathematical construction lemmas are proved in `proof/` and applied by the verifier:

1. Closed response-circuit retirement with an exact histogram/stock identity.
2. Reversible observable slicing, preserving every arbitrary dirty input.
3. Isolated-register restriction, retaining prefix semantics and restoration.
4. Colored whole-owner exchange and provider transfer, with every residual axis paid.

These are proofs written for this composition, not claims of four globally novel identities or four independent kappa gains. No new Lean certification is claimed. The complete result retains the inherited all-size compiler, common-label/mutable-basis transport, normalized Lemma A realization, restored-row, precision/tape and analytic-transfer interfaces.

## Reproduce

Python 3.11 or later, standard library only, assertions enabled:

```text
python -B verify.py --work /absolute/path/to/a-new-output-directory
```

Choose a new output directory outside the package. The 27-stage pipeline reconstructs the changed 120-port source, removes observationally dead writes, restricts to 112 ports, rebuilds actual orthogonal charts and whole owners, independently recounts the physical invoice, and runs two exact moment engines and all 47 strict outer inequalities. Both `MANIFEST.json` and `EXPECTED.json` are required. No network, search optimizer, compiler or Lean is needed.

All 560 dirty helpers remain. There are 40,320 helper uses and 16,128 pending bins; live stock is 7,168, physical stock 7,738, maximum rank 73 and deficit 2,560. The complete global histogram is `{'1': 176472, '2': 13104, '3': 40938, '4': 6336, '5': 20406, '6': 9216, '7': 132, '8': 72, '48': 230}`. Canonical template SHA-256: `59138bef1f8e23fb5f1b1692b137dbae801f51667da142973f7ec393f8b4c1dd`.

Generated gzip uses fixed level 9, timestamp zero and OS byte 255; text hashes normalize CRLF/LF only. `vendor/base120` is frozen historical ancestry with one documented launcher adaptation. Its old README, results and manifest describe the ancestor, not this derivative; the root manifest and root verifier are authoritative. The unchanged bit operator is a pinned dependency whose histogram is repriced, not redundantly reconstructed.

The public snapshot is frozen through PR525, including updated PR473. No later proposal is covered by the comparison. See `SOURCES.json`, `ADAPTATIONS.md`, `RESEARCH.md` and `evidence/`. Nothing publishes or changes GitHub.
