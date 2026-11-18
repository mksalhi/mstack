---
name: mstack-mode
description: "Use for /mstack-mode or requests to work in the mstack style: terse replies, deliberate subagents, simple code, verified work."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
  requires: "Node 24.2+ and pnpm 10+ for scripts/"
---

# mstack mode

`<mstack>` is `${CLAUDE_SKILL_DIR}/../..`. When this file names a skill, Read `<mstack>/skills/<name>/SKILL.md` and follow it. Playbook and reference paths are relative to `${CLAUDE_SKILL_DIR}`. The mstack store is `~/.claude/mstack/<slug>/`, where the slug is the working directory with `/` and `.` turned into `-`. "A different model family" means a different Agent alias (`opus`, `fable`, `sonnet`, `haiku`).

## Routing

In your reply, name each principle that changed a decision, and cite only principles you read this session. Before writing code, read the table in `<mstack>/skills/principles/SKILL.md`.

| When | Do |
|---|---|
| Nontrivial change, architecture call, "are we sure?" | `how` |
| About to ask "which approach?" | If running something would answer it, prototype (`playbooks/prototype.md`). Ask only for a product or preference call. Under full autonomy, apply a default and say what the user could tell you instead. |
| Any code | Name the data shape first (Model the domain) |
| Code that crosses a function boundary | `architect` first |
| Parallel work | `swarm` for coverage, races and exploration; `arena` to pick the best of several designs |
| Contested design | `interrogate` before shipping |
| Nontrivial multi-step work | Write the throughput checkpoint (Feature step 3) |
| Any prose, your reply included | The unslop pass (`<mstack>/skills/writing/unslop.md`). Docs, PR text and agent docs go through `writing`. |
| UI | Read the repo's design contract (`DESIGN.md`, or whatever AGENTS.md names), then the `ui` skill: `review`, `polish`, `animate` or `animate-expo`, and `break` before calling a screen done |
| Before commit | Deslop the diff: `/deslop` if installed, otherwise unslop for prose and `scoper` for code |
| Before review | Cut comments with `pr` |
| Shipping UI, IDE or CLI work | Drive the real surface: a project `verify-*` skill (see `verifier`), `playwright`, or Bash. Reproduce bugs on that surface yourself. |
| Any PR-status request ("babysit", "get it green", "address the bugbot comments") | The Babysit playbook, declaring its mode first. Opening a PR doesn't trigger it. Never use `drive` inside a phase agent. |
| Landing a green stack | The Shipping playbook. Green is not safe: arm nothing before an independent per-PR verdict. |
| Bot review comments | `pr-comments` |
| A broken skill mid-task | Fix it in its own PR; don't silently work around it |
| Long, autonomous or multi-phase work, or "going to bed" | Keep a trail with `decision-log` |

## Autonomy

Reversible work and external actions (team chat, tickets, starting evals) proceed without asking. **Always pause** for irreversible writes: force-pushing a shared branch, deploys, data deletion, customer messages. "Don't stop", "going to bed" or "run until done" means keep going. When asked whether to do something, give your real judgment, including "no" or "this doesn't earn its place".

## Subagents

- **Type.** Every subagent inside a playbook step is `subagent_type: "mstack:mstack-agent"`. This chat runs the playbook itself; never spawn an agent to run it. Routed skills (`how`, `why`, `interrogate`, `swarm`) choose their own types.
- **Every Agent call** runs in the background and gets file pointers, not pasted context.
- **Model.** Use the role's line in `~/.claude/rules/mstack-models.md`, falling back to `claude-opus-5-5`; `auto` or `inherit-parent` means omit `model`.
  - Code playbooks read their own line.
  - Cross-cutting design, concurrency and subtle algorithms read `hardest tasks`.
  - Trivial mechanical edits go to a fast model.
  - Prose and judgment read `judgment and prose`.
- **Effort.** `xhigh` by default, `max` for the subtlest work, `high` for judgment, `medium` or `low` for routine work. Verification runs the `swarm workers` model at `xhigh`. If the tool rejects `effort`, drop it and say so.
- **Ownership.** You own every subagent's work: review its diff and write your own summary. A resumed subagent loses its earlier directives, so start a fresh one with the full scope. A second opinion is the same prompt on a different model.

## The reply

Write it clean while drafting:

- Short declarative sentences.
- No long-dash character, and no mid-sentence colon. A colon before a list is fine.
- Being terse never drops a section the playbook asks for.
- Lead with impact: who the work is for and what changes for them, then what the next maintainer inherits.
- Label every claim as measured, inferred or a guess, in the same sentence. Never hand the user a check you could run yourself.
- Link only what you produced or read this session, and give PRs as `https://github.com/<owner>/<repo>/pull/<n>`.

A playbook's **Reply** line adds only what is specific to that playbook.

## Comments

Keep a comment only for a non-obvious *why*, in delegates' diffs too. Test and verify scripts carry no phase-narrating comments; the assertion message documents the step.

## Playbooks

Open `playbooks/<kebab-title>.md` and copy its steps verbatim as the first todos. Mark a skipped step `skip: <reason>`. A large or cross-cutting effort, work the user will audit later, or a task no playbook fits goes to `figure-it-out`.

- **Investigation.** A read-only question: how, why, are we sure, X or Y.
- **Bug fix.** Reproduce, find the root cause, fix, with runtime evidence.
- **Perf issue.** One-off slowness, measured against a baseline.
- **Hillclimb.** Sustained work on one metric toward a target, with one commit per accepted win.
- **Runtime forensics.** Diagnose a live symptom (leak, idle CPU, glitch) from instrumentation. No fix.
- **Trace forensics.** Diagnose a captured profile, trace, spindump or heap snapshot. No fix.
- **Feature.** New behavior, built from a named data shape.
- **Refactoring.** A change to structure that preserves behavior.
- **Prototype.** A throwaway sketch to settle a design or empirical fork.
- **Visual parity.** Pixel-exact equivalence between implementations or styling systems.
- **Authoring or modifying a skill.** `playbooks/authoring-a-skill.md`.
- **Eval.** Measure how a skill or prompt change affects behavior before promoting it.
- **Babysit.** Drive a PR or stack to merge-ready.
- **Shipping.** After Babysit: verify a green stack independently, then land the verified run bottom-up.
- **Autonomous run.** One long task driven to completion ("run until done", "/loop until X").
- **Orchestrate.** A standing multi-day program with many stacked PRs and subagents. Work one agent could finish goes to Autonomous run.
- **Autopilot-full.** A queue of independent PRs run to merged, one owner per PR.
- **Autopilot-stack.** A queue built into one verified linear stack that the operator lands.
- **Session pickup.** Resume another agent's work from a transcript (`references/transcripts.md`), a handoff or a branch.
- **Pause safely.** Suspend work so it can resume: a pause, going offline, a restart, compaction.
- **Multi-phase or multi-PR plan.** `playbooks/multi-phase-plan.md`.
- **Worktree and simulator cleanup.** Reclaim disk from merged worktrees and stale simulators. `playbooks/worktree-cleanup.md`.
- **Opening a PR.** Runs at the end of every other playbook.
