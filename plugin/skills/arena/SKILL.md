---
name: arena
description: "Use when one attempt could lock in the wrong shape: run N parallel candidates, keep the best, graft in the rest ('arena this'); or for parallel coverage (races, gauntlets, exploration): fan out N workers and merge one report ('swarm this')."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Arena

Two modes: **arena** (one best artifact, below) and **swarm** (coverage, at the end). Infer which from the ask and say which.

Open a todolist: Frame, Fan out, Cross-judge, Pick, Graft, Verify.

## Phase A: Frame

Every candidate gets the same prompt; the prompt is the contract.

1. State the artifact each candidate produces.
2. Write a rubric of 3-6 gradeable criteria for this task. Only the picker and judge see it.
3. Runners: the `arena runners` line in `~/.claude/rules/mstack-models.md`, else two on `claude-opus-5-5`. `auto` or `inherit-parent` means omit `model`. If the Agent tool rejects a model, run that seat on its family alias (`opus`, `fable`, `sonnet`, `haiku`) and say so. Add runners for more design directions. Spawn runners with `effort: xhigh`.
4. Give each candidate its own output location: a git worktree, else `/tmp/arena-<slug>/candidate-<n>/`.

## Phase B: Fan out

Spawn all N in one message, in the background, each with the task, the grounding paths, its output path, and an instruction to return the artifact plus a short rationale naming the alternatives it rejected. If a candidate produces nothing, continue with N-1 and note it.

## Phase C: Cross-judge

After all candidates finish, spawn one read-only judge on a model from the `arena cross-judge pool` line (else `claude-opus-5-5`), from a different family than yours when the pool allows, at `effort: high`. It scores each candidate by path against the rubric and recommends a base. Read the candidates while it runs.

## Phase D: Pick a base

Read every candidate end to end and score each criterion separately. Compare with the judge: disagreement means bias or an ambiguous rubric, so read both rationales before deciding. Pick the base a future maintainer can extend most easily; on a tie, the smaller API (`scoper`).

## Phase E: Graft

Walk each loser once for what is worth porting, usually one or two things. Port by hand so the result keeps one mental model. If the candidates converge, ship the consensus. If they diverge wildly, Phase A was under-specified: reframe and rerun, don't average.

## Phase F: Verify

Verify the result per Prove it works (`principles`). A problem the arena missed means Phase A was wrong (reframe, rerun) or you missed a graft (back to Phase E).

## Output

The artifact plus a short note: the base and why, the judge's verdict, each graft and its source, what was rejected and why, convergence or dropouts, and the verification result.

## Swarm mode

For coverage rather than one artifact (races, gauntlets, exploration): fan out N workers and merge one report. Open a todolist: Frame, Fan out, Aggregate, Report.

### Swarm A: Frame

1. State the done predicate and the artifact or report to return.
2. Shape: partition into slices, race N workers on identical briefs, or mix. For a race or mix, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Worker model: the `swarm workers` line in `~/.claude/rules/mstack-models.md`, else `claude-opus-5-5`; `auto` or `inherit-parent` means omit `model`. If the Agent tool rejects a model, use `claude-opus-5-5` and say so. A model race names each arm's model up front. Spawn workers with `effort: xhigh`.
4. Each writing worker gets its own writable output. Briefs that verify or measure commits name the exact SHAs; measurement briefs also name the method (sample count, what one sample is, order). Workers record both.

### Swarm B: Fan out

Spawn all N in one message with `subagent_type: general-purpose`, `isolation: "worktree"` for writers (omit for read-only), and the step 3 model. A worker starting from a non-default pushed branch gets it named in the brief and checks it out in its worktree first.

Every brief stands alone: goal, scope, exact slice or race arm, how to verify, what to report. Reports use `PASS`, `ISSUES` or `BLOCKED` with evidence; `ISSUES` lists every provable issue, not only the first. If a worker drops out, continue with N-1 and note it.

### Swarm C: Aggregate

Drop a result missing the SHAs and method its brief names and rerun that worker once; a second miss is a gap, never a pass. Coverage needs a result for every required slice. Races apply the declared rule. Never paste raw worker dumps.

### Swarm D: Report

One consolidated in-chat report: the table, issue one-liners, gaps or dropouts, and the race rule when used.
