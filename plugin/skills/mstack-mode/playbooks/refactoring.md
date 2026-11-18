1) Pin behavior before any moves: run the how skill, then write a characterization test or equivalence harness. Type check/lint are not a pin.

2) Reshape by modeling the domain: delete branches/invalid states; never add indirection.

3) Define the target shape as if built today. If crossing a function boundary, run architect first.

4) Subtract before you add. Remove dead code and one-caller wrappers. Ship the smallest change; revert speculative cleanups.

5) Move in small steps with the pin green. For API reshapes, migrate all callers and delete the old API in the same wave—no shims/parallel paths.

6) Prove behavior unchanged on the real artifact. For larger reshapes, do an old-vs-new diff, a replayed baseline, or a smoke run via the control skill.

7) Keep only if it lowers reader load; otherwise revert.

8) Rebase into small ordered commits per Opening a PR.

Reply: structure changed, the pin, the equivalence proof, reader-load delta, what shipped, what was reverted. No new behavior.
