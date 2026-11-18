### Shipping

Own what lands. Verify each PR independently; land only the contiguous verified run from the root; keep hands off while it lands.

- Verification: One non-author verifier per PR posts PASS, PASS+NOTES, or FAIL. Green CI/bot approvals are not verdicts.

- Pick the run: From the lowest unmerged PR, include contiguous PASS/PASS+NOTES until the first gap; its top is the ceiling.

- Re-check verdicts: Compare `git patch-id` at verdict SHA vs head. If only tests/docs/lint changed and target builds identically except noise (report kinds with files), the lane stands. Fresh checks/review for changed parts; rerun lanes with no build output (dev server); re-verify anything else that drifted.

- Land bottom-up, one PR at a time:
  - Merge the lowest: `gh pr merge <pr> --squash`. Confirm with `gh pr view <pr> --json state,mergedAt,baseRefName`; landed means merged to trunk (queued/auto-merge ≠ landed). Use `--auto` only when the verdict covers the current head.
  - Retarget next PR to trunk: `gh pr edit <pr> --base <trunk>`; move its patch onto the merge result, push `--force-with-lease`, re-apply re-checks, then merge.

- Hands off while it lands: Only the move above. `scripts/watch-pr/watch-pr --queued-stack --stack-prs <bottom-to-top>` under `/loop` until `COMPLETE`. If a merge stalls, diagnose before changing anything.

- Stop at the ceiling; extending the run restarts at forge.

Reply: run and ceiling; each verdict+producer; what landed+how confirmed; what the next gap needs.
