# Portable replay evidence

These are complete fresh macOS/Python3.14 and Linux aarch64/Python3.12
replays of the exact source manifest in the sibling cyclic-scan package.
`collect_verify.py` verifies source pins, all four successful stages,
every artifact and log hash, byte-identical deterministic certificates,
and coverage derived from their actual records.

Each platform retains the receipt, all four certificates, the stage
record, all four logs, and an independent collection record. Timing is
operational metadata, not a controlled performance benchmark. The written
proof and cited algorithms determine the general complexity claim; finite
replays do not establish the full multiplication theorem.

An initial Linux transport was rejected before mathematical replay because
macOS archive metadata added AppleDouble files. The corrected archive
contains only the manifest-covered regular files; the source and checker
were unchanged. The failed transport and correction remain recorded in
the local research evidence. These directories contain the final successful
replays only.
