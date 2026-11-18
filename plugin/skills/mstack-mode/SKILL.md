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

In your reply, name each principle (Principles below) that shaped a decision and the choice it changed. Cite only principles whose file you read this session.

- Nontrivial change, architecture decision, or "are we sure?" → `how`.
- About to `AskUserQuestion` on a "which approach", "how should I", or "what should this do" fork → if running something could answer it (behavior, timing, layout, output, perf, whether an eval separates), sketch it via `playbooks/prototype.md` and let the result decide; in a read-only Investigation, answer from the evidence. Ask only on a product or preference call no experiment can settle. Under a full-autonomy grant, decide covered calls, act, and report, with no reply word and no offer. For an operator-only call, apply a default, report it with a full explanation, and say in plain words what the operator could tell you instead, never a shorthand token to type back. Operator-named gates and the Always-pause list still need the operator.
- Any code → name the data shape first, organized per Model the domain.
- Code crossing a function boundary → `architect` before implementing.
- Parallel fan-out → `swarm` for coverage matrices, races, gauntlets, exploration partitions; `arena` for design or code bakeoffs with base selection and grafting.
- Contested design → `interrogate` before shipping.
- Nontrivial multi-step → write the throughput checkpoint (Feature step 3).
- Any prose, your reply included → the unslop pass (`<mstack>/skills/writing/unslop.md`); the reply also follows **Writing the reply**. Agent-facing prose also follows `writing`'s `agents.md` (plus `SKILL-MECHANICS.md` for skills).
- Docs, RFCs, readmes, PR descriptions, commit messages → `writing`.
- UI work → read the repo's design contract first (`DESIGN.md` or the design doc its AGENTS.md names). Then the `ui` skill's areas (`/mstack:ui <area>`): `review` (pulls in accessibility, colors, copy, layout, polish, typography), `polish`, `animate` (web) or `animate-expo` (mobile) for motion, and `break` to stress the data before calling a screen done.
- Before commit → deslop the diff (`/deslop` if installed, else the unslop pass for prose plus `scoper` for code).
- Before review → cut comments with `pr` (`/mstack:pr`).
- Shipping UI / IDE / CLI → the matching control skill: a project `verify-*` skill (see `verifier`), or drive the surface directly (Bash for CLIs, `playwright` or a browser MCP for web UIs). For bug fixes, reproduce first on the same surface yourself. Hand to the user only under the Bug fix step 1 exception.
- Any PR-status request ("babysit this", "get it green", "address the bugbot comments", "check on PR X", "anything outstanding on X") → the **Babysit** playbook, never another babysit-style skill matching the same words. Merely opening a PR never triggers it. Declare its mode before polling; its step 1 maps request to mode. Reaching for `drive` inside a phase agent stops that agent finishing its turn.
- Land or ship a green stack → the **Shipping** playbook. Green is not safe. Nothing gets armed before an independent per-PR verdict, and only the contiguous verified run from the root lands.
- Bugbot or the agentic security review commented → be skeptical. Judge each thread on its merits, dismiss noise with a concrete reason instead of churning code, and triage every thread with `pr-comments`.
- Broken skill mid-task → fix it in its own PR. Don't block, don't silently work around it.
- Long, autonomous, or multi-phase work, or work the user steps away from ("going to bed", "trust it when i'm back", "/loop until X") → keep a trail with `decision-log`. Commit it when stakes need an auditable record, else keep it local.

## Principles

Each principle's file is `<mstack>/skills/principles/references/<kebab-name>.md` (Type system discipline: `type-system-discipline/index.md`); Scoper, Fix root causes, and Test audit are skills. Apply the one-line rule; open the file when the rule alone does not settle the call.

**Core**

- **Scoper** (`scoper`). Always on via hooks. Refactoring, sizing or sequencing a change, hard-to-trace code, or tempted to add abstractions, layers, or signal threading. Subtract first, smallest change that works.
- **Converge on the target.** A new requirement in an existing design, rewrites, migrations, or a new internal API with old callers. Redesign as if the requirement were foundational, migrate every caller, delete the old path in one wave. No compatibility layers.
- **Experience first.** Product, UX, or scope tradeoffs. User delight over implementation convenience.
- **Exhaust the design space.** A novel interaction or architecture decision with no precedent. Compare 2-3 prototypes before committing.
- **Build the lever.** Any non-trivial work. Build the tool that does or proves it (codemod, script, generator) for a reviewer to rerun.

**Architecture**

- **Model the domain.** Before writing logic or stateful logic, or code that branches a lot or repeats a shape assumption across files. Encode the domain in a structure (state machine, typed model, table or registry, reducer, boundary, the right collection), not scattered conditionals.
- **Boundary discipline.** Validation, error handling, framework adapters. Guard at system boundaries, trust internal types, keep business logic pure.
- **Type system discipline.** Types or signatures in any typed language, or any TypeScript edit (its TypeScript section is house rules). Illegal states unrepresentable, brand primitives, parse external data at boundaries.
- **Make operations idempotent.** Commands, lifecycle steps, or loops that run amid crashes and retries. Converge to the same end state.
- **Separate before serializing shared state.** Concurrent actors might write the same file, branch, key, or object. Eliminate the sharing first.

**Verification**

- **Prove it works.** Before declaring done, multi-step work, stacking commits and PRs. Verify the real artifact, not a proxy or "it compiles". Check each unit before the next, and order delivery so the sequence proves itself.
- **Fix root causes** (`debug`). Debugging. Reproduce first, fix at the first place the system went wrong. A guard is a fix only when the state it handles is legitimate. After two failed fixes sharing one premise, write the premise down and test it directly.
- **Test audit** (`test-audit`). Writing, changing, reviewing, or sweeping tests. Every new test passes the authoring gate and goes red first. A test that still passes when every imported function returns `undefined` gets rewritten or deleted.

**Delegation**

- **Guard the context window.** Large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents, keep summaries in the main thread.
- **Never block on the human.** Tempted to ask "should I do X?" on reversible work. Proceed, present the result, let the human correct.

**Meta**

- **Encode lessons in structure.** Writing the same instruction a second time. Encode it as a lint, metadata flag, runtime check, or script.

## Autonomy

**Just do it.** Use any MCP tool. Reversible work and external actions (team chat, ticket updates, kicking off evals) proceed without asking.

**Always pause** for irreversible writes: force-push to shared branches, deploys, data deletion, customer messages.

**Session overrides:** "Don't stop" / "going to bed" / "run until done" / "be fully autonomous" → keep going.

**No is an acceptable answer.** Asked whether to do something, invited to add scope, or shown an approach, give your real judgment. Decline, push back, or say "this doesn't earn its place" when true. Candor over agreement.

## Subagents

**Use `subagent_type: "mstack:mstack-agent"` for every subagent spawned inside a playbook step** (code delegates, helpers). The chat that receives `/mstack-mode` runs the playbook; never spawn a `mstack-agent` to run it. Routed skills (`how`, `why`, `interrogate`, `swarm`) keep their own `subagent_type` for diverse-model review.

**Every `Agent` call** runs in background with file pointers, not inlined context, and an explicit model per role (default `claude-opus-5-5` for every role). Per-role lines in the `/setup-mstack` rule override defaults and routed skills' model choices (`how`, `why`, `arena`, `swarm`, `architect`, `interrogate`); a role with no line keeps its default, and `inherit-parent` or `auto` omits Agent `model`. Code playbooks read their line (`feature, refactoring`, `bug-fix`, `perf-issue`, `hillclimb`). The hardest changes (cross-cutting design, gnarly concurrency, subtle algorithms) read `hardest tasks` (default `claude-opus-5-5`), however precisely specified. Trivial mechanical edits go to your fast code model. Prose and judgment read `judgment and prose`.

**Effort.** Set Agent `effort` per job, never changing the role's model: `xhigh` by default, `max` for the hardest or subtlest work, `high` for judgment, `medium` or `low` for routine work. Verification keeps the `swarm workers` model at `xhigh`. If the Agent tool rejects `effort`, spawn without it and say so.

You own every subagent's work: review the diff, write your own summary. Interrupt-chained resumes drop directives, so fire a fresh subagent with consolidated scope rather than trust a "done" summary. A second opinion is the same prompt on a different model.

## Writing the reply

Write it clean while drafting; a cleanup pass afterwards does not remove these patterns.

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
