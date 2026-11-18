# Prove it works

**Rule:** Verify against the real artifact, not a proxy.

Verify every output by checking the real thing directly, not proxies, self-reports, or "it compiles."

**Why:** proxies (mtimes, output freshness, agent self-reports, cached screenshots) feel cheap; acting on a wrong inference costs more.

- Check process liveness directly, not through derived state.
- Read the actual value, not a cached or derived representation.
- When verification fails, suspect the observation method before the system.

To make the check rerunnable, build it as a lever per [Build the lever](build-the-lever.md).

## Per unit

Split multi-step work (sweep, migration, run of similar edits) into small units, each a bracket: known-good state, one change, run the check. Advance only on green; a break is cheap to localize at its unit, buried after a batch.

Start from current trunk. Rebase only unpushed work; merge trunk into pushed or long-lived branches. Run the per-unit check even when a lever does the edits.

## Delivery order

Stack commits and PRs in the order that proves the work, red then green: failing test first, fix on top. Scaffold first: anything later phases use (CI, linting, test infrastructure, shared types) lands before the features. Subtraction before reshape; baseline capture before treatment. Each commit small, single-purpose, landable alone, so the sequence reads as an argument.
