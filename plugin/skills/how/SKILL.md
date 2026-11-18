---
name: how
description: "Use for 'how does X work', a walkthrough before changing code, 'where should this live', 'teach me' or 'help me understand X', or researching a question from primary sources into a Markdown file."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# How

Pick the branch:

- **'How does X work', a walkthrough, 'where should this live':** steps 1 to 4 below.
- **'Teach me', 'help me understand X':** follow [teach.md](teach.md).
- **A question outside the repo:** [Research from primary sources](#research-from-primary-sources).

## Explain how X works

The answer is an architectural explanation at the level of a senior engineer onboarding onto a subsystem: a working mental model, not annotated source.

Spawn every subagent with `subagent_type: "general-purpose"`, a brief that forbids edits, and `effort: xhigh`. Model: the `how explorer` or `how explainer` line in `~/.claude/rules/mstack-models.md`, else `claude-opus-5-5`; `auto` or `inherit-parent` means omit `model`. If the Agent tool rejects a model, use `claude-opus-5-5` and say so.

### 1. Assess complexity

If the scope is ambiguous, state your reading and go. When in doubt, treat it as simple.

- **Simple** (one module, small utility, narrow question like "how does function X work"): no explorers. Spawn one explainer from `references/explainer-prompt.md` without the explorer-findings section; it explores and explains. Go to step 4.
- **Complex** (multi-file or multi-service subsystem, cross-cutting feature, full architectural overview): step 2.

### 2. Explore (complex only)

Split the question into 2 to 4 distinct angles. Spawn all explorers in one message, each from `references/explorer-prompt.md` with its angle.

### 3. Synthesize (complex only)

After all explorers return, spawn one explainer from `references/explainer-prompt.md` with every explorer's findings.

### 4. Present

Present the explainer's output in its sections (Overview, Key Concepts, How It Works, Where Things Live, Gotchas), lightly edited, dropping any that don't apply.

## Research from primary sources

Start a background agent to research while you keep working. Its job:

1. Investigate against **primary sources** (official docs, source code, specs, first-party APIs), tracing every claim to the source that owns it.
2. Write findings to one Markdown file, citing each claim's source.
3. Save it where the repo keeps such notes; with no convention, pick somewhere sensible and say where.
