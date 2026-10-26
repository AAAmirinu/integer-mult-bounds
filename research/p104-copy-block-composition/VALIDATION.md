# Validation record

CPython 3.12.14 on macOS arm64, standard library only, no subagents.
Canonical main is de5ec2e7a6074068452f45b1a191b5c72832df4a, priority revision 8.
The final immediate source is PR5786 at
6b936acd68a7e0f9062037900f0fe9bc4b6fdd25. Its complete frozen export and all
nested source inventories are authenticated before source imports.

The final full primary replay passed. The four registered commands then passed
in 438.77 seconds: normal and optimized full replay, followed by normal and
optimized exact scalar-transfer checks. The full replay checks all 795 input
columns and 632025 endpoint coefficients, separate transpose columns, 27 owned
lifetimes, peak 13 live owned fields, 2924 distinct native maps with absolute
phases, 208 main adapters, 1124 helper normalizers and the complete physical
caller. Both rational moment engines, completion, compiler, all 54 strict outer
rows and four functional conditions pass. Nine changed-word/caller/invoice
controls and the native phase control reject.

The compatibility proof checks all eight original R22 edits, including exact
9-by-9 and 2-by-2 rational scalar transfers. All 23 COPY events retain their
logical source values, including the 13 retained native copies. A wrong scalar
coefficient rejects. Three actual byte corruptions of the final direct sources
and PR5786 archive reject before imports; see SOURCE-CONTROLS.json.

Commands:

```
python3.12 -B scripts/research_package.py --package research/p104-copy-block-composition
python3 -B scripts/research_package.py --package research/p104-copy-block-composition --check-only
git diff --check
```

The final checks establish conditional kappa .00312277313. The raw ceiling is
strictly inside (.00312277315303,.00312277315304). The selected frontier stays
unchanged. The five framework assumptions remain. No large uniform word or
rounded multiplier is materialized. Hosted CI and independent scientific review
are separate and remain pending.

The earlier PR5774 composition is retained at
8f4a012d9171971837fef8949b1eedb60beacc64, with conditional kappa .00312204390.
Its normal/optimized full replay passed in 288.13 seconds. It is a superseded
checkpoint of this investigation, not a separate contribution. Frozen sources
remain byte-exact. The optional full-history ancestry preflight is unavailable
in this shallow checkout; no automatic full-history download was attempted.
