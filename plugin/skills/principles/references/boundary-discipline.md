# Boundary discipline

**Rule:** Guard at system boundaries, trust internal types.

Business logic lives in pure functions; the shell is thin and mechanical.

**Pattern:**
- **At boundaries** (CLI args, config files, external APIs, network protocols): validate, return errors, handle defensively. Validate config at parse time; parse raw data into domain types.
- **Inside:** typed data, error propagation, no re-validation, no redundant nil checks deep in call chains.
- **Across the boundary:** expose domain concepts, not the boundary's private representation. Never re-export transport, storage, framework, or wire types through the public surface. General-purpose mechanism inside, special-purpose policy at the edge.
- **Pure functions, no framework dependencies:** parsing (raw bytes to typed state), prompt construction (state in, string out), scoring (state to results).

**Tests:**
- "Is this data crossing a system boundary right now?" If not, validation is redundant.
- "Can this be a pure function the shell just calls?" If yes, extract it.
