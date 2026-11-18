---
name: principles
description: "Use when a design call needs a principle: boundaries and validation, bulk edits, rewrites, repeated corrections, novel designs, UX tradeoffs, a filling context window, retryable commands, core types and state, permission for reversible work, 'are we done', concurrent writers, or types (any .ts or .tsx edit)."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Principles

Apply the rule in the matching row. Open the linked file only when the rule alone does not settle the call; it holds the reasoning, edge cases and examples.

| Principle | When | Rule |
|---|---|---|
| [Boundary discipline](references/boundary-discipline.md) | Adding validation, error handling or framework adapters | Guard at system boundaries, trust internal types. |
| [Build the lever](references/build-the-lever.md) | Repetitive or bulk work: edits, migrations, checks | Build a script, codemod or generator instead of working by hand. |
| [Converge on the target](references/converge-on-target.md) | Adding a requirement to an existing design, or a rewrite | Build the target design, migrate every caller, delete the old path. |
| [Encode lessons in structure](references/encode-lessons-in-structure.md) | The same instruction or correction comes up twice | Encode it as a lint, check or script instead of more text. |
| [Exhaust the design space](references/exhaust-the-design-space.md) | A novel UI interaction or architecture choice with no precedent | Build 2-3 competing prototypes or sketches, compare them side by side, then commit. A second flavor of the first shape does not count. |
| [Experience first](references/experience-first.md) | Product, UX or scope tradeoffs | Favor user delight and fewer, polished features. |
| [Guard the context window](references/guard-the-context-window.md) | Context is filling: big outputs, long files, fan-out | Send bulk to subagents, keep summaries. Overflow degrades reasoning and halts progress. |
| [Make operations idempotent](references/make-operations-idempotent.md) | Commands, lifecycle steps or loops that may crash and retry | Reach the same end state every run. |
| [Model the domain](references/model-the-domain.md) | Choosing core types, stateful logic, heavy branching | Encode the domain in data structures. |
| [Never block on the human](references/never-block-on-the-human.md) | Tempted to ask permission for reversible work | Do it, show the result, let the human correct. |
| [Prove it works](references/prove-it-works.md) | Before calling work done, and on multi-step sweeps | Verify against the real artifact, not a proxy. |
| [Separate before serializing shared state](references/separate-before-serializing-shared-state.md) | Concurrent actors could write the same file, branch, key or state | Remove the sharing before adding locks. |
| [Type system discipline](references/type-system-discipline/index.md) | Designing types or signatures; any .ts or .tsx edit | Illegal states unrepresentable, parse at boundaries, no casts. |
