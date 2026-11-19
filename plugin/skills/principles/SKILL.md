---
name: principles
description: "Use when a design call needs a principle: boundaries and validation, bulk edits, rewrites, repeated corrections, novel designs, sizing or estimating work, UX tradeoffs, a filling context window, retryable commands, core types and state, permission for reversible work, 'are we done', concurrent writers, or types (any .ts or .tsx edit)."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

- **Boundary discipline.** Parse raw input (args, config, env, APIs) into domain types at the boundary; trust them inside with no re-validation. Business logic in pure functions; expose domain types, never wire or storage types.
- **Build the lever.** Default to a script, codemod, generator or rerunnable check over hand edits. Do one unit by hand, build the tool, rerun and diff on it. Fanning out? Put the recipe and verification contract in a skill the workers can't edit.
- **Code is cheap, proof is not.** Size work in agent units (files, subagents, runs), never human days. Build the whole ask with expert finish, no MVP or "phase 1"; effort is never a reason to stop or ask. Spend the savings on proof, then review your result as a bug hunt. `scoper` sets the code, not the scope.
- **Converge on the target.** Build what you would build from scratch with this requirement. Migrate every caller and delete the old path in the same wave, no compatibility layers; tests assert the new contract.
- **Encode lessons in structure.** Turn a repeated correction into a lint, check or script, not more text. Record every correction and apply it now or leave a concrete todo.
- **Exhaust the design space.** When the answer is not obvious (novel UI, architecture with real alternatives), build 2-3 different sketches, compare, then commit. Skip for established patterns and clear-target fixes.
- **Experience first.** User delight over implementation convenience. Ship fewer, polished features; every option serves the core loop or goes.
- **Guard the context window.** Send bulk reads and large payloads to subagents; keep summaries in the main thread. Cap each phase's files and turns.
- **Make operations idempotent.** Read state, diff, apply only what is missing. Write to temp then rename; make leftovers detectably stale. Test by running twice and crashing at each step.
- **Model the domain.** Pick the data shape before the logic so invalid states can't exist. Growing if/else chains or booleans that must stay in sync mean you skipped this. Open `references/model-the-domain.md` when choosing structures for core state.
- **Never block on the human.** Reversible work: proceed, then present what you did and why. Pause only for irreversible actions and the Always-pause list in `mstack-mode`.
- **Prove it works.** Verify the real artifact, not a proxy or "it compiles"; on failure suspect the observation first. One change per unit, run its check, advance only on green. Order commits red then green, subtraction before reshape.
- **Separate before serializing shared state.** Give each writer its own file, key or branch and merge at read time. Lock or single-writer only when one shared target is a real invariant.
- **Type system discipline.** Illegal states unrepresentable, external data `unknown` until parsed at the boundary, no `as` casts. Open `references/type-system-discipline.md` when writing TypeScript types, guards or schemas.
