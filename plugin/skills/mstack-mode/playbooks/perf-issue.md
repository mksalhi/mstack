### Perf issue

**You own the measurement story. Plan, review, verify the numbers.** Tie every fix to a measurement, never to a source read. For sustained improvement against a metric, use `playbooks/hillclimb.md`.

1. Capture a baseline trace via the matching control skill.
2. `how` to ground hypotheses. Don't claim a perf ceiling without running it. Try a strategy only when the trace shows its signal: elimination (needs the `how` pass, since a trace can't show deletability), divide and conquer, caching (name the invalidation first), indirection, batching, hedging, lazy evaluation, or scheduling off the interactive path (measure that path, not total work).
3. Plan the fix from the trace; `architect` first if it crosses a function boundary. Delegate to your configured perf-issue model (default `claude-opus-5-5`), per Subagents. Review the diff, capture a post-fix trace, and verify each attempt before the next (Prove it works).
4. Parse and compare the artifacts (JSON to sqlite, diff). Flag "inconclusive" or wrong-surface; neither is a pass.
5. Cite the measurement in the PR.
6. Run **Opening a PR**.

**Reply:** baseline number, post-fix number, delta, artifact path.
