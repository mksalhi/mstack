---
name: why
description: "Use for 'why does X work this way', design rationale, regressions or postmortems: cited evidence from git, issues, docs and chat."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

Keep facts separate from inferences.

- Agent type: Every spawn subagent_type: "general-purpose". Never use Explore or Plan.
- Model: Use role’s line in ~/.claude/rules/mstack-models.md; else claude-opus-5-5. auto/inherit-parent => omit model. If a tool rejects it, use its default and say so.

1) Anchor
- If target is vague, infer from context (open files, recent edits), state your reading, proceed.
- Seed context: files/line ranges/key symbols; commits: git blame -L a,b <file>, git log --follow -p -- <file>, git log --oneline -20 -- <file>; PRs: (#1234) from merge subjects via gh pr view <n> --json title,body,comments,reviews,closingIssuesReferences; linked ticket IDs.

2) Investigate in parallel
- Map all MCP servers (incl. deferred) to categories; spawn one investigator per category, in one message, on the why investigators model. Always include source control.
- Build each spawn prompt by filling [references/investigator-prompt.md](references/investigator-prompt.md) and appending that category's playbook, adapted to the user's MCP. Open `references/sources/<category>.md` when writing that investigator's prompt (code-archaeology, linear, notion, slack, datadog, sentry, databricks).
- Every investigator searches only its source, returns evidence not conclusions, quotes verbatim with exact location, logs every query including empty ones, and puts cross-source pointers under Leads.
- Defensive target (null checks, retries, timeouts, rate limits, feature flags, egress guards, OOM handlers)? Also have investigators search incident terms: Linear incident, sev-*, postmortem-action-item labels; Slack #sev-* and #incident-* near the code's addition; git "fix for incident", "add defensive check", revert then re-apply.
- Skip a category only with a written reason (no MCP or provably irrelevant). Empty results are findings.
- Answer inline only for trivial single-commit targets whose PR fully answers, after confirming other searches add nothing.

3) Synthesize and present
- Spawn one synthesizer on the why synthesizer model with findings (nulls/skips), the anchor, the question, filled into [references/synthesizer-prompt.md](references/synthesizer-prompt.md). Every claim carries a cited tier (Direct, Supported, Inferred, Speculative, Unknown), contradictions shown, open questions left open. Present with light edits only; never rewrite its confidence language. If asked before changing code, add Preserve, Change, Avoid, Risk constraints after Sources Consulted.
