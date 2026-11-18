# Architect runner prompt

The orchestrator passes this to every parallel candidate runner in Phase B, filling in: the task, Phase A grounding artifacts, the isolated working directory (a git worktree when available, else a per-runner subdirectory under the sketch dir; candidates must be independent), and the output path.

You are producing one candidate design in architect's parallel exploration. Read the `architect` skill in full first. Output a candidate package: type sketch, function signatures, module map, and prose rationale per [`rationale-template.md`](rationale-template.md).

The orchestrator compares candidates on these axes:

- Caller's usage first: README-style usage and two or three real call sites before the types; derive the sketch from them and reconcile the sketch to the usage, not the reverse.
- Data structures first. Trace each dominant access pattern through the structure; "we'll add a map / index / cache later" means the structure is wrong.
- Interface depth: capability hidden relative to surface size. Prefer a simple interface that pulls complexity into the callee, even at implementation cost. No transport or wire types on the public API; parse into domain types behind it.
- Shared state: if two actors might both write and the answer to "what happens?" isn't "nothing," default to per-actor state merged at the read boundary, per Separate before serializing shared state (`principles`).
- Visible boundaries: `not implemented` bodies, `// TODO` pseudocode for tricky logic, doc comments stating intent and invariants. Data must be traceable input to output from types and signatures alone.
- Invariants in types: hard-to-misuse types > runtime checks > prose comments, per Encode lessons in structure (`principles`).
- Validate at boundaries, trust types inside, per Boundary discipline (`principles`). Business logic as pure functions; thin shell.
- Single source of truth per invariant. Derive instead of sync.
- Idempotent state transitions where applicable, per Make operations idempotent (`principles`): runs twice? crashes halfway?
- Short call chains: if tracing the flow needs more than three files, flatten, per `scoper`.

You are one of several runners, possibly on the same model; differ in shape anyway. Produce your best design; don't hedge toward a safe middle. Differences between candidates are the signal for picking a base and grafting.
