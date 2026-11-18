# Make operations idempotent

Rule: Every run converges to the same correct state.

- Derive actions from current state: read -> diff -> apply only missing changes.
- Make leftovers detectable and safe: locks, temp files, half-written records, claimed jobs must be recognized as stale regardless of where a crash occurred. Write to a temp path then rename into place; compare artifacts by content, not creation order.

Test:
1) Run twice.
2) Crash at every step.
3) Re-execution converges.

If any answer depends on leftover state, add a reconciliation step.
