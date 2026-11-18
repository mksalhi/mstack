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

Every spawn is an Agent with `subagent_type: "general-purpose"` and a brief that forbids edits. Model: explorers use the `how explorer` line in `~/.claude/rules/mstack-models.md`, explainers the `how explainer` line (both default `claude-opus-5-5`); use the default if the rule or line is missing; leave `model` unset for `auto` or `inherit-parent`. Agent rejects a slug: use the default and say so; rejects the default: use the closest valid same-family slug from its error. Set `effort` per the **Effort** rule in `mstack-mode`'s Subagents section.

### 1. Assess complexity

Ambiguous scope: state your interpretation and explore. When in doubt, simple.

- **Simple** (one module, small utility, narrow question like "how does function X work"): no explorers. Spawn one explainer from `references/explainer-prompt.md` without the explorer-findings section; it explores and explains. Go to step 4.
- **Complex** (multi-file or multi-service subsystem, cross-cutting feature, full architectural overview): step 2.

### 2. Explore (complex only)

Split the question into 2 to 4 distinct angles. Spawn all explorers in one message, each from `references/explorer-prompt.md` with its angle.

### 3. Synthesize (complex only)

After all explorers return, spawn one explainer from `references/explainer-prompt.md` with every explorer's findings.

### 4. Present

Present the explainer's output with only light edits for clarity or conversation context, in its sections (Overview, Key Concepts, How It Works, Where Things Live, Gotchas), dropping any that don't apply.

## Research from primary sources

Spin up a **background agent** to research while you keep working. Its job:

1. Investigate against **primary sources** (official docs, source code, specs, first-party APIs), tracing every claim to the source that owns it.
2. Write findings to one Markdown file, citing each claim's source.
3. Save it where the repo keeps such notes; with no convention, pick somewhere sensible and say where.
