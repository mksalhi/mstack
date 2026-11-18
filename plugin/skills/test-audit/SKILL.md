---
name: test-audit
description: "Use whenever writing, changing, reviewing or pruning tests: authoring gate plus audit for low-value or implementation-coupled tests."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Test audit

Read the repo's `AGENTS.md` files first; they win over this skill. Three modes, one bar:

- **Authoring**: gate every new or changed test at write time.
- **Audit**: sweeps for tests that restate source, duplicate stronger tests, couple to implementation, or keep test-only production hooks alive. Split a broad audit into separate PRs; aim for confidence, not deletion count.
- **Campaign**: prune every test a workspace or subsystem owns. Read [CAMPAIGN.md](CAMPAIGN.md) first.

## Authoring gate

**The `undefined` check:** if the test would still pass with every imported function returning `undefined`, it cannot fail for a defect. Five shapes:

- **Weak or no assertion**: none, or only `toBeDefined`, `toBeTruthy`, `not.toThrow`, `toBeInstanceOf`, `toBeGreaterThan(0)`, `assert x is not None`.
- **Mock or absence only**: only `toHaveBeenCalled`, `not.toHaveBeenCalled`, `toBeUndefined`, `toEqual([])`, `toHaveLength(0)`, `not.toBe(wrongValue)`.
- **Self-referential**: expected value comes from the code under test: `expect(parsed.url).toBe(buildUrl(...))`.
- **Constant pin**: restates a hand-maintained constant, default, table row, or prompt string: `expect(LIMITS.maxTools).toBe(8)`.
- **Fixture asserts fixture**: asserts data built in setup; the subject never runs in the body.

Fix: call the subject in the body with one concrete input and assert the literal output or observable effect, `expect(slugify("Hello, World!")).toBe("hello-world")`. For an absence check, also assert presence on the other input in the same test. For a constant, test the mechanism that reads it. For a mock, assert the payload received or the state after. If no such assertion exists, delete the test. Cross-row table relations (a key in two tables, a parent that exists) and `*.test-d.ts` compile-time checks pass.

Then answer four questions; add the test only when all four have answers:

1. What observable behavior, invariant, or independent contract does it protect?
2. What credible regression makes it fail?
3. Why doesn't existing coverage catch it? Each contract has one primary owner test at the strongest boundary; another layer needs its own distinct risk (e.g. a transport or lifecycle failure the owner cannot reach). Prefer extending a table-driven case or shared fixture over a near-duplicate; consolidate duplicated setup in the same change.
4. Does it need a production seam (export, flag, wrapper, injection hook) no production caller needs? Then test at the real boundary instead.

Then check every [junk pattern](#junk-patterns); a match fails unless the [retention bar](#retention-bar) names the contract it independently guards. A test that breaks under behavior-preserving refactoring asserts implementation: rewrite it at the owning boundary.

Before landing, break the production code it guards, watch the test go red, then restore the source exactly.

Bug regression tests must fail on pre-fix code for the intended reason and pass after the owner-boundary repair. One regression at the owner boundary covers the bug; don't replay it at every layer.

## Junk patterns

Authoring rejects new tests matching these; audits hunt existing ones.

- assertion-free coverage probes;
- self-comparisons and identity copiers;
- copied fixtures, inventories, manifests, or export lists;
- exact source, import, or string greps;
- private predicate or call-shape tests duplicated at real boundaries;
- duplicate invocations of the same contract;
- per-implementation replays of shared helpers;
- tests whose only purpose is preserving test-only exports, globals, or wrappers;
- dead production code whose only callers are tests;
- expected values produced by the helper or renderer under test;
- mocks that implement the asserted behavior, or one identical mock standing in for different APIs;
- fixtures that supply the receipt, admission, or callback ordering the owner should produce, or persistence asserted against a store the path never writes;
- capability tests that restate declared flags instead of exercising the delivery or acknowledgement the flag promises;
- negative controls that pass for an unrelated reason (a denial from a different guard, a rejection production never reaches);
- names or fixtures that promise more than the input exercises (a "retires the window" test asserting the window was not cleared);
- tests restating constants, enum or model fields, catalog flags, or prompt wording (prompt bytes excepted per the retention bar);
- tests of framework or library behavior (serializer renames, schema validation, 422s, ORM defaults) our code adds no logic to;
- assertions that only check a mock was called when the outcome is observable at the boundary (request bodies, rows, emitted events);
- parametrize rows that reach the same branch as another row;
- global request or event counts in async code (racy); assert the specific effect;
- DB-backed tests pointed at a developer's database; run only against a disposable server the harness creates.

## Discovery

Read-only; report evidence before editing. Hunt the [junk patterns](#junk-patterns). For broad scope, run parallel lanes (one per workspace or subsystem plus a cross-cutting pattern sweep). Outside campaign mode, prefer a few high-confidence candidates over a speculative inventory.

In an audit, an existing test that must change for behavior-preserving reorganization is suspect, not automatically deletable. Before judging a candidate, read the complete test and production owner, entry point, callers, callees, sibling implementations, overlapping tests, the config that selects it (vitest include globs, pytest markers), and relevant history. For claimed dependency-backed behavior, inspect the dependency source or types.

## Retention bar

Keep a test that independently enforces a public API, protocol, config, storage, security, or architecture contract: API router contracts, DB migrations and access policies, third-party payloads, and prompt bytes only when they are an external contract (provider protocol, cache key, persisted format). Also keep:

- call ordering when order is observable;
- regressions with a credible failure mode;
- source inspection when it is the cheapest independent guard: fails when the contract (user-facing key, byte, path) changes, survives an identifier-only refactor;
- a retained test failing on baseline: treat as a possible product bug, reproduce, repair the owner.

Static or slow is not a deletion reason. Prove a test that resembles implementation is not the independent contract before removing it.

## Candidate evidence

Record every field before editing; a candidate with a missing field is not ready for deletion:

- exact test name and location;
- what failure it can actually detect;
- non-test callers of the covered production or support seam;
- stronger remaining owner-boundary proof, or why none is needed;
- relevant history and why the test or seam exists;
- production or test-support deletion unlocked;
- risk and the focused validation command.

## Edit shape

One coherent owner-boundary batch. Delete obsolete test-only exports, globals, wrappers, and dead production paths (no aliases). Move retained regressions to canonical owners. Consolidate repeated package or dependency assertions into one generic contract. Update vitest include globs or pytest markers if suites move. Prefer net-negative production LOC. No replacement tests restating the same implementation; don't turn uncertain candidates into cleanup.

## Validation

Never edit source or tests while a test watcher runs in the checkout. Run DB-backed and e2e suites only where the repo's AGENTS.md allows (an isolated worktree stack, never the human's primary checkout).

1. Run the smallest owner and sibling tests with a name filter, then the touched suite.
2. For removed source greps or plan assertions, run the script or dry-run that owns the real contract.
3. Run the repo's formatter, then `git diff --check`.
4. Run lint and typecheck, including downstream packages consuming changed shared types.
5. Inspect `git diff --numstat`; report production/tooling separately from tests and test support.
6. After final edits, run mstack-mode's before-commit and before-review gates.

## Landing

Commit, push, open a PR, or land only when authorized. Read `<mstack>/skills/pr/SKILL.md` for the PR body and follow the mstack-mode Shipping playbook (`<mstack>/skills/mstack-mode/playbooks/shipping.md`) to land. One coherent PR at a time; after landing, refresh from current `main` and rerun read-only discovery for the next batch.

## Handoff

Report:

- root cause and removed low-value categories;
- production owner simplifications;
- retained false positives and why they remain valuable;
- focused and full proof actually run;
- production versus test LOC;
- PR and merge state;
- named follow-ups.
