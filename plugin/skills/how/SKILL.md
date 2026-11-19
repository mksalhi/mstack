---
name: how
description: "Use for 'how does X work', a walkthrough before changing code, 'where should this live', 'teach me' or 'help me understand X', or researching a question from primary sources into a Markdown file."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# How

Branches: “How does X work”/walkthrough/“where should this live”: steps 1–4. “Teach me”: see Teach me below. Outside the repo: see Research from primary sources.

Spawn every subagent with subagent_type: "general-purpose", a brief that forbids edits, and effort: xhigh. Model: the how explorer/how explainer line in ~/.claude/rules/mstack-models.md; else claude-opus-5-5; auto or inherit-parent => omit model; if the Agent tool rejects a model, use claude-opus-5-5 and say so.

1) Assess complexity
- Simple: spawn one explainer without the explorer-findings section. Open [references/explainer-prompt.md](references/explainer-prompt.md) when writing any explainer brief and fill its placeholders.

2) Explore
- Split into 2–4 angles. Spawn explorers in one message. Open [references/explorer-prompt.md](references/explorer-prompt.md) when writing their briefs and give each its angle.

3) Synthesize
- Spawn one explainer from the explainer prompt with every explorer’s findings.

4) Present
- Sections: Overview, Key Concepts, How It Works, Where Things Live, Gotchas; drop any that don’t apply.

## Teach me
- Run steps 1–4 and the why skill in parallel, then combine. Keep why narrow unless reasons are the point.
- Explain only, change nothing. Give the smallest complete answer, then offer to go deeper. Never a wall of text, quizzes or say-it-back requests.
- Open [teach.md](teach.md) before replying, for takeaways, figures, voice and reply order.

## Research from primary sources
- Start a background agent; use primary sources; write one Markdown file citing each claim; save where notes live (else pick somewhere sensible and say where).
