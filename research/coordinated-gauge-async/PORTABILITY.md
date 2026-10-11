# Portable serialization and safety checks

Every child runs through code/run_portable.py. The wrapper preserves its script
arguments, import directory and working directory, and forces newly generated
Path.write_text output to UTF-8/LF. It changes no mathematical operation.
A fixture checked sibling imports, argv, cwd and exact LF output bytes. A separate
optimized-Python test confirmed the verifier refuses to run with assertions off.

This fixes a concrete issue: adapters_gk.py writes RESIDUAL-ADAPTERS.json as text;
integrate_gk.py embeds its raw SHA in the final template. Default Windows CRLF
and Linux LF produce different hashes despite identical parsed mathematics.
Pinned source/input bytes remain unchanged; `.gitattributes` uses `** -text`.

Generated gzip headers can differ across Python/zlib versions. Compressed hashes
are fresh same-run provenance, not fixed cross-platform mathematical identities.
The final template identity is the hash of decompressed canonical JSON. No claim
is made that Python3.14 or Linux was executed in this local Windows3.11 run.

The reconstructed word was compared against the independently nominated word.
Every program field matched. Differences were only an optional redundant R=560
field and two unused floating estimates in report. The constructor checks the
redundant dimension, removes only those metadata fields from its semantic hash,
and binds every remaining field. No numerical proof uses the removed estimates.
See research-notes/RECONSTRUCTION-METADATA-DIFF.json.

The final manifest binds all source and evidence bytes. The output directory must
be new and outside the package. No cleanup, network or publication is performed.
