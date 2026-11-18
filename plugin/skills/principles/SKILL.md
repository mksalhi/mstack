---
name: principles
description: "Use when a design call needs a principle: boundaries and validation, bulk edits, rewrites, repeated corrections, novel designs, UX tradeoffs, a filling context window, retryable commands, core types and state, permission for reversible work, 'are we done', concurrent writers, or types (any .ts or .tsx edit)."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Principles

Apply the rule in the matching row. Open the linked file only when the rule alone does not settle the call; it holds the reasoning, edge cases and examples. Three more principles are skills: Scoper (`scoper`, always on), Fix root causes (`debug`) and Test audit (`test-audit`).

| Principle | When | Rule |
|---|---|---|
| [Boundary discipline](references/boundary-discipline.md) | Validation, error handling, framework adapters | Guard at system boundaries, trust internal types, keep business logic pure. |
| [Build the lever](references/build-the-lever.md) | Repetitive or bulk work: edits, migrations, checks | Build the script, codemod or generator that does or proves it, so a reviewer can rerun it. |
| [Converge on the target](references/converge-on-target.md) | A new requirement in an existing design, a rewrite, a migration, a new API with old callers | Redesign as if the requirement were there from the start, migrate every caller, delete the old path in one wave. No compatibility layers. |
| [Encode lessons in structure](references/encode-lessons-in-structure.md) | The same instruction or correction comes up twice | Encode it as a lint, check, metadata flag or script instead of more text. |
| [Exhaust the design space](references/exhaust-the-design-space.md) | A novel UI interaction or architecture choice with no precedent | Build 2-3 structurally different prototypes or sketches, compare them, then commit. A variant of the first shape doesn't count. |
| [Experience first](references/experience-first.md) | Product, UX or scope tradeoffs | Favor user delight over implementation convenience, and fewer, polished features. |
| [Guard the context window](references/guard-the-context-window.md) | Big outputs, long files, repeated reads, fan-out | Send bulk work to subagents and keep summaries in the main thread. |
| [Make operations idempotent](references/make-operations-idempotent.md) | Commands, lifecycle steps or loops that may crash and retry | Reach the same end state every run. |
| [Model the domain](references/model-the-domain.md) | Core types, stateful logic, heavy branching, a shape assumption repeated across files | Encode the domain in a structure (state machine, typed model, table, reducer), not scattered conditionals. |
| [Never block on the human](references/never-block-on-the-human.md) | Tempted to ask permission for reversible work | Do it, show the result, let the human correct. |
| [Prove it works](references/prove-it-works.md) | Before calling work done, multi-step work, stacked commits and PRs | Verify the real artifact, not a proxy or "it compiles". Check each unit before the next, and order delivery so the sequence proves itself. |
| [Separate before serializing shared state](references/separate-before-serializing-shared-state.md) | Concurrent actors could write the same file, branch, key or object | Remove the sharing before adding locks. |
| [Type system discipline](references/type-system-discipline.md) | Designing types or signatures; any .ts or .tsx edit | Make illegal states unrepresentable, brand primitives, parse external data at boundaries, no casts. Examples: [type-system-patterns.md](references/type-system-patterns.md). |
