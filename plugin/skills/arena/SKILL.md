---
name: arena
description: "Use when one attempt could lock in the wrong shape: run N parallel candidates, keep the best, graft in the rest ('arena this'); or for parallel coverage (races, gauntlets, exploration): fan out N workers and merge one report ('swarm this')."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Arena

Two modes: arena (one best artifact) and swarm (coverage). Infer which from the ask and say which. Open a todolist.

Arena todolist: Frame, Fan out, Cross-judge, Pick, Graft, Verify.

## Arena

Phase A: Frame
- Same prompt for all; it’s the contract. State the artifact each candidate produces. Private rubric: 3–6 criteria.
- Runners: from ~/.claude/rules/mstack-models.md; else two on claude-opus-5-5. auto or inherit-parent means omit model. If the Agent tool rejects a model, run that seat on its family alias (opus, fable, sonnet, haiku) and say so. Add runners for more design directions. Spawn with effort: xhigh.
- Output per candidate: a git worktree, else /tmp/arena-<slug>/candidate-<n>/.

Phase B: Fan out
- Spawn all N in one message, in the background. Brief each with task, grounding paths, its output path. Instruct: return the artifact plus a short rationale naming alternatives rejected. If a candidate produces nothing, continue with N-1 and note it.

Phase C: Cross-judge
- Spawn one read-only judge from the arena cross-judge pool line (else claude-opus-5-5), from a different family than yours when the pool allows, at effort: high. It scores by path against the rubric and recommends a base. Read candidates while it runs.

Phase D: Pick
- Read every candidate, score each criterion. Compare with the judge; on disagreement, read both rationales before deciding. Pick the base a future maintainer can extend most easily; on a tie, choose the smaller API.

Phase E: Graft
- Walk each loser once for 1–2 portables. Port by hand to keep one mental model. If candidates converge, ship the consensus. If they diverge wildly, reframe and rerun; don’t average.

Phase F: Verify
- Verify per Prove it works (principles). A miss means Phase A was wrong (reframe, rerun) or you missed a graft (return to Phase E).

Output
- Return the artifact plus a short note: base and why, judge’s verdict, each graft and its source, what was rejected and why, convergence or dropouts, and the verification result.

## Swarm

For coverage.

Swarm todolist: Frame, Fan out, Aggregate, Report.

Swarm A: Frame
- State the done predicate and the artifact or report to return.
- Shape: partition slices, race N workers, or mix. For race/mix, declare first pass, rank all, or best-of before spawning.
- Worker model: from ~/.claude/rules/mstack-models.md, else claude-opus-5-5; auto or inherit-parent means omit model. If the Agent tool rejects a model, use claude-opus-5-5 and say so. Spawn with effort: xhigh.
- Each writing worker gets its own writable output. Briefs that verify or measure commits name exact SHAs; measurement briefs also name the method (sample count, what one sample is, order). Workers record both.

Swarm B: Fan out
- Spawn all N in one message with subagent_type: general-purpose, isolation: "worktree" for writers (omit for read-only), and the step 3 model. If starting from a non-default pushed branch, name it in the brief and have the worker check it out in its worktree first.
- Every brief stands alone: goal, scope, exact slice or race arm, how to verify, what to report. Reports use PASS, ISSUES or BLOCKED with evidence. ISSUES lists every provable issue. If a worker drops out, continue with N-1 and note it.

Swarm C: Aggregate
- Drop a result missing the SHAs and method its brief names and rerun that worker once; a second miss is a gap, never a pass. Coverage needs a result for every required slice. Races apply the declared rule. Never paste raw worker dumps.

Swarm D: Report
- One consolidated in-chat report: the table, issue one-liners, gaps or dropouts, and the race rule when used.
