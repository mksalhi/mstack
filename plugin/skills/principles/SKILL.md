---
name: principles
description: "Use when a design call needs a principle: boundaries and validation, bulk edits, rewrites, repeated corrections, novel designs, UX tradeoffs, a filling context window, retryable commands, core types and state, permission for reversible work, 'are we done', concurrent writers, or types (any .ts or .tsx edit)."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

- [Boundary discipline](references/boundary-discipline.md): Guard at system boundaries, trust internal types, keep business logic pure.
- [Build the lever](references/build-the-lever.md): Build the script, codemod or generator that does or proves it, so a reviewer can rerun it.
- [Converge on the target](references/converge-on-target.md): Redesign as if the requirement were there from the start, migrate every caller, delete the old path in one wave. No compatibility layers.
- [Guard the context window](references/guard-the-context-window.md): Send bulk work to subagents and keep summaries in the main thread.
- [Make operations idempotent](references/make-operations-idempotent.md): Reach the same end state every run.
- [Prove it works](references/prove-it-works.md): Verify the real artifact, not a proxy or "it compiles". Check each unit before the next, and order delivery so the sequence proves itself.
- [Separate before serializing shared state](references/separate-before-serializing-shared-state.md): Remove the sharing before adding locks.
- [Type system discipline](references/type-system-discipline.md): Make illegal states unrepresentable, brand primitives, parse external data at boundaries, no casts.
