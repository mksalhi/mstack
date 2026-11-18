# Model the domain

- Encode the domain in data structures that make invalid states unrepresentable; choose the data shape before logic and fit it to dominant access paths.
- Prefer: state machine (over booleans/phases), typed/discriminated unions (over loose params), maps/registries/lookups (over spread branching), reducer/command/event (over ad hoc mutation), a module that owns domain rules (execution order is not ownership), small boundaries to gather invariants, and queues/caches/indexes/graphs/trees/normalized collections when access patterns demand.
- Derive structures from “what must never happen” and “how data is read.”
- Don’t force abstractions; prefer boring code when shape is clear/local; avoid indirection that removes no branches or risks.
- Smells you skipped this: growing if/else chains, booleans that must stay in sync, phase-named modules repeating rules.
