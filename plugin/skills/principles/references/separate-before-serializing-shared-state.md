# Separate before serializing shared state

Rule: Remove the sharing before adding locks.

Instructions and conventions are not concurrency control.

- Default: eliminate the shared write target; give each actor its own file/key/branch/state dir; merge only at read/reporting boundary. Two workers writing `lastX` into one `state.json` is still shared; `indexer-state.json` + `metrics-state.json` is not.
- Only when one shared target is a real invariant, serialize structurally: lockfiles, sequential phases, single-writer, or atomic compare-and-swap.
