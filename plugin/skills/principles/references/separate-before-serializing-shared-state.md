# Separate before serializing shared state

**Rule:** Remove the sharing before adding locks.

When concurrent actors might share mutable state, first ask whether they need the same mutable object. If not, eliminate the sharing. If sharing is real, serialize structurally (lockfiles, sequential phases, exclusive ownership); instructions and conventions are not concurrency control.

**Why:** concurrent writes cause intermittent, hard-to-reproduce races.

**Pattern:**
1. **Identify shared mutable state:** files both read and write, branches both push to, APIs both define and consume.
2. **Default: eliminate the shared write target.** One canonical object, or independent facts? Give each actor its own file, key, branch, or state directory; merge only at the read/reporting boundary. Two workers writing their own `lastX` field into one `state.json` is still shared mutation; `indexer-state.json` + `metrics-state.json` is not.
3. **Only when one shared target is a real invariant, serialize structurally:** lockfiles, sequential phases, single-writer actor, or atomic compare-and-swap. "We need a lock" is a design smell to check, not the default.
