# Exact reachable-subspace pruning

OpenAI QuantumCircuit/PruningConstruction.lean proves reflect_action_error: the effect of deleting a reflection is exactly twice the norm of the projected state. Its constructive pruning proof composes local errors. We use only its zero-error specialization, not approximate pruning on arbitrary inputs.

For a linear register circuit, let R_i map all independent initial columns to the state immediately before a recursive gate U_i. If (U_i-I) R_i = 0, replacing that gate by identity preserves the current reachable state for every initial input. Induction through the unchanged suffix proves the same complete endpoint. Every private state and dirty input is included; a clean-input check alone is insufficient. A particularly cheap sufficient case is an identically zero operand row for a linear recursive gate. No recursive child is charged for that zero operand, but ordinary initialization and clearing operations remain paid.

The native C++ pilot propagates every one of 800 independent logical input columns modulo 2^61-1 through both emitted programs and inspects all 3,701 positive child sites per orientation, including private centres. All coefficients are dyadic; reduction is well-defined. A nonzero modular column disproves an identically zero rational row. No zero candidates occurred. This rules out only the zero-operand specialization on this fixed word, not the full invariant-subspace criterion or approximate quantum pruning. No kappa gain is credited.

This is an exact sufficient circuit rule derived from a different OpenAI proof family than Newton interpolation, rational Schur elimination and min-cut scheduling. Source inspection is not a new Lean audit. The more general fixed-subspace condition still needs an actual all-input witness; it is not assumed to hold.

Follow-up on the selected 99-pivot program: all 3,700 positive child sites in each orientation were screened with the same modular criterion, again with zero candidates. The earlier 3,701-site pilot above used the preceding 92-pivot word. The delivered PRUNING-SCREEN.json binds this new program.
