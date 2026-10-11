# Constructive pending-factor transport and deferred terminal suffixes

## Sufficient retiming identity

Let X_v be translation by v on a finite F2 address space, and C_v=((1+i)I+(1-i)X_v)/2. Direct expansion gives C_v C_w=C_w C_v and C_v^2=X_v. Let a scalar array shear be S_A(x,y)=(x,y+A x). Then diag(Q_x,Q_y) commutes with S_A exactly when Q_y A=A Q_x. In particular identical products Q of C_v commute through both sides of a shear whose A is a polynomial in translations.

This applies to the actual completed complex local endpoint: its blocks are products F C_q^-1 and translations (the source defines F as the product of C_coordinate, NOT the Hadamard matrix). It does not apply blindly to intermediate canonical-frame gates. The complete invocation must finish, all private registers clear, and all borrowed spectators restore before invoking the identity.

A more flexible sufficient identity allows monomial bridge changes. If a retiming changes cumulative exponents on bridge endpoints by d_x(v),d_y(v), and all differences d_y(v)-d_x(v) are even, the conjugated bridge coefficient differs by the translation product of X_v raised to half those differences. Emit and charge that translation in the bridge; the endpoint identity is then exact on arbitrary dirty input arrays. Equal parities are checked for each actual vector v, not for unrelated local coordinate indices. This criterion is sufficient for the specifically serialized translated bridge. It is not a license to change a bridge without emitting its compensation.

## A usable specialization requiring no new bridge at all

Take an asynchronous controller preserving each replica's original local and bridge order. When a replica completes its last local invocation, postpone its entire remaining suffix: late idle-child completions, its terminal bridge chain, its terminal translations and terminal data operation. Finish all replicas' local invocations first, then execute these suffixes. Leave the common global correction last.

Every postponed event touches only its replica's data families (plus unchanged cleared private workspace). Other replicas may borrow one of those families only through a complete normalized helper invocation. Such an invocation applies its declared residual to a subset of that owner's still-pending idle axes, restores all other coordinates including spectators, and clears all private registers. Distinct residual footprints on the owner commute, and their product with the explicit remainder is exactly the original pending idle child. Therefore regrouping all helper endpoints before the deferred idle completion gives exactly the old per-replica endpoint. The terminal bridges see fully completed original data states. The construction is valid for arbitrary initial owner dirt.

Concrete K4 consequence: late children 12..17 can remain available after their owner's stage8 local invocation, until the common end of all local calls. Their release points remain after the owner's stage2, stage4 or stage6 negative bridge, respectively. Whole owner uniqueness within every invocation, distinct active data families, literal spectator maps, disjoint pending footprints and explicit remainder billing are unchanged. No residual is split across physical families. No pending child's rank is reduced on the strength of this lemma alone.

## Invoice and audit requirements

The local scalar words, number of complete local sweeps and number of bridges are unchanged. Only chronology and owner allocation change; all owner charts must still be emitted and charged. The existing max-L2 prefix overcharge counts complete local sweeps and individual bridges, so its conservative bit bound remains valid independent of this reordered chronology. Each replica's projection must still equal its original source event sequence; all tail sweeps must precede that replica's first terminal bridge. Recompute the profile from actual assignments and actual unfilled remainders before reporting any saving.

## Exact pilot, scope and provenance

PAIRED-PARITY-SCREEN.json enumerates possible single-use, paired-X/Y factor retimings for the literal 73-axis K4 controller. The seven actual-vector incidence classes reproduce the original early and narrow bridge bounds. The meaningful extra freedom is precisely the terminal suffix timing above. This restricted enumeration does not exclude redesigns of the local word, multiple uses with cancellations, or different controller recipes.

Source definitions: PR496 finite_serial_pool.py gives C_v; its vendored split-centres-global/vendor/clifford_exact.py defines fourier as a product of C_v. The vendored e8-complex-gauge-kernel PROOF.md states both completed data endpoints. The source DATA-PHASES.json supplies actual pending vectors and all phase translations. The algebra is the same intertwiner equation used to transport operators in tensor-isomorphism reductions; OpenAI FourierCircuit/SparseShear and WordScheduling supply related complete-block cancellation and support-safe substitution structures, not an imported proof of this new schedule.

No new kappa is claimed in this note. The hosting lane must price and emit an actual deferred-suffix allocation, and the independent audit must validate it before composition.
