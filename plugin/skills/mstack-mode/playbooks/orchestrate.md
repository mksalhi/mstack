### Orchestrate

You own the program, never the code: write briefs, drain the queue, keep the frontier green, decide.
- Completions are queue events, not interrupts.
- Every spawn and resume carries the standing orders verbatim.
- The brief is the product. A worker cannot ask you a question.

#### Roles and placement
- Coordinator (this chat). Frames, briefs, drains, reports, decides. Never edits code; conflicted merges, chain rebases and code changes are units. It may land a verified unit itself by fast-forward or clean cherry-pick. Agents only through the Agent tool; state only through `orch` at drain points (`orch` never spawns, waits or wakes).
- Sub-coordinator. One per track. Owns its track’s units, briefs, workers and verifiers. Rolls up aggregates at wave boundaries, never raw child reports. In-flight cap about ten.
- Worker / verifier. `subagent_type: "mstack:mstack-agent"` with `isolation: "worktree"`, unless the task needs the main checkout (a verify-* or `playwright` run bound to local state, this project's transcripts, simulators, local-only auth). One writer per worktree or branch. Verifier on a different model family from its worker.
- Depth stays coordinator, track, worker (at most 3). Decompose tracks per project.

#### Store layout
`orchestrate/<project-slug>/` in the mstack store. One writer per file. Bookkeeping: `node scripts/orch/orch.ts` (`orch`).
- `preferences.md`: standing orders, numbered, one constraint per line.
- `overview.md`: durable PR and issue DB. Append, never rewrite wholesale.
- `units.tsv`: one row per unit (id, track, state, branch, PR, head SHA, brief path), updated in place.
- `frontier.json`: computed merge frontier, per Stack safety.
- `ledger.tsv`: verification ledger, per Verification.
- `inbox/`: completion pointers. `gates.md`: parked human gates.
- `decisions.tsv`: the trail via `decision-log`.
- `status.md`: regenerated from `units.tsv` and `ledger.tsv` at each drain.

#### The brief
A missing field means the unit is not scoped. Refuse to spawn it.
```
GOAL         one sentence, the outcome, executable by a stranger with no chat access
SCOPE        paths this unit may write; paths it may not; its exclusive worktree or branch
CONTEXT      pointers to files and PRs; upstream reports pasted in full when this unit
             depends on them, because workers cannot see siblings
ACCEPTANCE   checkable criteria, one per line
VERIFY       exact commands or the control-skill path, plus known gotchas
TIMEBOX      rough cap on runtime; on expiry, return partial findings and stop rather than run on
FORBIDDEN    no PR retargets or merges, no rebase, no force-push, no fixes outside scope,
             plus unit-specific bans
REPORT       status, branch, head SHA, PRs, verdict, what you actually ran, deviations,
             suggested follow-ups
STANDING     <preferences.md pasted verbatim>
```
- A one-command unit gets a paragraph: goal, scope, verify command, report shape.
- A sub-coordinator brief adds its track boundary, unit list, spawn budget, the drain protocol and the rollup format (per child: name, status, PR, head SHA, verdict, one line; plus track status and frontier delta).
- Audit one sampled worker brief per sub-coordinator per wave. A failure stops that track’s next refill until its instructions are fixed.
- Never resume-chain a brief. Respawn fresh with consolidated scope.

#### Steps
1. Frame. A countable done predicate, units, effort, stacks, wall-clock budget. If one agent could finish inside it, work directly. At about 70% of the budget, stop spawning and land what is verified. Name tracks; contested decomposition or one-way door goes through `arena`.
2. Install. `orch init`, open the trail via `decision-log`, write the standing orders, seed `frontier.json` with `orch frontier set --repo <repo-dir>` (`--forge origin` for Origin).
3. Pilot. Push one unit from brief to merge; fix the brief template, verify recipe and unit size from it before fan-out.
4. Scale. Rolling window up to the cap. Recompute ready work after each drain; relay upstream reports into downstream briefs; siblings talk only through you.
5. Drain. Run Queue and drain at every drain point.
6. Land. Continuously from the first verified unit. Heavy repos get a stacker from wave one. Keep the frontier green before upper-stack work; advance `frontier.json` only on merge or new head SHAs.
7. Close. Drain the inbox; reconcile every spawned agent to a terminal row; confirm the predicate on the real artifact and a verdict for every landed PR's current head; audit the trail via `decision-log`; encode recurring corrections into `preferences.md` or the brief template. Leave the store.

#### Queue and drain
- On a completion: `orch inbox push <agent> <unit> <status> [--report PATH]`. Never review a diff in a drain; a completion needing review becomes a verifier unit.
- Drain at brief, stack operation, gate, ledger or frontier update, a track rollup, a frontier watcher wake (`/loop`), and before a human report. Start with `orch inbox drain`; arrivals wait for the next drain.
- Each drain classifies every pointer (landed, needs-verify, failed, zombie, noise), writes rows with `orch unit add|set` and `orch ledger record`, runs `orch status`, and spawns the next wave in one message.
- At each rollup, account for every child: arrived, respawned, or scope absorbed. Never silently redo a missing child's work.
- A drain turn ends with `orch status`’s three lines (counts, changes, open gates).

#### Stack safety
- A stack is a base-branch chain (the Stacks rule in `playbooks/opening-a-pr.md`). Recompute `frontier.json` after every merge and stack change. It walks the PR base chain via `gh` and reads local refs, so run it from the stacker's clone.
- One stacker per stack, named in the standing orders, does every rebase, force-push, retarget, merge and close, as briefed units. Workers never do.
- One babysitter per stack (`playbooks/babysit.md`), scoped to one frontier generation, reports conflicts to the stacker instead of rebasing.
- One retro watcher follows merged PRs for reverts, post-merge CI breaks, and orphaned follow-ups.

#### Verification
- A cheap VERIFY command: the worker runs it and you spot-check receipts. A separate verifier only for expensive, judgment-laden or high-blast-radius checks.
- `ledger.tsv` has one row per verdict keyed by PR number plus head SHA: `live-ui-verified | unit-test-verified | type-check-only | verifier-blocked | verifier-failed`. CI green is an input, not a verdict. Behavioral work needs better than `type-check-only`. A verifier overrides a worker's self-report; a new head SHA voids the row.
- Externalize output as each unit lands: branch pushed, ledger row written, receipts in the store.

#### Liveness and failure
- Never resume an agent to check on it. Probe read-only: ledger, `units.tsv`, `gh`, pushed branches, `/tasks`.
- A silent death gets a synthetic postmortem row in the inbox. Replan as evidence arrives.
- Retry by mode: cap-hit or oom, respawn with smaller scope. Network-drop, retry as-is. Tool-error, retry on a different model. Unknown, retry once. After two retries, abandon and replan.
- A late zombie reconciles against the current frontier and ledger first. Salvage unique findings through a fresh unit, never a blind merge.
- If further spawning would produce garbage, put a stop line atop the standing orders, let in-flight work finish, fix the cause, clear it.
- After a few consecutive tool aborts of your own, write a handoff to the store (what's done, where, the exact resume command) and end the run.
- After a restart, branches and PRs persist: re-read standing orders and `units.tsv`, recompute the frontier, reattach work by PR, respawn sub-coordinators from their stored briefs, drain, resume. `orch` replaces a lock whose holder pid is gone.

#### Escalation
- To the human (parked in `gates.md`, work routed around): irreversible actions; product calls no experiment settles; a standing order contradicting reality; a dead end that survived a replan.
- Never to the human: frontier nudges, rebases, retries, CI flakes, review threads, formatting, out-of-scope asks, “should I keep going”. When in doubt, act and log. Mid-run discoveries fix only what blocks the frontier; the rest parks in follow-ups.

Reply at checkpoints and close, from `units.tsv` and `ledger.tsv`: the predicate and count, what each track landed, the frontier (PRs and SHAs), verdicts, what was abandoned and why, open gates (the only asks), store and trail paths, PR links.
