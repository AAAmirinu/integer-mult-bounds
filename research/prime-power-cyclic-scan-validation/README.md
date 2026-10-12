# Portable replay evidence

`macos-dirty/` and `linux-dirty/` are complete fresh replays of the current
nine-stage source manifest, including varying unit phases and dirty-array
inverse shears. They passed on macOS/Python 3.14 in 164.74s and Linux
aarch64/Python 3.12 in 163.67s. All nine deterministic certificates
are byte-identical across platforms. The collector checks source pins,
every artifact and log hash, and coverage derived from the actual records.

The original five stages retain 108 generic cases, 480 mixed-factor cases
with 240 dense comparisons, 345 budget instances, 8384 stride mappings,
43 routed executions, and 116 varying-phase/coefficient cases with 72 dense
comparisons. The dirty extension adds 36 leaf cases, 120 dense compositions,
24 actual-kernel cases and 1035 integer precision budgets. All 48 malformed
or corrupted controls are rejected, including eight instruction mutations.
Each current platform directory retains the receipt, nine certificates,
stage record, nine logs and independent collection record.

Current source manifest: `01ad8bfa2f392cdba88d398fdfd62f5d6cc1c172887cdc2c5ce38c9040d979e6`.

`macos-weighted/` and `linux-weighted/` retain the previous five-stage
replays at manifest `bccbfe9d741d2b19f50e7749f8b161fbd80de0bded2ab05047f705e58f03367d`.
`macos/` and `linux/` retain the earlier four-stage evidence at manifest
`947439ebc034aa28003d5940037b8abd05be94b1269b20fb09ca3d08bf3abb46`.
These earlier receipts are historical, not evidence for the current source.

Timings are operational metadata, not controlled performance benchmarks.
The written proof and cited algorithms determine general complexity;
finite replays do not establish the complete multiplication theorem or
bit-reversible arithmetic compilation. An initial earlier Linux transport
was rejected because archive metadata added AppleDouble files; explicit
regular-file archives corrected it without weakening source checks.
