# Validation of the published package

Checks were run serially on Windows with the bundled Python interpreter.
The original PR5550 control and the PR5684 candidate each had a 120-second
timeout and a sampled 512 MiB memory cap. No native or artifact-generating
replays ran concurrently.

The portable normal replay reproduced both complete frozen scientific outputs
in 26.234 and 26.765 seconds. The optimized replay reproduced those same bytes
in 24.265 and 24.765 seconds. Maximum sampled child RSS was 73,928,704 bytes.
Both reported `PASS_P104_EXPLICIT_OWNED_CALLER_AUDIT`, all 16 rejection controls,
and the exact public-hole permutation fixture.

An initial wrapper run failed byte equality because Windows stdout converted
LF to CRLF. The wrapper now explicitly selects UTF-8 and LF before executing
the unchanged checker. The successful normal and optimized runs above used
that correction; no scientific field or expected output was changed.

A separate agent reviewed the adapter and independently recounted the frozen
literal word and complete output. It confirmed 66,366 paid jobs, 12,958 targets,
all 1,758 nonoverlapping local/query scratch intervals, eleven local lifetimes
with peak two, and ordinary allowance 124,302,196 below 184,647,552. It found
no blocking issue. Its requested clarification of the inherited provenance
keys is included in the README. This is an independent agent check, not human
review or formal proof-kernel acceptance.

Package metadata and source pins passed. Committed-byte, source-history,
registered replay and standalone export checks are separate publication gates;
their results are reported in the PR rather than inferred from these runs.
