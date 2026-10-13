# Independent checks

`audit_local.py` is the unchanged gauge44 checker: it reconstructs the exact scalar maps, frame chains, cones and inherited centre interface without importing the generator. `price_profile.py` is the unchanged PR656 two-engine/outer checker; it requires assertions because the retained outer engine uses them.

The new `extras/check_owner_map.py` independently reconstructs widths and child counts from the actual native outputs, checks the literal physical assignment against inherited geometry, and evaluates a separate rational moment interval. `extras/replay_owner_map.py` regenerates the exact owner bytes from the integer flow/slot certificate. Both use explicit exception checks and remain active under `-O`. The top-level full replay deliberately refuses `-O`.
