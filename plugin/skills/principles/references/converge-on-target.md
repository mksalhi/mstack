# Converge on the target

Rule: Build the target design, migrate every caller, delete the old path.

## Integrate as if foundational

- Ask: "writing this from scratch with this requirement, what would we build?"
- Design the whole redesign, then deliver incrementally per [Prove it works](prove-it-works.md).

## Outcome over intermediate states

- End-state integrity over transitional stability. Intermediate breakage is fine when planned, scoped, and reversible.
- Require full static and runtime verification at plan completion.

## Migrate callers, then delete the legacy API

Once a new API is chosen, migrate callers and remove the old one in the same refactor wave; no compatibility layers.

- Don't keep legacy paths just because internal callers exist: inventory callers, migrate, delete the old API immediately.
- Update tests to assert the new contract; delete tests that only protect pre-refactor implementation details.
