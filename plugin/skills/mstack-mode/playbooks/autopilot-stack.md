### Autopilot-stack

You own the stack, not landing. Hand one linear base-chained stack. Playbooks reload each tick from <mstack>/skills/mstack-mode/playbooks/>; this one wins on conflict.

- Owners: report STACK-READY; never rebase onto another branch (incl. trunk), retarget, merge, close, or arm auto-merge.
- Only you write topology/rebase/retarget. Owners push only their branches and report tip+intended parent. Append clean PRs in dependency order (`origin pr edit <pr> --base <parent-branch>` or `gh pr edit <pr> --base <parent-branch>`); never require `gt`.
- Until landing, absorb drift at root: run Autopilot-full step 5 test per link; rebase bottom-up if needed (unless `playbooks/opening-a-pr.md` Commits rule forbids), then apply patch-id.
- Deliver, then hands off: once landing starts, nobody writes except the post-merge retarget in `playbooks/shipping.md`. Mid-landing problems go through you to the operator; fixes wait for the operator’s go.

Reply per `handoff` catch-up: links to root and tip, one-line verdicts, and any parked/excluded with reason.
