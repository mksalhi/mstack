---
name: arena
description: "Use when one attempt could lock in the wrong shape: run N parallel candidates, keep the best, graft in the rest. Triggers: 'arena this'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Arena

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
