---
name: principles
description: "Use when a design call needs a principle: boundaries and validation, bulk edits, rewrites, repeated corrections, novel designs, sizing or estimating work, UX tradeoffs, a filling context window, retryable commands, core types and state, permission for reversible work, 'are we done', concurrent writers, or types (any .ts or .tsx edit)."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

- [Boundary discipline](references/boundary-discipline.md): Guard at system boundaries, trust internal types, keep business logic pure.
- [Build the lever](references/build-the-lever.md): Build the script, codemod or generator that does or proves it, so a reviewer can rerun it.
- [Code is cheap, proof is not](references/code-is-cheap.md): Size work in agent time, build the whole ask, rewrite when the shape fights the goal, and spend the savings on proof.
- [Converge on the target](references/converge-on-target.md): Redesign as if the requirement were there from the start, migrate every caller, delete the old path in one wave. No compatibility layers.
- [Encode lessons in structure](references/encode-lessons-in-structure.md): Turn a repeated correction into a lint, check or script, not more text.
- [Exhaust the design space](references/exhaust-the-design-space.md): When the answer is not obvious, build 2-3 competing sketches, compare them, then commit.
- [Experience first](references/experience-first.md): Put user delight over implementation convenience; ship fewer, polished features.
- [Guard the context window](references/guard-the-context-window.md): Send bulk work to subagents and keep summaries in the main thread.
- [Make operations idempotent](references/make-operations-idempotent.md): Reach the same end state every run.
- [Model the domain](references/model-the-domain.md): Choose the data shape before the logic, so invalid states can't be represented.
- [Never block on the human](references/never-block-on-the-human.md): For reversible work, proceed and then present; don't ask permission.
- [Prove it works](references/prove-it-works.md): Verify the real artifact, not a proxy or "it compiles". Check each unit before the next, and order delivery so the sequence proves itself.
- [Separate before serializing shared state](references/separate-before-serializing-shared-state.md): Remove the sharing before adding locks.
- [Type system discipline](references/type-system-discipline.md): Make illegal states unrepresentable, brand primitives, parse external data at boundaries, no casts.
