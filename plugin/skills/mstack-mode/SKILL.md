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

**Claude Code runtime.** `<mstack>` is `${CLAUDE_SKILL_DIR}/../..`. For every skill named here, Read `<mstack>/skills/<name>/SKILL.md` and follow it. Playbook and reference paths resolve against `${CLAUDE_SKILL_DIR}`. The mstack store is `~/.claude/mstack/<slug>/` (working directory with `/` and `.` turned into `-`). Subagents run through the Agent tool with Claude model aliases (`opus`, `fable`, `sonnet`, `haiku`). Where mstack asks for a different model family, pick a different alias.

## Non-negotiables

In your reply, name each principle that shaped a decision and the choice it changed. Cite only principles you read this session.

- Nontrivial change, architecture decision, or "are we sure?" → `how`.
- About to ask the user "which approach" or "what should this do" → if running something could answer it (behavior, timing, layout, output, perf), sketch it via `playbooks/prototype.md` and let the result decide; in a read-only Investigation, answer from the evidence. Ask only for a product or preference call no experiment can settle. Under full autonomy, decide, act and report; for a call only the operator can make, apply a default, explain it, and say in plain words what they could tell you instead. Gates the operator named and the Always-pause list still wait for them.
- Any code → name the data shape first, organized per Model the domain.
- Code crossing a function boundary → `architect` before implementing.
- Parallel fan-out → `swarm` for coverage, races and exploration; `arena` to pick the best of several designs or implementations.
- Contested design → `interrogate` before shipping.
- Nontrivial multi-step → write the throughput checkpoint (Feature step 3).
- Any prose, your reply included → the unslop pass (`<mstack>/skills/writing/unslop.md`); the reply also follows **Writing the reply**. Docs, RFCs, READMEs, PR and commit text, and agent docs → `writing`.
- UI work → read the repo's design contract first (`DESIGN.md` or the design doc its AGENTS.md names). Then the `ui` skill's areas (`/mstack:ui <area>`): `review` (pulls in accessibility, colors, copy, layout, polish, typography), `polish`, `animate` (web) or `animate-expo` (mobile) for motion, and `break` to stress the data before calling a screen done.
- Before commit → deslop the diff (`/deslop` if installed, else the unslop pass for prose plus `scoper` for code).
- Before review → cut comments with `pr` (`/mstack:pr`).
- Shipping UI / IDE / CLI → the matching control skill: a project `verify-*` skill (see `verifier`), or drive the surface directly (Bash for CLIs, `playwright` or a browser MCP for web UIs). For bug fixes, reproduce first on the same surface yourself. Hand to the user only under the Bug fix step 1 exception.
- Any PR-status request ("babysit this", "get it green", "address the bugbot comments", "check on PR X") → the **Babysit** playbook, not another skill matching the same words. Opening a PR doesn't trigger it. Declare its mode (its step 1) before polling. Don't use `drive` inside a phase agent: the agent can't finish its turn.
- Land or ship a green stack → the **Shipping** playbook. Green is not safe. Nothing gets armed before an independent per-PR verdict, and only the contiguous verified run from the root lands.
- Bot review comments → triage every thread with `pr-comments`; dismiss noise with a concrete reason instead of churning code.
- Broken skill mid-task → fix it in its own PR. Don't block, don't silently work around it.
- Long, autonomous or multi-phase work, or work the user steps away from ("going to bed", "/loop until X") → keep a trail with `decision-log`.

## Principles

The principles and their one-line rules are the table in `<mstack>/skills/principles/SKILL.md`; read it at the start of any task that writes code. Scoper, Fix root causes (`debug`) and Test audit (`test-audit`) are skills.

## Autonomy

**Just do it.** Use any MCP tool. Reversible work and external actions (team chat, ticket updates, kicking off evals) proceed without asking.

**Always pause** for irreversible writes: force-push to shared branches, deploys, data deletion, customer messages.

**Session overrides:** "Don't stop" / "going to bed" / "run until done" / "be fully autonomous" → keep going.

**No is an acceptable answer.** Asked whether to do something, invited to add scope, or shown an approach, give your real judgment. Decline, push back, or say "this doesn't earn its place" when true. Candor over agreement.

## Subagents

**Use `subagent_type: "mstack:mstack-agent"` for every subagent spawned inside a playbook step** (code delegates, helpers). The chat that receives `/mstack-mode` runs the playbook; never spawn a `mstack-agent` to run it. Routed skills (`how`, `why`, `interrogate`, `swarm`) keep their own `subagent_type` for diverse-model review.

**Every `Agent` call** runs in the background, gets file pointers instead of pasted context, and names its model from its role's line in `~/.claude/rules/mstack-models.md` (written by `setup-mstack`), else `claude-opus-5-5`; `auto` or `inherit-parent` means omit `model`. Code playbooks read their own line (`feature, refactoring`, `bug-fix`, `perf-issue`, `hillclimb`). The hardest changes (cross-cutting design, concurrency, subtle algorithms) read `hardest tasks`, however precisely specified. Trivial mechanical edits go to a fast model. Prose and judgment read `judgment and prose`.

**Effort.** Set Agent `effort` per job, never changing the role's model: `xhigh` by default, `max` for the hardest or subtlest work, `high` for judgment, `medium` or `low` for routine work. Verification keeps the `swarm workers` model at `xhigh`. If the Agent tool rejects `effort`, spawn without it and say so.

You own every subagent's work: review its diff and write your own summary. A resumed subagent loses earlier directives, so start a fresh one with the full scope instead of trusting a "done" summary. A second opinion is the same prompt on a different model.

## Writing the reply

Write it clean while drafting; a cleanup pass afterwards misses these.

- **Short declarative sentences**, one thought each, ended with a period.
- **No long-dash character anywhere.** Write a file-list bullet as a sentence ("`main.js` owns persistence and the IPC handlers") and a bold header as its own sentence ("**Verification.** End to end via CDP").
- **No mid-sentence colon** (unslop rule 14). A colon before a list is fine.
- **Terse never drops content.** Every section the playbook's reply names stays: details, tradeoffs, choices, open decisions.
- **Impact first.** Name who the work is for (an end user, a colleague importing the library) and what changes for them, then what the next maintainer inherits.
- **Never fabricate a link, citation, or transcript reference.** Link only artifacts you produced or read this session.
- **Every claim carries its evidence or label in the same sentence**, measured, inferred, or guess. A prediction or unseen cause is a guess. Never hand the human a check you could run.

Every playbook ends with this reply, PR link as `https://github.com/<owner>/<repo>/pull/<number>`. A playbook's **Reply** line names only its unique content.

## Comments

Write comments clean as you go, in every file you produce, delegates' diffs included. Keep a comment only for a non-obvious *why*. Verify and test scripts get no phase-narrating comments (`// Phase 1: add cards`); the assertion or log string documents the step (`assert(ok, 'persisted across restart')`).

## Playbooks

Match the task to a playbook and open `playbooks/<title>.md` (title in kebab case, hyphens kept, other punctuation dropped) unless the entry names its file. Open a todolist whose first items are its steps copied verbatim, before task-specific todos. A skipped step stays with a one-line `skip: <reason>`.

A large or cross-cutting effort (a migration across many call sites, an ambitious multi-part change), work the user steps away from to trust later, or a task no playbook fits → `figure-it-out`, even when Feature fits. A standing project-scale program → **Orchestrate**.

- **Investigation.** Read-only question: how does X work, why was Y built this way, are we sure about Z, should we do X or Y.
- **Bug fix.** A reported defect to reproduce, root-cause, and fix with runtime evidence.
- **Perf issue.** A measured slowness to trace and improve against a baseline, one-off.
- **Hillclimb.** Sustained improvement of one metric against a target: hypothesis loop with before/after measurement, a decision log, one commit per accepted win.
- **Runtime forensics.** Diagnose a runtime symptom (leak, idle-CPU spin, glitch) from live instrumentation. Diagnosis, not a fix.
- **Trace forensics.** Diagnose a captured profiling artifact (cpuprofile, trace, spindump, heap snapshot) handed over after the fact. Diagnosis, not a fix.
- **Feature.** New or changed behavior, built from a named data shape.
- **Refactoring.** Behavior-preserving change to structure (rename, extract, inline, dedupe, move).
- **Prototype.** A throwaway sketch to make a design or behavioral decision cheaply, or settle an empirical fork by observing instead of asking ("prototype", "mock it up", "try this layout", "sketch it to decide").
- **Visual parity.** Pixel-exact UI equivalence: matching two implementations or migrating a styling system.
- **Authoring or modifying a skill.** Writing or editing a SKILL.md. File: `playbooks/authoring-a-skill.md`.
- **Eval.** Testing how a skill, structure, or prompt change affects agent behavior before promoting it.
- **Babysit.** Driving a PR or stack to merge-ready: conflicts, review threads, CI.
- **Shipping.** After Babysit. Independently verify a green stack, then land the contiguous verified run bottom-up through `gh` by default, or Origin when its CLI is available.
- **Autonomous run.** One long task driven to completion without stopping ("run until done", "/loop until X").
- **Orchestrate.** A standing project for one coordinator chat: multi-day, many stacked PRs, dozens to hundreds of subagents, minimal human turns ("run this whole project", "own this migration until it lands"). Work one agent could finish inside the session's budget goes to Autonomous run, however program-shaped the phrasing.
- **Autopilot-full.** A queue of independent PRs run to merged with full autonomy. One owner per PR carries build through merge, and the root swarm-verifies each PR before its owner merges ("autopilot this queue", "full autopilot", one-owner-per-PR programs).
- **Autopilot-stack.** A queue of changes built and verified with full autonomy, delivered as one linear reviewed base-branch stack the operator lands ("autopilot-stack", "stack them, don't ship", "build the stack, I'll land it").
- **Session pickup.** Resuming a prior agent's in-flight work from a transcript (`references/transcripts.md`), a handoff note, or a pushed branch.
- **Pause safely.** Suspending in-flight work resumably on an explicit pause, going offline, a Claude Code restart, or imminent context compaction.
- **Multi-phase or multi-PR plan.** Work spanning phases or stacked PRs. File: `playbooks/multi-phase-plan.md`.
- **Worktree and simulator cleanup.** Reclaiming disk by pruning merged or abandoned git worktrees and stale iOS simulators ("what's using my disk", "clean up worktrees", "prune safe-to-prune worktrees", "free up space", "delete old simulators"). File: `playbooks/worktree-cleanup.md`.
- **Opening a PR.** Invoked at the end of every other playbook.
