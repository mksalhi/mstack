### Perf issue

**You own the measurement story. Plan, review, verify the numbers.** Tie every fix to a measurement, never to a source read. For sustained improvement against a metric, use `playbooks/hillclimb.md`.

1. Capture a baseline trace via the matching control skill.
2. `how` to ground hypotheses. Don't claim a perf ceiling without running it. Strategy families generate hypotheses; try one only when the trace shows its signal:
   - **Elimination.** Does the hot path need to exist (unconsumed computation, always-off gate, redundant sync, legacy path)? The trace can't show deletability, so this needs the `how` pass.
   - **Divide and conquer.** Cost scales with input. Chunk, shard, prune, or parallelize independent pieces.
   - **Caching.** Identical inputs recompute or refetch. Name the invalidation before claiming the win.
   - **Indirection.** A cheaper intermediate absorbs hot-path work (index over scan, queue off the interactive thread). Add the hop only when it removes more than it adds.
   - **Batching.** Many small ops each pay fixed overhead (RPC, query, syscall, draw call). Coalesce.
   - **Redundancy.** The wait hangs on one slow instance. Hedge or replicate, only when the wait dominates and there is headroom.
   - **Lazy evaluation.** Cost lands on unused or not-yet-needed results. Defer to first use.
   - **Scheduling.** Move necessary work off the interactive moment (idle, background warmup, precompute, post-commit). Measure the interactive path, not total work.
3. Plan the fix from the trace; `architect` first if it crosses a function boundary. Delegate to your configured perf-issue model (default `claude-opus-5-5`), per Subagents. Review the diff, capture a post-fix trace, and verify each attempt before the next (Prove it works).
4. Parse and compare the artifacts (JSON to sqlite, diff). Flag "inconclusive" or wrong-surface; neither is a pass.
5. Cite the measurement in the PR.
6. Run **Opening a PR**.

**Reply:** baseline number, post-fix number, delta, artifact path.
