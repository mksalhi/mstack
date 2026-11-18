---
name: arena
description: "Use when one attempt could lock in the wrong shape: run N parallel candidates, keep the best, graft in the rest. Triggers: 'arena this'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Arena

Open a todolist with one entry per phase (Frame, Fan out, Cross-judge, Pick, Graft, Verify) before launching anything.

## Phase A: Frame

Every candidate gets the same prompt; the prompt is the contract.

1. State the artifact each candidate produces.
2. Derive a rubric of 3-6 concrete gradeable criteria for *this* task. It is for the picker (Phase D); candidates see only the task.
3. Runners: the `arena runners` line in `~/.claude/rules/mstack-models.md`; if the rule or line is missing, two runners on `claude-opus-5-5`. An `auto` or `inherit-parent` entry (here or in the cross-judge line) means omit `model`. If the Agent tool rejects an entry, run that seat on its family's default (`opus`, `fable`, `sonnet`, `haiku`; no match: `claude-opus-5-5`) and say so; if it rejects a default, use the closest valid same-family slug from the error. Add runners for multiple design directions; reuse one model N times when the work is generation-bound, not judgment-sensitive. Set each spawn's `effort` per the **Effort** rule in `mstack-mode`'s Subagents section.
4. Each candidate gets its own output location (a git worktree, else `/tmp/arena-<slug>/candidate-<n>/`), per Separate before serializing shared state (`principles`).

## Phase B: Fan out

Spawn all N subagents in one message (they run in the background), each with the task, the shared grounding path, its own output path, and instructions to produce the artifact plus a short rationale naming alternatives considered and rejected. A candidate with no output: proceed with N-1 and note the dropout.

## Phase C: Cross-judge

Only after all candidates finish: pick one model from the `arena cross-judge pool` line (missing: `claude-opus-5-5`), preferring a family different from the parent's. Spawn one readonly judge that sees the rubric and candidates by path label, scores each criterion, and recommends a base with rationale. It runs in parallel with your Phase D reading.

## Phase D: Pick a base

Read every candidate end to end. Score each criterion by criterion, not on feel, and compare with the judge. Agreement confirms; disagreement means bias or an ambiguous rubric, so read both rationales before deciding. Pick the base a future maintainer can extend most easily without breaking invariants; on a tie, the cleaner boundary or smaller API (`scoper`).

## Phase E: Graft

Walk each loser once more for what's worth porting, usually one or two things each. Fold grafts in by hand (Converge on the target, `principles`) so the result keeps one mental model; never paste mechanically. If candidates converge on one shape, note it and ship the consensus, no graft. If they wildly diverge, Phase A was under-specified: reframe and re-run, don't average.

## Phase F: Verify

Verify per Prove it works (`principles`). A problem the arena missed means Phase A was wrong (reframe, re-run) or you missed a graft a candidate had (back to Phase E). Don't paper over it.

## Outputs

One synthesized artifact plus a short note: base and why, the judge's verdict, each graft with its source candidate, what was rejected and why, convergence or dropouts, and the verification result.
