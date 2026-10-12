# Portable replay evidence

`macos-weighted/` and `linux-weighted/` are complete fresh replays of the
current five-stage source manifest, including independently varying
unit phases. They passed on macOS/Python3.14 in157.14s and Linux
aarch64/Python3.12 in144.34s. All five deterministic certificates are
byte-identical across platforms. The collector checks source pins, every
artifact and log hash, and coverage derived from the actual records.

The five stages cover108 generic cases,480 mixed-factor cases with240
dense comparisons,345 budget instances,8384 stride mappings,43 routed
executions, and116 varying-phase/coefficient cases with72 additional
dense comparisons. All28 malformed/corrupted controls are rejected.
Each current platform directory retains the receipt, five certificates,
stage record, five logs and independent collection record.

`macos/` and `linux/` preserve the earlier four-stage evidence at the
original manifest947439ebc034aa28003d5940037b8abd05be94b1269b20fb09ca3d08bf3abb46.
Those receipts are historical; their pins are not represented as current.
Current manifest:bccbfe9d741d2b19f50e7749f8b161fbd80de0bded2ab05047f705e58f03367d.

Timings are operational metadata, not controlled performance benchmarks.
The written proof and cited algorithms determine the general complexity
claim; finite replays do not establish the full multiplication theorem.
An initial earlier Linux transport was rejected before mathematical
replay because macOS archive metadata added AppleDouble files. Explicit
regular-file archives corrected it without weakening source checks.
