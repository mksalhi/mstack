# Skill mechanics

The skill-specific branch of [agents.md](agents.md): invocation choice and router skills.

## Invocation

- **Model-invoked:** keeps a `description`, so the agent and other skills can fire it; the human can still type its name. The description is an always-loaded context pointer: permanent context load bought for discoverability. An all-reference model-invoked skill can be the one home for reference several skills share. Mechanics: omit `disable-model-invocation`; write a model-facing description carrying the trigger branches (the pointer rules in `agents.md` apply in full).
- **User-invoked:** only the human typing its name can invoke it; no other skill can. Zero context load, but cognitive load: you must remember it exists. Mechanics: set `disable-model-invocation: true`; the `description` becomes a human-facing one-line summary, trigger lists stripped.

Pick model-invocation only when the agent or another skill must reach it on its own; otherwise user-invoked.

Reference two user-invoked skills both need can live in neither (neither can fire the other): put it in a plain file outside the skill system that any skill can point at.

## Splitting by invocation

Split off a model-invoked skill when a distinct leading word you actually use in prompts should trigger it alone, or another skill must reach it. The new always-loaded description costs context load, so the independent reach must be worth it.

## Router skills

When user-invoked skills pile up past memory, add a **router skill**: one user-invoked skill naming the others and when to use each, so the human remembers one. It can only hint, never fire them.

## Description

- Front-load the leading word and the main trigger. Harnesses cut descriptions when the skill listing overflows its budget (Claude Code: 1% of the context window, entries capped at 1,536 characters; Codex: 2% or 8,000 characters), and the cut falls on the end.
- Say when to use it, not how it works: an agent that reads a workflow summary in the description tends to follow the summary instead of loading the skill.
- Name the near-miss when a neighbouring skill shares its words ("For what changed in this chat, use ketchup").

## Size and layout

- Keep `SKILL.md` under 500 lines and about 5,000 tokens: it stays in context for the rest of the session once loaded.
- Everything every branch needs goes inline; what only some branches need goes in a file the body points to with its condition ("Read `references/x.md` before Y"). Name scripts the agent should run, not read.
- Point to files from `SKILL.md` directly, one hop. A chain (`SKILL.md` → a.md → b.md) gets partial reads.
- Put a contents list at the top of a reference file over 300 lines.
- Sources: platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, agentskills.io/specification, code.claude.com/docs/en/skills, learn.chatgpt.com/docs/build-skills, and obra/superpowers `writing-skills` for the workflow-summary finding (2026-11-18).
