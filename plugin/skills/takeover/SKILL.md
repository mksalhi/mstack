---
name: takeover
description: "Use to finish someone else's PR, branch or agent thread while keeping their credit ('take over'), or to bring an old PR up to date and decide if it should still exist ('modernize', 'rebase this old PR')."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Takeover

Two modes. **Take over**: finish another person's or agent's work toward its original goal. **Modernize**: update an old PR against today's base and judge whether it still belongs. A takeover usually runs Modernize first. Infer the mode from the ask and say which.

## Rules for both modes

- Fetch first: the PR head, the base and any related branch. Treat existing worktree changes as the user's; work in a fresh worktree when the active one is dirty or busy.
- Update branches with `--force-with-lease` pinned to the head you observed before rewriting. If the lease fails, fetch and reassess; never overwrite new work.
- This skill never merges, closes a PR, changes its base, or widens its scope unless the user asked for that.
- Report observed facts apart from judgment, and say what you could not verify.

## Modernize

Modernize the idea, not just the branch. A clean rebase does not prove the PR still belongs in the product.

1. **Establish intent.** Record the PR URL, state, base, head branch and SHA, author, checks and review state. Read the title, body, linked issues, commits, review threads and the full diff. Write the smallest goal the PR was after before judging how it does it. Record the merge base.
2. **Check what moved around it.** Read the base's commits since the merge base, and search merged and open PRs for a replacement. Ask: was the same user problem already solved? Did APIs, types, schemas or boundaries change? Do both sides now own the same behavior? Was the touched code deleted, moved or simplified? Would landing it restore old behavior or add a second way to do something? Is the benefit still worth the upkeep? No Git conflicts is not evidence the PR is current.
3. **Pick a verdict before pushing anything.**
   - **MODERNIZE**: the goal holds and the shape is right. Rebase, resolve, test, push.
   - **REWORK**: the goal holds but a mechanical rebase would keep the wrong shape. Do the rewrite on a new branch with behavior pinned first, then push it; a rewrite is cheap once proof exists. Stop at a description only when the user asked for a verdict alone.
   - **CLOSE**: superseded, obsolete, wrong direction, or no longer worth it. Cite evidence and stop; never close without permission. Age alone is not evidence, and sunk effort is not a reason to keep it.
4. **Rebase without losing intent** (MODERNIZE only). Rebase a copy at the recorded head onto the fresh base. Resolve each conflict by the PR's intent and the base's newer invariants; a conflict that is really a product or architecture disagreement sends you back to step 3. Compare old and new series with `git range-diff` and read the final diff: nothing intended disappeared, nothing already landed came back. Run the repo's checks for the touched area, telling real failures from pre-existing or infra ones. Push per the rules above.

Done when the verdict is stated with evidence and, for MODERNIZE, the rebased branch is pushed with checks run.

## Take over

Own the original goal, not the original implementation: don't defend code just because another agent wrote it.

1. **Resolve the handoff to code.** Read the source PR, branch or thread, including review findings and the user's later corrections. Find the actual current head and any uncommitted work. The handoff is context, not proof.
2. **Continue on the right branch.** For a replacement PR, bring the original commits onto a new branch and add your fixes as separate commits. Honor an explicit in-place or stacked continuation instead. Never overwrite unrelated work or change the original PR without permission.
3. **Keep the credit.** Preserve Git authorship and existing `Co-authored-by` trailers. Credit the original contributors in the PR body and link the original PR. If the work will be squashed, carry human author credit into the squash commit with verified identities, never guessed emails. Model attribution does not replace contributor credit.
4. **Bring it current.** Run Modernize against the intended base. Rework only what finishing the same goal needs; simplify without dropping intended behavior. Recheck the source PR before you finish, since it may have moved while you worked.
5. **Prove it.** Reproduce the original failure and drive realistic workflows yourself, per the repo's rules. Green mocked tests don't prove the user experience. State what stays unverified.
6. **Finish.** If the finish includes a PR, open or update it per the `pr` skill, then babysit it (`mstack-mode` Babysit playbook) instead of stopping at creation. Merge or close the original only when the user authorized it.

**Reply:** lead with the verdict (MODERNIZE, REWORK or CLOSE) or what you inherited; then what changed on the base, conflicts found, what you changed, checks and proof, how credit was kept, the PR link, and the decision left for the user.
