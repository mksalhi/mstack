### Feature

**You own the design. Plan, review, verify. Delegate implementation.**

1. `how` over the affected subsystem.
2. `architect` for parallel design exploration.
3. Write the throughput checkpoint as four todo items. A dimension that does not apply keeps its item as `n/a: <reason>`:
   - **Blocking first steps.** Gates run before fan-out.
   - **Independent workstreams.** Disjoint files, services, or layers parallelize. Shared writes serialize.
   - **Shared mutable state.** Default to splitting the target (Separate before serializing shared state). Serialize only for real invariants.
   - **Smallest safe decomposition.** If one worker is best, name why.
4. Delegate code-writing to your configured feature model (default `claude-opus-5-5`), per Subagents, with a specific scope: file paths, success criteria, and the data shape and organizing structure chosen per Model the domain before any logic (state machine over scattered booleans, table over branching, typed model over repeated shape assumptions). When the implementation admits multiple valid shapes (error handling, abstraction layer, test structure), delegate via the `arena` skill instead. This is mandatory, with no skip-with-reason, and scoper does not override it (the gain is review separation). A subagent forbidden to spawn owns the diff directly with the same review separation; never reply "standing by" on a nested agent. Surgical edits; re-ground upstream-derived files against the source. Port shared-primitive improvements to every consumer and verify each. Commit liberally.
5. Verify on the matching surface. Flag "inconclusive" or wrong-surface; neither is a pass.
6. Rebase into small ordered commits per the Commits rule in **Opening a PR**, building, verifying, and committing each unit before the next (Prove it works). Stack follow-ups.
7. Contested design: `interrogate` before shipping.
8. Run **Opening a PR**.

Code-coupled work (one feature, one migration) goes to a single owner with the checkpoint inline, who fans out after the blocking phase. Parent-level fan-out is for slices with independent artifacts (audits, cross-subsystem investigations, competing experiments). Rewrite the checkpoint at phase boundaries. Spawn a fresh owner rather than chaining interrupts.

**Reply:** what you built, what you chose and why, the throughput checkpoint, open decisions. Tables for design alternatives.
