### Autonomous run

**You own the exit condition. Define done, then drive to it without stopping.**

1. State the exit condition as a checkable predicate before the first iteration (tests green, repro fixed, all N PRs merged, pixel-diff zero).
2. Wake with Claude Code's built-in `/loop`. An event to watch (CI, a merge, a ref advancing) gets a watcher subagent that wakes you, with a long time-based heartbeat as fallback. No event: a fixed-interval heartbeat sized to when the result is worth re-checking.
3. Each iteration makes the smallest change the evidence justifies, verifies it against the predicate, commits if it advanced, and reverts what didn't help, including "might help" extras. Verify each unit before the next (Prove it works).
4. Mid-run discoveries are yours. Fix broken skills, related bugs, flaky verifiers, review noise, tooling failures, orphaned follow-ups, and fixable drift via mstack-mode, out-of-band fixes in their own PR. Never park reversible work for the human or use `AskUserQuestion`. Surface only irreversible actions, product or preference calls no experiment can settle, or a real dead end. Return to the predicate after each side fix.
5. Log every iteration via the `decision-log` skill: what changed, whether the predicate moved.
6. Stop when the predicate is met. A plateau is not a stop; pivot past it. Surface a genuine dead end rather than spinning. Never relax the predicate.

**Reply:** exit condition, iterations run, what landed, what was discarded, final predicate state.
