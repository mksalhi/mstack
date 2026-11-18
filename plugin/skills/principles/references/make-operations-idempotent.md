# Make operations idempotent

**Rule:** Reach the same end state every run.

Operations must converge to the correct state however many times they run and wherever the previous run stopped. Every state-mutating operation answers: "What if this runs twice? What if the last run crashed halfway?"

**Why:** crashes, restarts, and retries are normal; partial state must not change the next run's outcome.

- Derive each step from the state that exists, not from what the previous run meant to do: read current state, compare to the goal, apply only the difference.
- Anything a run leaves behind (lock, temp file, half-written record, claimed job) must be recognizable as stale by the next run, judged by evidence that holds wherever the previous run could have stopped, not only the common case. E.g. write to a temp path and rename into place; compare artifacts by content, not creation order.

**Test:**
1. What happens if this runs twice in a row?
2. What happens if the previous run crashed at every possible point?
3. Does re-execution converge to the same end state?

If any answer is "it depends on what state was left behind," add a reconciliation step.
