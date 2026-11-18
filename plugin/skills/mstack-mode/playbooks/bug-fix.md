### Bug fix

- Ship only smallest evidence-backed diffs; revert refuted.

1) Diagnose via phases 1–4 in <mstack>/skills/debug/SKILL.md. Build loop via control skill (mstack-mode Routing). Ask user only per “cannot build a loop.” Seed how/why. Confirm mechanism via runtime evidence before step 2.

2) Crossing function boundary → architect first. Delegate scoped implementation to bug-fix model (default `claude-opus-5-5`).

3) Phases 5–6: if Phase 5 finds a seam, land the regression test as its own commit before the fix; else keep Phase 1 loop and re-run on same surface. “Inconclusive”/wrong-surface ≠ pass. Remove tagged debug logs.

4) Run Opening a PR.

Reply: what broke, root cause, fix, how verified. Paste failing-then-passing repro output verbatim.
