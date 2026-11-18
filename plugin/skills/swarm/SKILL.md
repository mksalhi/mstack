---
name: swarm
description: "Use for parallel coverage (races, gauntlets, exploration): fan out N workers and merge one report. Triggers: 'swarm this'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Swarm

Open a todolist: Frame, Fan out, Aggregate, Report.

## Phase A: Frame

1. State the done predicate and the artifact or report to return.
2. Shape: partition into slices, race N workers on identical briefs, or mix. For a race or mix, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Worker model: the `swarm workers` line in `~/.claude/rules/mstack-models.md`, else `claude-opus-5-5`; `auto` or `inherit-parent` means omit `model`. If the Agent tool rejects a model, use `claude-opus-5-5` and say so. A model race names each arm's model up front. Spawn workers with `effort: xhigh`.
4. Each writing worker gets its own writable output. Briefs that verify or measure commits name the exact SHAs; measurement briefs also name the method (sample count, what one sample is, order). Workers record both.

## Phase B: Fan out

Spawn all N in one message with `subagent_type: general-purpose`, `isolation: "worktree"` for writers (omit for read-only), and the step 3 model. A worker starting from a non-default pushed branch gets it named in the brief and checks it out in its worktree first.

Every brief stands alone: goal, scope, exact slice or race arm, how to verify, what to report. Reports use `PASS`, `ISSUES` or `BLOCKED` with evidence; `ISSUES` lists every provable issue, not only the first. If a worker drops out, continue with N-1 and note it.

## Phase C: Aggregate

Drop a result missing the SHAs and method its brief names and rerun that worker once; a second miss is a gap, never a pass. Coverage needs a result for every required slice. Races apply the declared rule. Never paste raw worker dumps.

## Phase D: Report

One consolidated in-chat report: the table, issue one-liners, gaps or dropouts, and the race rule when used.
