# Swarm

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
