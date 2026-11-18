# Test-pruning campaign

Prune one subsystem's whole test surface (a workspace such as `backend/`, or a subsystem such as a voice pipeline) in one PR. The value bar, retention bar, candidate evidence, and validation in [SKILL.md](SKILL.md) apply to every lane. Don't start a step before the previous one's done-criterion holds.

## 1. Baseline

At a pinned `main` SHA, record test and support line counts and every test file's pass/fail state. Keep baseline failures in their own list: often real product bugs.

Done when every in-scope test file has a recorded baseline result.

## 2. Lanes and inventory

Split into **lanes** along production owner boundaries, not file prefixes (messaging: accounts, commands, inbound, outbound, persistence, transport, shared helpers, test harness). Include the subsystem's cases at shared core boundaries and its QA and live-proof harness tests.

Done when every test file and QA scenario the subsystem owns belongs to exactly one lane.

## 3. Read-only ledger per lane

One read-only agent per lane reads every assigned test in full (including parameter tables), plus production owners, entry points, callers, history, and the selecting test config. Each declaration gets one mark in a written **ledger**; an `it.each` / `pytest.mark.parametrize` is one declaration unless rows need different marks.

- `R`: retain, naming the contract and the bug it catches (a move to a better-named file stays `R`, move noted);
- `F`: retain the contract, repair the assertion (e.g. a vacuous negative that passes when only one of several items is missing);
- `C`: consolidate, naming the absorbing owner first: sibling table case, stronger boundary suite, or shared owner in another package;
- `D`: delete, naming the remaining proof or why no contract exists.

Judge by assertions, not names.

Done when every declaration has a mark and an evidence line.

## 4. Layer plan per lane

The ledger is input, not the edit list. A second read-only pass looks for the redundant **layer**: several suites replaying one shared helper through a mocked collaborator around stronger real-transport suites. Name the **keeper** suite per contract, preferring the real transport boundary with a fake network. Correct ledger errors found.

Done when each lane plan names retired files, the keeper per contract, assertions to carry into keepers, and test-only production seams unlocked.

## 5. Cutover

Edit lane by lane. Serialize changes to shared harnesses and support files through one owner. Remove each lane's unlocked test-only seams (injection parameters, getters, reset exports, indirection layers). Update vitest include globs or pytest markers if suites move. Put durable test-ownership rules, drawn from mistakes this campaign found, in the subsystem's `AGENTS.md`.

Done when every lane plan is applied and each lane's keepers pass.

## 6. Preservation review

Independent reviewers, one per boundary group, compare deleted coverage against keepers for contracts that lost their only proof, and for new assertions that cannot fail (a rejection row production never reaches).

For each restored contract, mutate the production owner once, confirm the keeper goes red, then restore the source byte for byte.

Done when every gap is restored or rejected with source evidence, and every restored contract has a caught mutation.

## 7. Product defects

A baseline failure surviving into a keeper is a bug. Fix it at its owner in a separate commit, proven through the real user flow with a **control** run that reverts the fix and shows the old behavior. Record unrelated discrepancies as follow-ups.

Done when each repaired defect has a failing control and a passing candidate on the same harness.

## 8. Reconcile and hand off

Merge `main` rather than rebasing. When `main` modified a file the campaign deleted, keep the deletion and port the new contract into the keeper; confirm every new `main` regression has a home. Rerun the whole subsystem suite and repeat live proof on the merged head. Review tooling may truncate the file list on a diff this large.

Hand off with the [SKILL.md](SKILL.md) report, plus:

- baseline and final test/support line counts, with production counted separately;
- lanes, retired layers, and keepers;
- preservation gaps found and their mutations;
- product defects with control and candidate proof.
