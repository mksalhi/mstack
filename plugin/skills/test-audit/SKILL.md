---
name: test-audit
description: "Use whenever writing, changing, reviewing or pruning tests: authoring gate plus audit for low-value or implementation-coupled tests."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Test audit

Read the repo’s AGENTS.md files first; they win over this skill. Three modes, one bar:
- Authoring: gate every new or changed test at write time.
- Audit: sweep for restatement, duplication, coupling, or test-only hooks. Split broad audits; aim for confidence.
- Campaign: prune every test a workspace or subsystem owns in one PR. Open [CAMPAIGN.md](CAMPAIGN.md) before step 1 of a campaign and finish each of its steps before the next.

## Authoring gate

Undefined check: if the test passes with every import returning undefined, it cannot fail for a defect. Reject:
- weak or no assertion (defined/truthy/instance/greater-than-zero/None);
- mock/absence-only (called/uncalled/undefined/empty/length/not-toBe wrongValue);
- self-referential (expected from the subject itself);
- constant pins (restated limits/defaults/strings/tables/prompts);
- fixture asserts fixture (subject never runs in body).

Fix: call the subject with one concrete input and assert the literal output or observable effect; for absence, also assert presence with the other input; for constants, test the reader; for mocks, assert payload/state. If none fits, delete. Cross-row table relations and *.test-d.ts compile-time checks pass.

Before adding, answer:
1) What observable behavior, invariant, or independent contract does it protect?
2) What credible regression makes it fail?
3) Why doesn’t existing coverage catch it? One primary owner test per contract at the strongest boundary; another layer needs a distinct risk.
4) Does it need a seam no production caller needs? Then test at the real boundary instead.

A test that breaks under behavior-preserving refactoring asserts implementation; rewrite it at the owning boundary.

Before landing a new test, break the guarded code to watch it go red, then restore exactly. Bug regressions must fail on pre-fix code for the intended reason and pass after the owner-boundary repair; one owner-boundary regression suffices.

## Junk patterns

- self-comparisons and identity copiers;
- copied fixtures, inventories, manifests, or export lists;
- exact source, import, or string greps;
- private predicate or call-shape tests duplicated at real boundaries;
- duplicate invocations of the same contract;
- per-implementation replays of shared helpers;
- tests whose only purpose is preserving test-only exports, globals, or wrappers;
- dead production code whose only callers are tests;
- mocks that implement the asserted behavior, or one identical mock for different APIs;
- fixtures that supply the receipt, admission, or callback ordering the owner should produce, or persistence asserted against a store the path never writes;
- capability tests that restate declared flags instead of exercising delivery/acknowledgement;
- negative controls that pass for an unrelated reason;
- names/fixtures that promise more than inputs exercise;
- tests of framework/library behavior our code adds no logic to;
- assertions that only check a mock was called when the outcome is observable at the boundary;
- parametrize rows that reach the same branch;
- global request/event counts in async code (racy);
- DB-backed tests pointed at a developer’s database.

## Discovery

Read-only; report evidence before editing. Prefer high-confidence candidates. Read the complete test and production owner, entry/exit, siblings, overlapping tests, config selecting it, and relevant history. For dependency-backed behavior, inspect the dependency source or types.

## Retention bar

Keep tests that independently enforce a public API, protocol, config, storage, security, or architecture contract (API router contracts, DB migrations/access policies, third-party payloads, prompt bytes only when an external contract). Also keep:
- call ordering when order is observable;
- regressions with a credible failure mode;
- cheapest independent source inspection guard (fails on contract changes, survives identifier-only refactors);
- retained tests failing on baseline: treat as a possible product bug; reproduce and repair the owner.

Static or slow is not a deletion reason. Prove a test is not the independent contract before removing it.

## Candidate evidence

Record: exact test name/location; what failure it can actually detect; non-test callers of the covered production/seam; stronger remaining owner-boundary proof (or why none is needed); relevant history/why it exists; production/test-support deletion unlocked; risk and the focused validation command.

## Edit shape

One coherent owner-boundary batch. Delete test-only exports/globals/wrappers and dead production paths. Move retained regressions to canonical owners. Consolidate repeated package/dependency assertions into one generic contract. Update vitest include globs or pytest markers. Prefer net-negative production LOC. No replacement tests restating the same implementation.

## Validation

Never edit source or tests while a watcher runs. Run DB-backed and e2e suites only where AGENTS.md allows.
1) Run smallest owner and sibling tests with a name filter, then the touched suite.
2) For removed greps/plan assertions, run the script or dry-run that owns the real contract.
3) Lint and typecheck, including downstream consumers of changed shared types.
4) Inspect git diff --numstat; report production/tooling separately from tests and test support.
5) Run mstack-mode’s before-commit and before-review gates.

## Landing

Commit/push/PR only when authorized. Read <mstack>/skills/pr/SKILL.md and follow <mstack>/skills/mstack-mode/playbooks/shipping.md. One coherent PR at a time; after landing, refresh from current main and rerun read-only discovery.

## Handoff

Report: root cause and removed low-value categories; production owner simplifications; retained false positives and why; focused and full proof actually run; production vs test LOC; PR and merge state; named follow-ups.
