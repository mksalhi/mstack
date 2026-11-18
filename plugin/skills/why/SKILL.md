---
name: why
description: "Use for 'why does X work this way', design rationale, regressions or postmortems: cited evidence from git, issues, docs and chat."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Why

Find the forces that gave code its shape; `how` covers what it does. Keep what you know separate from what you infer.

- **Agent type.** Every spawn is `subagent_type: "general-purpose"`. Never use `Explore` or `Plan`, which lack MCP tools, and investigators and the synthesizer need them.
- **Model.** Use the role's line in `~/.claude/rules/mstack-models.md`, falling back to `claude-opus-5-5`. `auto` or `inherit-parent` means omit `model`. If the tool rejects the model, use the default and say so.
- **Effort.** `xhigh`.
- **Investigators write nothing.**

## 1. Anchor

If the target is vague, guess it from context (open files, recent edits), state your reading, and proceed. Then build the seed context that every agent gets:

- **Files, line ranges and key symbols.**
- **Commits:** `git blame -L a,b <file>`, `git log --follow -p -- <file>`, and `git log --oneline -20 -- <file>`.
- **PRs:** the `(#1234)` numbers from merge subjects, each read with `gh pr view <n> --json title,body,comments,reviews,closingIssuesReferences`.
- **Linked ticket IDs.**

Trace back past the latest commit. Today's shape built up over many decisions, so the most recent one isn't the authority.

## 2. Investigate in parallel

Map every available MCP server (deferred ones included) to one category below, then spawn one investigator per category, all in one message, on the `why investigators` model. Each gets [references/investigator-prompt.md](references/investigator-prompt.md) filled in, plus its source playbook, adapted for whichever MCP the user actually has:

| Category | Best at | Playbook |
|---|---|---|
| Source control (git, `gh`, comments, tests): always spawn | Rationale captured in review | [code-archaeology](references/sources/code-archaeology.md) |
| Tickets (Linear, Jira, GitHub Issues) | The product or business reason | [linear](references/sources/linear.md) |
| Docs (Notion, Confluence, Google Docs) | Design rationale written before the code | [notion](references/sources/notion.md) |
| Chat (Slack, Teams, Discord) | Discussion that never reached a doc | [slack](references/sources/slack.md) |
| Observability (Datadog, Grafana, Honeycomb) | Runtime reality behind timeouts and limits | [datadog](references/sources/datadog.md) |
| Errors (Sentry, Rollbar) | The exceptions behind defensive code | [sentry](references/sources/sentry.md) |
| Warehouse (Databricks, Snowflake, BigQuery) | Usage, experiments, where a number came from | [databricks](references/sources/databricks.md) |

**Defensive targets** (null checks, retries, timeouts, rate limits, flags, OOM handlers) also get [incident-postmortem](references/sources/incident-postmortem.md).

**Skip a category only with a written reason:** either no MCP exists for it (a gap) or it's provably irrelevant (for example, a build script with no runtime path, so error tracking can't apply). An empty result is still a finding. Answer inline only for a trivial single-commit target whose PR fully answers the question, and only after confirming the other searches would add nothing.

## 3. Synthesize and present

Spawn one synthesizer on the `why synthesizer` model with the findings (nulls and skips included), the anchor, the question and [references/synthesizer-prompt.md](references/synthesizer-prompt.md). Present its output with light edits only, and **never rewrite its confidence language**. If the question comes before changing the code, add Preserve, Change, Avoid and Risk constraints after Sources Consulted.
