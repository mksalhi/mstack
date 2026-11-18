### Hillclimb

**You own the metric and the experiment's integrity. Supervise, review, delegate the attempts.** One change, one measurement, keep or revert. Never stack untested changes or claim a win from inspection (Prove it works).

1. Ground the workload. Run the `how` skill over the target, name the workload dimensions that move the result (data size, history, state, concurrency), and pick a case that reproduces the user's complaint. No reproducing case: fix the repro instead. Fix one metric, its better direction, and a checkable stop predicate pairing a target with a floor on attempts ("at least 50% better than baseline and at least 10 iterations"). Use the user's numbers, otherwise agree them.
2. Build the measurement harness, prove its sensitivity, then freeze it (Build the lever). Contrasting realistic workloads must separate as expected, with the target case reproducing the symptom; if not, revise workload or metric. Frozen means one repeatable command emits the metric, sampled past noise (median of N). Record the baseline and a green regression-gate run before any change.
3. Open `decisions.tsv` via the `decision-log` skill, one row per attempt: id, hypothesis, change, before, after, delta, tests, verdict (kept or reverted), note. Read it before each attempt. Keep it gitignored.
4. Each hypothesis names a specific mechanism from step 1 ("defer X off the boot path because it blocks first paint"), not "try memoizing something".
5. Loop, one hypothesis per iteration:
   - Delegate the change with a tight scope to your configured hillclimb model (default `claude-opus-5-5`), per Subagents. Review the diff (Guard the context window). Fan independent hypotheses to parallel subagents, each in its own worktree (Separate before serializing shared state).
   - Measure before and after with the frozen harness and run the regression gate.
   - Keep only when the metric moves past noise and the gate stays green. Otherwise revert in full.
   - One commit per accepted fix, `git add <files>`, never `-A`. Log the row either way.
   Check each iteration before the next (Prove it works). Unattended: borrow only the wake mechanism from `playbooks/autonomous-run.md`, not its stop rule.
6. Push past the first plateau. After several rejects in a row, pivot category, combine near-misses, re-read the source, or try something radical. Correctness and simplicity outrank the number: revert a win that breaks behavior, keep a simplification that holds the number (`scoper`).
7. Stop when the predicate is met or remaining ideas are marginal. Never relax the predicate, never quit with cheap untried hypotheses left. Stuck: surface it.
8. Run **Opening a PR** with accepted commits stacked in landing order.

**Reply:** metric and target, baseline to final with percent delta, iterations (kept vs reverted), each accepted fix on one line, the `decisions.tsv` path, the next idea you would try.
