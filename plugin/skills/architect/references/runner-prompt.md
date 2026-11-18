Output a candidate package: type sketch, function signatures, module map, and prose rationale per [`rationale-template.md`](rationale-template.md).

- Caller’s usage first: README usage + 2–3 real call sites before types; sketch derives from usage.
- Data structures first: trace dominant access; never “we’ll add a map / index / cache later.”
- Interface depth: small surface; complexity inside. No transport or wire types on the public API; parse into domain types behind it.
- Shared state: if two writers and answer isn’t “nothing,” use per‑actor state merged at read boundary, per Separate before serializing shared state (`principles`).
- Visible boundaries: “not implemented” bodies, TODO pseudocode for tricky logic, doc comments for intent/invariants. Types/signatures must trace input→output.
- Invariants in types > runtime checks > prose, per Encode lessons in structure (`principles`).
- Validate at boundaries; trust types inside. Business logic as pure functions; thin shell, per Boundary discipline (`principles`).
- Single source of truth per invariant; derive instead of sync.
- Idempotent state transitions, per Make operations idempotent (`principles`): safe if run twice or crash halfway.
- Short call chains; if tracing needs >3 files, flatten, per `scoper`.
