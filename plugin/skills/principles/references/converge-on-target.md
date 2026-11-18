# Converge on the target

**Rule:** Build the target design, migrate every caller, delete the old path.

## Integrate as if foundational

Redesign as if the new requirement had been there from the start; don't bolt it on.

- Read all affected files and understand the current design.
- Ask: "writing this from scratch with this requirement, what would we build?"
- Propagate through every reference: types, docs, examples, rationale sections.
- Design the whole redesign, then deliver incrementally per [Prove it works](prove-it-works.md).

## Outcome over intermediate states

Optimize for the verifiable end state, not smooth intermediate states; keeping every step stable breeds compatibility code that becomes debt.

- End-state integrity over transitional stability. Intermediate breakage is fine when planned, scoped, and reversible.
- Use for planned rewrites and migrations with explicit phase boundaries; declare where breakage is acceptable.
- Keep high-signal checks on actively touched areas while migrating.
- Require full static and runtime verification at plan completion.

## Migrate callers, then delete the legacy API

Once a new API is chosen, migrate callers and remove the old one in the same refactor wave; no compatibility layers.

- Don't keep legacy paths just because internal callers exist: inventory callers, migrate, delete the old API immediately.
- Temporary adapters are exceptional and time-boxed.
- Update tests to assert the new contract; delete tests that only protect pre-refactor implementation details.
- Applies when no external users need backward compatibility, the project can absorb coordinated breaking changes, and the new API is part of a simplification or refactor. Dual paths make the codebase append-only.
