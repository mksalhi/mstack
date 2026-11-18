### Autopilot-stack

**You own the stack, never the landing. Hand the operator one linear stack of base-chained PRs to review and land.** **Autopilot-full** applies except for how verified work leaves. Each tick re-reads both playbooks under `<mstack>/skills/mstack-mode/playbooks/`; this one wins on conflict.

1. **Run Autopilot-full's owners, minus landing.** Owners report STACK-READY instead of merge-ready, and never rebase onto another branch (trunk included), retarget, merge, close a PR, or arm auto-merge. A dependent item branches from its dependency's branch.
2. **One topology writer: you.** Owners push only their own branches and report tip and intended parent. Only you rebase or retarget. Append clean PRs in dependency order, based on the parent branch (`origin pr edit <pr> --base <parent-branch>` or `gh pr edit <pr> --base <parent-branch>`); never require `gt`. Owners take your push as new base and lease, and resolve their own slice on conflict for you to push.
3. **Absorb drift at the root.** Until landing starts, apply Autopilot-full step 5's test per link and rebase bottom-up where needed (unless the Commits rule in `playbooks/opening-a-pr.md` forbids it), then the patch-id rule link by link.
4. **Deliver, then hands off.** Each link carries its verdict in its PR. Once landing starts, nobody writes to the chain except the post-merge retarget in `playbooks/shipping.md`. Mid-landing problems go through you to the operator; fixes wait for the operator's go.

**Which autopilot.** Full: independent PRs and landing authority granted. Stack: operator wants review first, work is sequenced or coupled, or merge authority is withheld.

**Reply:** per the `ketchup` skill, with links to stack root and tip, a one-line verdict per link, and anything parked or excluded with the reason.
