---
name: why
description: "Use for 'why does X work this way', design rationale, regressions or postmortems: cited evidence from git, issues, docs and chat."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Why

Find the forces that gave code its shape (`how` covers what it does). Separate what you know from what you infer; the confidence framework is in `references/epistemics.md`, and the synthesizer must follow it.

Every spawn is `subagent_type: "general-purpose"`. **Never swap in a narrower type like `Explore` or `Plan`**: a missing tool, MCP above all, disables MCP-backed investigators and the synthesizer's citation spot-checks. Investigators write nothing.

Model per spawn: its role line in `~/.claude/rules/mstack-models.md`, else `claude-opus-5-5`; `auto` or `inherit-parent` means omit `model`. If the Agent tool rejects a model, use `claude-opus-5-5` and say so. Spawn with `effort: xhigh`.

## 1. Understand the target and the question

- **Target:** usually code, a pattern, a feature, or a named design decision. **Question:** usually design rationale, a tradeoff, a motivating edge case, an external constraint, dead code, or a broad history sweep.
- Vague target: guess from context (open files, recent edits, the discussion), state your reading, and proceed.

## 2. Establish the code anchor

Build the seed context inline before spawning; it goes to every investigator and the synthesizer: file paths and line ranges, key symbols, recent commits touching the target, PR numbers (`(#1234)` in merge subjects), linked ticket IDs.

- `git blame -L <start>,<end> <file>`: last-touch commits.
- `git log --follow -p -- <file>`: full history with patches through renames.
- `git log --oneline -20 -- <file>`: recent commits with PR numbers.
- `git log -1 --format=%B <commit>`: extract PR numbers.
- For each substantive commit: `gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews`.

Trace back past the latest commit: the current shape accretes many earlier decisions, so recency is not authority.

## 3. Spawn parallel investigators

Default to the full parallel investigation. An empty result is a finding; never skip the search.

List available MCP servers (the `mcp__<server>__<tool>` names in your tool list, deferred included, or `claude mcp list`). Map each to one roster category below by name, server instructions, tool names, and resource descriptors; a multi-fit MCP goes to its primary evidence, recorded as ambiguous in the coverage map.

Spawn one investigator per category with a matching MCP, all in one message, each owning exactly one tool or MCP, on the `why investigators` model. Each prompt is `references/investigator-prompt.md` filled in, plus:
- the category playbook `references/sources/<source>.md` for the selected MCP, adapted from the examples in `references/source-playbook.md`
- `references/sources/incident-postmortem.md` **if the target looks defensive** (null checks, retries, timeouts, rate limiting, feature flags, egress guards, OOM handlers)
- the code anchor and the user's original question

Roster, one investigator per available category. "Best at" sets expectations, names the gap when a category returns empty, and justifies a skip only when provably irrelevant.

1. **Source control** (git, `gh` PRs, code comments, tests). Always available; always spawn. Best at *implementation-time rationale captured in review*.
2. **Issue / ticket tracker** (Linear, Jira, GitHub Issues, Plane, Shortcut). Best at *the product or business forcing function*.
3. **Long-form documents** (Notion, Confluence, Google Docs, Coda). Best at *design rationale written before the code*.
4. **Real-time team chat** (Slack, Discord, Teams, Mattermost). Best at *deliberation that never reached a doc*; key when the paper trail is thin.
5. **Infrastructure observability** (Datadog, New Relic, Honeycomb, Grafana, Splunk). Best at *runtime reality*: timeouts, retries, rate limits, circuit breakers.
6. **Error / exception tracking** (Sentry, Rollbar, Bugsnag, Airbrake). Best at *exceptions behind defensive code*: catch blocks, null guards, type checks, retries.
7. **Product analytics warehouse** (Databricks, Snowflake, BigQuery, ClickHouse, dbt, Redshift). Best at *product and data reality*: flag-gated code, experiments, data migrations, "where did this number come from".

Skip an investigator only with an **explicit written justification** in Sources Consulted, for one of two reasons:

- **No MCP for the category**: a gap, not a choice. "Real-time team chat skipped. No matching MCP available, so the conversational record was not searchable."
- **Provably irrelevant**, not "probably": "Error / exception tracking skipped. Target is a build-time script with no runtime code path."

A trivial single-commit target whose PR description holds the complete answer may be answered inline **only after** confirming every available category search would be redundant; say so. Rare.

## 4. Synthesize

Spawn one synthesizer on the `why synthesizer` model with: investigator findings (including nulls and justified skips), the code anchor, the user's question, `references/epistemics.md`, and `references/synthesizer-prompt.md`.

## 5. Present

Present the synthesizer's output with light edits only. **Never rewrite the confidence language.**

Its sections, per `references/synthesizer-prompt.md`: The Question, The Code in Question, What We Found, What We Can Reasonably Infer, Competing Hypotheses, What We Don't Know, Sources Consulted, Confidence Summary. Adapt freely but keep the confidence separation, and Sources Consulted as one line per investigator, including empty or skipped ones with the reason.

If the `why` question precedes changing this code, add after Sources Consulted a Preserve / Change / Avoid / Risk constraint set for planning the change.
