# Validation and limits

Author execution: macOS arm64, CPython3.12, base
32890bc5de034ab8fc93ac88ead7279a6a416d04. No new dependencies.

The initial P8 fixture allowed the rounded consumer to equal its RHS. Before
publication it was strengthened to P16/w32, and a bypass-consumer control now
requires a real change. The full three-case source-bound replay passed in
5.41seconds before the final head/lease controls; that observation is not a
physical tape speed or a portable runtime guarantee. The final receipt includes
all final controls. A module-name collision with the inherited `layout` was
resolved by the specific `rhs_layout` name. A checker initially compared entire
retained output capacity with logical input length; it now compares logical
bodies and independently requires all retained work backing to be erased.

Executed so far:

- `python3.12 -I -B research/physical-boundary-rhs-caller/verify.py --write`
- `python3.12 -B scripts/research_package.py --package research/physical-boundary-rhs-caller --check-only`

All three actual calls and final source/control checks passed. Registered
normal/optimized replay and committed export results are recorded in the next
reproducibility update. No hosted CI, production Gaussian preparation, full
Core second-pass integration, selected-frontier replay or formal proof kernel
has run. No inherited numerical theorem is independently accepted by this note.
