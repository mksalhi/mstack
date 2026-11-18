- One or two files with an obvious approach: skip the plan, say so, stop.
- Settle open questions by prototype (playbooks/prototype.md) before writing. Keep each branch, SHA, and screenshots for Appendix A. Ask the operator only a product or preference call no run can settle, with options (Never block on the human).
- Copy the skeleton below into the plan file (default the mstack store's docs/) and fill every placeholder. Keep every heading and sub-block in order. One section per PR, one PR per change with its own evidence (Prove it works). Name the execution playbook in How to read this: playbooks/autopilot-full.md or playbooks/autopilot-stack.md per the rule at the end of playbooks/autopilot-stack.md, or playbooks/orchestrate.md for a standing program.
- Run `node <mstack>/skills/mstack-mode/scripts/check-plan.mjs <plan.md>` and fix every line it prints (Encode lessons in structure).
- Post the plan path and the script output, then stop. Execution starts on the operator's explicit go, under the named execution playbook.

Verification rules

- Every verification block opens with the rule sentence in the template. The live block is mandatory: ten lanes at the PR head per the arena skill's swarm mode on the swarm workers model (default `claude-opus-5-5`), each one box with scenario, saved screenshot, and pass predicate.
- Lane 1 and perf compare trunk with head. Never invent a trunk result, and never claim a ratio between unlike scenarios.
- A PR that changes an interaction is review-gated (operator reviews screenshots and a video in chat before merge). Otherwise write `**Review gate.** None. <PR id> is not review-gated.` with no boxes.
- Control skill by surface: web, browser, and Electron use a project verify-* skill or `playwright`; CLIs and TUIs a verify-* skill or Bash; native mobile the repo's simulator-driving skill. Two surfaces get lanes on both. A surface with no control skill is an Appendix C risk, and its live block still says how each lane drives it.

````markdown
# <Program> plan

<Under ten lines. What changes, for whom, the rule enforced, the PR ids in order.>

## How to read this

One box is one unit of work. Every box names the evidence that checks it. A nested box is a sub-step of the box above it. Check a box only when its evidence exists, a file, a log line, a screenshot, a test run, or a SHA. The body is a how-to. The appendices explain and record.

The program runs `<mstack>/skills/mstack-mode/playbooks/<execution playbook>.md`. <Who merges, and which PR ids are the operator's items that stop at merge-ready.>

Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

## Program checklist

### Arm the program

- [ ] State the protocol and this plan to the operator, then stop. Start execution only on the operator's explicit go.
- [ ] On the operator's go, arm a `/goal` with this exact text. "<The plan path, the PR ids in order, the verification rule, who merges, and the done condition.>"
- [ ] Read these from trunk at start and at every tick.
  - [ ] `cat <mstack>/skills/mstack-mode/playbooks/<execution playbook>.md`
  - [ ] `cat <mstack>/skills/arena/SKILL.md`
  - [ ] `cat <control skill path>`
  - [ ] `cat <mstack>/skills/mstack-mode/playbooks/opening-a-pr.md`
  - [ ] `cat <mstack>/skills/<name>/SKILL.md` for each other skill the program uses
- [ ] Arm the 30-minute audit tick as a real terminal `/loop`, never from memory.
- [ ] Use this tick prompt, verbatim. "Re-read the execution playbook from trunk and the armed /goal. Audit the operation against both and fix drift now. Probe every active lane and judge progress by side effects only. Stand down a stuck lane and dispatch its replacement. Post a short status message to the operator only for tracked changes no earlier status message reported (PR opened, code-ready head, round launched or closed, verdict, merge, stuck agent and the action taken, blocker added or cleared, decision only the operator can make). Name those and nothing else. If there are none, end the turn with no reply text. Either way, log this tick's row in your decision trail, naming the items reported or none."
- [ ] On the operator's hold or stand-down, send every owner a zero-writes order at once.

### Spawn owners

- [ ] Spawn one owner per PR with the lifecycle the execution playbook names.
- [ ] Follow this dependency graph. Dependent work starts after its parent merges, or bases on the parent branch when the playbook stacks.
  - [ ] <PR id> and <PR id> are independent and first. Both branch from `main`.
  - [ ] <PR id> after <PR id>.
- [ ] Hold the file boundaries. <PR id or class> touches only `<glob>`.
- [ ] Hold the review gate. <PR ids> change an interaction and wait for the operator's review in chat with screenshots and a video.

### PR mechanics, for every PR

- [ ] Resolve the forge once. Default `gh`; if `command -v origin` succeeds and Origin resolves the repository, use `origin pr` for every PR operation. Record any fallback to `gh`. Never require `gt`.
- [ ] Open the PR ready, never draft, with `origin pr create --status open --base <base-branch>` or `gh pr create --base <base-branch>`. A stack child targets its parent branch.
- [ ] Run the repo's lint and typecheck once before the PR-facing push. Push with hooks on.
- [ ] Deslop before each commit and cut comments before review, per the mstack-mode Routing table.
- [ ] Triage every Bugbot and security-reviewer comment with the `pr` skill's bot-thread triage.
- [ ] Rebase onto current trunk before the code-ready report and babysit, and keep that base in fix rounds. Rebase again only at merge prep, on a `git merge-tree` conflict with trunk, or on a CI failure caused by trunk.

### Verdict and merge, for every PR

- [ ] Run a full swarm per `<mstack>/skills/arena/SKILL.md` (swarm mode) once, at the code-ready head, and again only for new behavior, a redesign, or a large new diff. A rebase, conflict resolution, or minor fix gets a single verifier at the new head. Lanes are one gates lane, the ten **Verify, live** lanes, the **Verify, perf** lane, and two or more audit lanes with distinct focus that read the diff and receipts and distrust the PR body. The root audits the merge-ready report's receipts before the verdict.
- [ ] Clean only when every lane is `PASS`. Findings, including a defect filed as a note, go back to the owner. A new head gets a fresh verdict, except results still valid under the patch-id rule in `playbooks/shipping.md`.
- [ ] <The merge or append rule from the execution playbook, with the patch-id rule from `playbooks/shipping.md`.>

### Boot recipe, for every live lane

Each live lane runs in its own worktree at the PR head. Drive through the control skill above.

- [ ] `git fetch origin <head-branch> && git checkout <head SHA>`.
- [ ] <Start the backend and the surface. Wait for ready.>
- [ ] <Deliver input only through the control skill's commands. Name the read-only diagnostics.>
- [ ] Save every screenshot to `<mstack store>/swarm-<pr-id>/worker-<n>/<slug>.png` and return the paths with the report.

## <Task as a verb phrase> (<PR id>)

**Depends on.** <PR id, or None.>

**Files.**

- [ ] Edit `<path>`.
- [ ] Create `<path>`.
- [ ] Delete `<path>`.

**Build.**

- [ ] <One change. Name the symbol and the file.>

**You see.**

- [ ] <One observable result, with the exact log line or screen state.>

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] <Test file and the case it gains.> Run `<command>`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `<swarm workers model>` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run <the same load-bearing scenario> at trunk and head. If trunk lacks the feature, record that and gate <the behavior the diff adds plus the end state the user waits for>. Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 2. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
<Lanes 3 to 10 as boxes in the same form.>

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. <Measured at trunk and head. If trunk lacks the feature, also the diff-added work and the end state the user waits for.>
- [ ] Probe. <Command or procedure, run at trunk and head interleaved. Both sides produce the metric.>
- [ ] Baseline. Record the trunk <value> first.
- [ ] Rule. <Head against trunk, with the number that fails. If scenarios differ, absolute budgets for the diff-added work and user-visible end state, not a ratio.>

**Review gate.** The operator reviews before merge.

- [ ] Copy lane <n> screenshots into `<media path>/<pr-id>-review-<slug>.png`.
- [ ] Record a 30 to 60 second video of the change in a lane worktree. Save it as `<media path>/<pr-id>-review.mp4`.
- [ ] Post the screenshots and the video in chat. Stop at merge-ready. Wait for the operator's click.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Rebased onto current trunk after the verdict, patch-id unchanged.
- [ ] <The owner squash-merges its own PR, or the root appends it to the base-branch stack and the operator lands it bottom-up.>

## Close the program

- [ ] Every box above is checked with its evidence.
- [ ] Reply to the operator with the report the execution playbook names.

## Appendix A. Prototype evidence

<Each open question a prototype answered, with the branch, the SHA, and the artifact links. Each question that stays unproven.>

## Appendix B. Alternatives rejected

<Each approach weighed and why it lost.>

## Appendix C. Risks

<Each risk with the PR it lands in and what the owner watches.>

## Appendix D. Links and reading list

<Docs to read before editing. Which PRs get `<mstack>/skills/how/SKILL.md` and `<mstack>/skills/interrogate/SKILL.md`. The trail per `<mstack>/skills/decision-log/SKILL.md`.>
````
