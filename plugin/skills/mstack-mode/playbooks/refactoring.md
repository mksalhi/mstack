### Refactoring

**You own the contract. Structure changes, behavior does not.** A missing feature or real bug found mid-cleanup splits out; ship the structural change first against the pinned contract. A named redesign routes to Feature. Large or cross-cutting work goes to `figure-it-out`.

1. Pin the behavior contract. Run the `how` skill over the subsystem, then write a characterization test, snapshot, or equivalence harness before any structure moves. Type check and lint are not a pin.
2. Name the missing structure per Model the domain. Leave boring code whose shape is clear and local. The reshape deletes branches or invalid states, never adds indirection.
3. Name the target shape: module layout, types, call graph as if built today (Model the domain, Converge on the target). Crosses a function boundary: run `architect` first.
4. Subtract before you add: dead code, one-caller wrappers, redundant validators, orphan references (`scoper`). Ship the smallest change that reaches the target. Revert speculative cleanups.
5. Move in small steps, each keeping the pin green. For API reshapes, migrate every caller and delete the old API in the same wave, no shims or parallel paths (Converge on the target). Spot-check every rename against the files, including strings, prose, and back-references. Delegate mechanical edits with a specific scope (paths, names moved, behavior held) to your configured refactoring model (default `claude-opus-5-5`), per Subagents.
6. Prove behavior unchanged on the real artifact (Prove it works). Larger reshapes get an equivalence check: an old-vs-new output diff, a replayed baseline, or a smoke run via the control skill.
7. Keep it only if it lowers reader load somewhere (`scoper`). Otherwise revert.
8. Rebase into small ordered commits per the Commits rule in **Opening a PR**: subtraction, reshape, follow-on cleanup, each green (Prove it works). Run **Opening a PR**.

**Reply:** structure changed, the pin, the equivalence proof, reader-load delta, what shipped and what was reverted. No new behavior.
