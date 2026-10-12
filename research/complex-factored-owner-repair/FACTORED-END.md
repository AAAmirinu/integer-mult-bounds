# Inherited two-helper construction

The JP8 two-factored-end construction is unchanged from PR627 at
`f95308a9afa5adc071fe75c8cd7feec172503d4f`, including the entire declarative
recipe and all verifier code. Its original explanation is preserved in
[comparison/PR627-FACTORED-END.md](comparison/PR627-FACTORED-END.md).
That historical note's owner-packing figures and commands describe the
original PR627 package. Use this package's README for the new owner map.

`tools/build_factored_end.py` still reconstructs the unchanged supplier
from the pinned PR623 inputs. `tools/replay_owner_map.py` now replays only
our placement changes from PR627; it does not change helper widths.
