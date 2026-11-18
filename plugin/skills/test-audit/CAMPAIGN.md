# Test-pruning campaign

Prune one subsystem’s whole test surface in one PR. The value bar, retention bar, candidate evidence, and validation in [SKILL.md](SKILL.md) apply. Don’t start a step before the previous is done.

1. Baseline
- At a pinned main SHA, record test/support line counts and each in-scope test file’s pass/fail.
- Keep baseline failures in a separate list.
- Done: every in-scope test file has a recorded baseline result.

2. Lanes and inventory
- Split by production owner (not file prefixes).
- Include the subsystem’s cases at shared core boundaries, plus its QA and live-proof harness tests.
- Done: every test file and QA scenario belongs to exactly one lane.

3. Read-only ledger per lane
- A read-only agent reads every assigned test in full (incl. parameter tables), owners, entry points, callers, history, and the selecting test config.
- Each declaration gets one mark; an it.each / pytest.mark.parametrize is one declaration unless rows need different marks.
- Marks:
  - R: retain; name the contract and the bug it catches (moves stay R; note move).
  - F: retain the contract; repair the assertion.
  - C: consolidate; name the absorbing owner first.
  - D: delete; name the remaining proof or why no contract exists.
- Judge by assertions, not names. Add one evidence line per declaration.
- Done: every declaration has a mark and evidence.

4. Layer plan per lane
- Find redundant layers around stronger real-transport suites. For each contract, name the keeper, preferring the real transport boundary with a fake network. Correct ledger errors.
- Done: plan lists retired files, keeper per contract, assertions to carry into keepers, and unlocked test-only seams.

5. Cutover
- Edit lane by lane. Serialize shared harness/support edits through one owner.
- Remove unlocked test-only seams (injection parameters, getters, reset exports, indirection layers).
- Update vitest include globs or pytest markers if suites move.
- Put durable test-ownership rules in the subsystem’s AGENTS.md.
- Done: plan applied per lane and keepers pass.

6. Preservation review
- Independent reviewers (per boundary group) compare deletions vs keepers for lost-only proofs and for assertions that cannot fail.
- For each restored contract, mutate the owner once, confirm the keeper goes red, then restore the source byte for byte.
- Done: every gap is restored or rejected with source evidence, and every restored contract has a caught mutation.

7. Product defects
- Any baseline failure surviving into a keeper is a bug.
- Fix at its owner in a separate commit, proven through the real user flow with a control run that reverts the fix and shows the old behavior. Record unrelated discrepancies as follow-ups.
- Done: each repaired defect has a failing control and a passing candidate on the same harness.

8. Reconcile and hand off
- Merge main (don’t rebase). If main modified a file the campaign deleted, keep the deletion and port the new contract into the keeper; confirm every new main regression has a home.
- Rerun the whole subsystem suite and repeat live proof on the merged head.
- Hand off with the [SKILL.md](SKILL.md) report, plus: baseline and final test/support line counts (production counted separately); lanes, retired layers, and keepers; preservation gaps found and their mutations; product defects with control and candidate proof.
