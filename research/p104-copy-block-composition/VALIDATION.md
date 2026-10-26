# Validation record

This checkpoint composes PR5774 with the original R22 block at .00312204390.
It is superseded during this investigation by the newly released PR5786 source;
it is not a separate contribution or selected-frontier change.

CPython3.12.14 on macOS arm64, standard library only, no subagents. The full
primary replay passed. The two registered normal/optimized primary commands
passed in288.13 seconds. They checked all789 scalar inputs,2923 native maps with
absolute phases, the full caller, two moment engines, compiler and outer checks.
The added scalar-transfer compatibility proof passed normally in.16 seconds and
optimized in.23 seconds. Three actual source-byte corruptions reject. Metadata
and whitespace checks pass. Export and publication checks are not claimed for
this intermediate checkpoint. All frozen source bytes and prior evidence remain.
