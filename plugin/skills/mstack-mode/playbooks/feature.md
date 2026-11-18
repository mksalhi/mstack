### Feature

Throughput checkpoint (four TODOs; use n/a: <reason> if not applicable):
- Blocking first steps before fan-out.
- Independent workstreams: disjoint artifacts parallelize; shared writes serialize.
- Shared mutable state: split first (Separate before serializing shared state); serialize only real invariants.
- Smallest safe decomposition: if one worker is best, name why.

Delegate code-writing to the configured feature model (default claude-opus-5-5) per Subagents. Model the domain before logic. If multiple valid shapes, delegate via the arena skill (mandatory; no skip). If a subagent cannot spawn, it owns the diff with same review separation; never reply "standing by". Surgical edits; re-ground upstream-derived files; port shared-primitive improvements to consumers and verify; commit liberally.

Verify on the matching surface; "inconclusive" or wrong-surface is not a pass. Rebase into small ordered commits per Opening a PR; build, verify, and commit each unit.

Code-coupled work: single owner; fan out after blocking; parent-level fan-out only for independent artifacts.

Reply: what you built; what you chose and why; the throughput checkpoint; open decisions. Tables for design alternatives.
