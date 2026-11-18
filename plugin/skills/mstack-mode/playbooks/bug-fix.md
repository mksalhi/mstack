### Bug fix

**You own this task. Plan, review, verify.** Delegate investigation and the fix to subagents. Every shipped line traces to runtime evidence. A "might help" change is a hypothesis and does not ship. When evidence refutes a hypothesis, revert what it motivated. Ship the smallest change the evidence justifies.

1. Diagnose with the `debug` skill (`<mstack>/skills/debug/SKILL.md`), phases 1 to 4. Build the red-capable loop yourself on the matching surface via the control skill (mstack-mode Routing). Ask the user only when that skill's "cannot build a loop" section applies, after driving the surface as far as it goes. Seed the ranked hypotheses with `how` over the affected subsystem and `why` for regression history. Confirm the surviving *mechanism* with runtime evidence before step 2.
2. Plan the fix. Crossing a function boundary → `architect` first. Delegate implementation with a specific scope to your configured bug-fix model (default `claude-opus-5-5`).
3. Finish with debug phases 5 and 6. If Phase 5 finds a correct seam, the regression test lands as its own commit before the fix. Otherwise record the missing seam and keep the Phase 1 loop. Re-run the Phase 1 loop on the same surface. "Inconclusive" or wrong-surface is not a pass. Remove every tagged debug log.
4. Run **Opening a PR**.

**Reply:** what broke, root cause, fix, how you verified. Paste failing-then-passing repro output verbatim.
