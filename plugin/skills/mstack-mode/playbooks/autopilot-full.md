### Autopilot-full

You own verdicts, never PRs. One owner carries each PR from build to merge; nothing merges until your swarm, which never wrote the code, has proven what lands.

1) Operator gates first. The grant covers only the queue’s items; items the operator claims and PRs outside the queue stop at merge-ready. A request to state the plan is not a go. On an explicit go, arm a `/goal` with the full program objective.

2) One owner per PR. Resolve the forge once per `playbooks/opening-a-pr.md`. Each owner is a `mstack:mstack-agent` (`isolation: "worktree"`) that builds, opens its PR per `playbooks/opening-a-pr.md`, proves on the real artifact, babysits per `playbooks/babysit.md`, and merges once 4–5 clear.
- Open the PR early. Code-ready = after deslop and `/mstack:pr`; rebase onto current trunk and report the code-ready head before self-proof. Report every later head; report merge-ready only after self-proof, CI, and babysit.
- Run the repo’s checks for touched paths on the committed head before the code-ready push and any later push that needs a verifier.
- Assume the agent dies. Push early and start a decision-log in the root’s mstack store (absolute path in the brief); push after every unit worth keeping. Record spawned subagent id, state, and a stuck-after runtime. Force-push only your own branch with `--force-with-lease` pinned to your last pushed or taken-over SHA (unless the Commits rule in `playbooks/opening-a-pr.md` forbids it). On a push you did not make, stop and report to the root.

3) Owners run in parallel off trunk, never stacked.

4) Swarm-verify once at the code-ready SHA. Re-swarm only for new behavior, a redesign, or a large new diff; otherwise one verifier at the new head (the patch-id rule in `playbooks/shipping.md` may carry a lane; every head needs green CI). Lanes re-run the gates, prove load-bearing behavior live (project `verify-*` skill, `playwright`, or Bash), and audit the diff. No clean verdict without the live lane and your audit of the merge-ready report’s receipts.
- Send all proven findings in one fix-forward with a red test across every site sharing the defect. A defect already on trunk is recorded against trunk and does not gate; one the PR copies or newly reaches is the PR’s. Never push a fix yourself; replace a stuck owner.

5) Merge only what you verified, on the trunk it lands on. Green CI never authorizes a merge alone. Merge prep rebases onto trunk, reports the head, waits for green CI. Right before merging, fetch trunk:
- Untested code would land: rebase, wait for CI.
- Lockfile both sides changed: skip the rebase if a frozen install passes on the merge result and the PR’s packages resolve as on the head; otherwise rebase and repair.
- Trunk changed a caller or dependency of the patch: run the patch’s checks on the merge result, merge on pass.
- Otherwise merge. A third rebase past merge prep: hold and report to the root.

6) Root layer. Any loosened gate (raised budget, allowlist entry) needs a verifier’s proof plus your fresh countersign; the owner’s record points at it. Disabled or soft-failed checks always come out. Never give or bypass a forge-enforced approval.
- On the operator’s go, arm an audit tick about every 30 minutes: a real terminal `/loop` with a monitored-shell 30-minute sleep emitting an output-notification sentinel. Each tick re-reads `cat <mstack>/skills/mstack-mode/playbooks/autopilot-full.md` and the `/goal`; has owners record drift (unreported head, unrecorded agent); probes every agent to leaf lanes, judged by side effects, not status text. Stuck: errors, cannot start turns, nothing new past its stuck-after runtime, or an owner with no push or trail row by the first tick. Waiting on you or the operator is not stuck; answer it. Replace stuck agents at once. Catch the operator up per `handoff` catch-up mode only when the tick changed something.

7) Operator stop: stand down at once. Every owner gets a zero-writes order, reports where it stands, and keeps its brief until released.

Reply: per `handoff` catch-up mode: each PR’s state and verdict, what merged, countersigns and why, open operator gates, with links to PRs and trails.
