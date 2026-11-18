# Model the domain

**Rule:** Encode the domain in data structures.

Encode the real domain in a data structure instead of scattering it across conditionals; the right structure makes invalid states unrepresentable and deletes branches. Choose it at write time; later it becomes a deferred refactor.

Settle the data shape before logic: define core types early, trace every access pattern, fit structures to the dominant paths.

Reach for:
- A state machine over scattered booleans, phases, or lifecycle checks.
- A typed model over loose parameters or repeated shape assumptions.
- A map, registry, lookup table, or discriminated union over branching spread across files.
- A reducer or command/event model over ad hoc mutations.
- A module owning one body of domain knowledge, not a sequence (load, validate, transform, save). Execution order is not ownership.
- A small module boundary gathering repeated behavior, ownership, or invariants.
- A queue, cache, index, graph, tree, or normalized collection when the access pattern calls for it.
- Otherwise: work out what the code must never allow and how data is read, then find the structure that encodes exactly that.

Don't force an abstraction. Prefer boring code when the shape is clear, local, and unlikely to grow. Distrust indirection that removes no branches, duplicated rules, invalid states, or lifecycle risk.

Signs you skipped this: a feature adds one more branch to an if/else chain; a second boolean must stay in sync with the first; phase-named modules repeat the same domain rules (temporal decomposition).
