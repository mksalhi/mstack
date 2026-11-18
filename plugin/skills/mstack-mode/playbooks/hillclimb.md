### Hillclimb

Own the metric and integrity. One change → one measurement. Never stack untested changes or claim a win by inspection.

1) Ground the workload: run the `how` skill on the target; name workload dimensions; pick a reproducible case. No repro: fix the repro. Choose one metric, its better direction, and a stop predicate (target + floor on attempts; use the user’s numbers, else agree them).

2) Freeze the measurement harness: contrasting workloads must separate and the target case must reproduce the symptom; else revise workload/metric. One repeatable command emits the metric, sampled past noise (median of N). Record a baseline and a green regression-gate run before any change.

3) Open `decisions.tsv` via the `decision-log` skill. One row per attempt: id, hypothesis, change, before, after, delta, tests, verdict, note. Keep it gitignored.

4) Each hypothesis names a specific mechanism from step 1.

5) Loop:
- Delegate tightly scoped changes to hillclimb subagents (default `claude-opus-5-5`), one hypothesis per worktree. Review diffs.
- Measure before/after with the frozen harness; run the regression gate.
- Keep only past-noise wins with a green gate; else revert fully.
- One commit per accepted fix; `git add <files>`, never `-A`. Log the row.
- Unattended: borrow only the wake mechanism from `playbooks/autonomous-run.md`, not its stop rule.

6) Push past plateaus. Correctness/simplicity outrank the number; revert wins that break behavior; keep simplifications that hold the number (`scoper`).

7) Stop when the predicate is met or ideas are marginal. Never relax it. If stuck, surface it.

8) Open a PR with accepted commits stacked in landing order.

Reply: metric/target; baseline→final with percent delta; iterations (kept vs reverted); each accepted fix (one line); `decisions.tsv` path; next idea.
