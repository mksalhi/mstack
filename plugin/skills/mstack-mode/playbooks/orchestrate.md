### Orchestrate

**You own the program, never the code. Author briefs, drain the queue, keep the frontier green, decide.** On cheap near-identical units, collapse ceremony as each section directs.

- Completions are queue events, not interrupts.
- Every spawn and every resume carries the standing orders verbatim.
- The brief is the product. A worker cannot ask you a question.

#### Roles and placement

- **Coordinator (this chat).** Local. Frames, briefs, drains, reports, decides. Never edits code; conflicted merges, chain rebases, and code changes are tasks. Where local git is cheap it may land a verified unit itself (fast-forward or clean cherry-pick, then push). Agents go only through the Agent tool; state only through `orch` at drain points (it never spawns, waits, or wakes anything).
- **Sub-coordinator.** Local, durable, one per track, only past what one coordinator can drain. Owns its track's units, briefs, workers, and verifiers (nesting to depth 3). Rolls up aggregates at wave boundaries, never raw child reports. In-flight cap roughly ten, as a rolling window, never blocking batches.
- **Worker / verifier.** `subagent_type: "mstack:mstack-agent"` with `isolation: "worktree"`, unless the task needs the main checkout (runtime verification bound to local state such as a project verify-* skill or the `playwright` skill, reading this project's transcripts, simulators and local IDE state, auth that exists only here). Prefer fewer, broader workers. One writer per worktree or branch (Separate before serializing shared state). Verifier on a different model family from its worker.

Depth stays coordinator, track, worker. Decompose tracks per project; no hard-coded swarm trees.

#### Store layout

Create `orchestrate/<project-slug>/` in the mstack store. Every file has one writer; readers aggregate. Bookkeeping uses `node scripts/orch/orch.ts` (`orch` below).

- `preferences.md`: standing-orders register, numbered lines, one constraint each (model policy, stack shape and count, verification bar, forbidden paths, escalation policy). Paste verbatim into every spawn and resume. When you catch yourself restating an instruction, append the line before you act (Encode lessons in structure).
- `overview.md`: durable PR and issue DB. Append, never rewrite wholesale.
- `units.tsv`: one row per unit (id, track, state, branch, PR, head SHA, brief path), updated in place.
- `frontier.json`: computed merge frontier, per Stack safety.
- `ledger.tsv`: verification ledger, per Verification.
- `inbox/`: completion pointers. `gates.md`: parked human gates (question, options, default on no answer).
- `decisions.tsv`: the trail via `decision-log`.
- `status.md`: regenerated from `units.tsv` and `ledger.tsv` at each drain, never hand-maintained.

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

- A one-command unit gets a paragraph naming goal, scope, verify command, and report shape. Spawns may cite the standing orders by store path; resumes paste them verbatim.
- A sub-coordinator brief adds its track boundary and unit list, spawn budget with the worktree default and main-checkout exceptions, the drain protocol, and the rollup format (per child: name, status, PR, head SHA, verdict, one line, plus track status and frontier delta).
- Audit one sampled worker brief per sub-coordinator per wave, alongside the wave, never as a gate. A failure stops that track's next refill and fixes the sub-coordinator's instructions.
- Never resume-chain a brief. Respawn fresh with consolidated scope.

#### Steps

1. **Frame.** State the done predicate as something countable ("all 126 units merged, each ledger-verified `unit-test-verified` or better"). Quantify units, effort, stacks, and wall-clock budget. If one agent could finish inside it, work directly in this session with plain workers, inline verification, and landing as you go, without the store or pilot machinery. At roughly 70% of the budget, stop spawning and land what is verified. Name the tracks; a contested decomposition or one-way door goes through `arena` first. Present the framing once; reversible prep does not wait.
2. **Install the runtime.** Run `orch init`. Open the trail via `decision-log`, write the standing orders before any spawn, and seed `frontier.json` from existing PRs with `orch frontier set --repo <repo-dir>`, adding `--forge origin` when the forge is Origin.
3. **Pilot.** Push one unit through brief, worker, verification, stack entry, ledger row, and merge; fix the brief template, verify recipe, and unit size from its evidence before fan-out. For cheap clone units the first normal unit is the pilot. A separate verifier and audit gate only for expensive or novel units.
4. **Scale.** Rolling window up to the in-flight cap. Sub-coordinators only past the threshold in Roles. Recompute ready work after each drain, relay upstream reports into downstream briefs, keep sibling communication upward.
5. **Drain.** Run Queue and drain at every drain point.
6. **Land.** Continuously from the first verified unit, never a final phase. Heavy repos get a standing stacker from wave one. Keep the frontier green before upper-stack work. Advance `frontier.json` only on merge or reported new head SHAs.
7. **Close.** Drain the final inbox, reconcile every spawned agent to a terminal row (done, abandoned, zombie-reconciled), confirm the predicate on the real artifact, confirm every landed PR has a verdict for its current head SHA, audit the trail per decision-log with its cross-model review, encode recurring corrections into `preferences.md` or the brief template. Leave the store intact.

#### Queue and drain

- On a completion notification, run `orch inbox push <agent> <unit> <status> [--report PATH]` and return to what you were doing. Never review a diff inside a drain; a completion that needs review becomes a verifier unit.
- Drain in batches at four points: end of a critical section (brief, stack operation, conflict decision, gate, ledger or frontier update), a track rollup, a frontier watcher wake (armed via `/loop`, with a long heartbeat fallback), and before a human report. Begin with `orch inbox drain`. Arrivals during a drain wait for the next.
- Each drain classifies every pointer (landed, needs-verify, failed, zombie, noise), writes rows through `orch unit add`, `orch unit set`, and `orch ledger record`, runs `orch status`, then spawns the next wave in one message.
- At each track rollup, account for every spawned child: arrived, respawned, or scope explicitly absorbed. Never silently redo a missing child's work.
- A drain turn ends with the three lines from `orch status` (counts against states, what changed, gates open). The full reply contract applies only at checkpoints and close.

#### Stack safety

- A stack is a base-branch chain (the Stacks rule in `playbooks/opening-a-pr.md`). Never require Graphite.
- Recompute `frontier.json` after every merge and stack mutation: ordered PR list, branch names, head SHAs, generation number, lowest unmerged PR. The command walks the PR base chain through the checkout's current branch via `gh` (pass `--forge origin` for Origin) and reads head SHAs from local refs, so run it from the stacker's clone. A branch with no PR errors.
- Exactly one stacker per stack mutates topology (chain rebases, force-pushes, base retargets, merges, PR closes), serialized within its stack. Record the holder in the standing orders. Merges and stack surgery are briefed units.
- Workers never rebase, retarget, or merge PRs. Babysitters follow `playbooks/babysit.md`, one per stack, scoped to one immutable frontier generation, and report conflicts to the stacker instead of rebasing.
- One retro watcher follows merged PRs for reverts, post-merge CI breaks, and orphaned follow-ups.

#### Verification

- A cheap single VERIFY command: the worker runs it, the coordinator spot-checks receipts. A dedicated verifier only for expensive, judgment-laden, or high-blast-radius verification.
- `ledger.tsv`, written with `orch ledger record` and checked with `orch ledger check`, has one row per verdict keyed by PR number plus head SHA: `live-ui-verified | unit-test-verified | type-check-only | verifier-blocked | verifier-failed`. CI green is an input, not a verdict. Behavioral work needs better than `type-check-only`. `verifier-blocked` is not a pass; respawn when the environment heals. `verifier-failed` gets a fix unit, not a re-verify. A verifier overrides a worker's self-report on the same key. A new head SHA voids the row. The ledger, not memory, answers "was this verified".
- Externalize output the moment a unit lands, never batched: the worker pushes its branch, the verifier writes its ledger row, receipts land in the store.

#### Liveness and failure

- Never resume an agent to check on it. Probe read-only: the ledger, `units.tsv`, `gh`, pushed branches, `/tasks`. Transcript mtime is not liveness.
- A silent death gets a synthetic postmortem row in the inbox (unit, failure mode, last evidence, options). Replan on evidence as it arrives, never waiting for full quiescence.
- Retry by mode: cap-hit or oom, respawn with smaller scope. Network-drop, retry as-is. Tool-error, retry on a different model. Unknown, retry once. After two retries, abandon the unit and replan around it.
- A late zombie reconciles against the current frontier and ledger first. Salvage unique findings through a fresh unit, never a blind merge.
- When continued spawning would produce garbage tree-wide (bad upstream output, broken acceptance, dead infra), write a stop line at the top of the standing orders, let in-flight work finish, fix the cause, clear it.
- Bound your own infra retries too. After a few consecutive tool aborts, write a terminal handoff to durable state (what is done, where it lives, the exact resume command) and end the run.
- After a Claude Code restart, agents are dead but pushed branches and PRs are not. Re-read the standing orders and `units.tsv`, recompute the frontier, reattach work by PR and branch, respawn one sub-coordinator per track from its stored brief plus current state, drain, resume. `orch` replaces a store lock whose holder pid is gone.

#### Escalation

- Reaches the human, batched into the status page: irreversible actions (force-push to shared branches, deploys, deletions, closing someone else's PR), product or preference calls no experiment settles, a standing order contradicting observed reality, a program-level dead end that survived a replan. Park each in `gates.md` before asking and route work around it.
- Never reaches the human: frontier nudges, rebase mechanics, retries, CI flake triage, review-thread triage, format fixes, scope the brief forbids (refuse and continue), "should I keep going". When in doubt, act and log.
- Mid-run discoveries fix only what blocks the frontier. Everything else parks in follow-ups.

**Reply:** at checkpoints and close, from `units.tsv` and `ledger.tsv`, not narrative: the predicate and count against it, tracks and what each landed, the frontier (PR list plus SHAs), verdicts summary, what was abandoned and why, gates awaiting the human (the only asks), store path, trail path, PR links.
