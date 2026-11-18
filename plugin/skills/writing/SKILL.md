---
name: writing
description: "Use for any prose: docs, RFCs, READMEs, PR or commit text, agent docs (skills, AGENTS.md, CLAUDE.md); cutting AI tells ('unslop', 'sounds like AI'); sharpening a prompt ('sharpen'); or plain words ('bro', 'in English', 'ELI5')."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Writing

Write so a tired engineer understands on the first read. Apply every section. Then run an unslop pass in [unslop.md](unslop.md). For a whole document, pick its mode with [diataxis.md](diataxis.md).

- Agent docs: also read [agents.md](agents.md).
- Plain words: restate your last message in the voice set by the Voice paragraph of <mstack>/skills/how/teach.md.
- Sharpen a prompt: see Sharpen a prompt.

## Rules

- Use the real symbol, file, flag, or command name. Use the words a developer says out loud. Define a named pattern on first use. Use one name per thing.
- Be specific. Name the failing action and the effect.
- Address “you”. Use present tense. Give commands. Put the condition before the instruction. Lead with the common case. Write one instruction per sentence.
- Keep “the” and “a”. Keep “only” and “not” next to the word they change.
- Break noun strings. Make every “it” or “this” point at one thing. Do not use “this” or “which” for a whole clause.
- Use periods, not semicolons. No em dashes. No slashes in prose. No “(s)” plurals. No idioms or Latin abbreviations. Drop “etc.”.
- Headings carry the point. Link text names the target, never “click here”.
- If a rule makes a sentence worse, fix it another way or leave it.

## Repo specifics

- PR descriptions and commit messages skip the Diátaxis mode choice. A PR body is a briefing readable in under a minute. Link swarm logs, SHA lists, and metric tables. Do not paste them.
- Product UI strings: the ui skill’s copy area, <mstack>/skills/ui/references/copy.md.
- Indent code snippets with tabs. Write real paths. Every count or tree claim must be true at the landing commit, with the command that regenerates it.

## Sharpen a prompt

Ask for a deeper version of the task, not a bigger one.

1. Say what a top professional would do that the prompt does not ask for.
2. Name the rawest material they would start from.
3. Name the specific methods and tools they would use.
4. Say what, other than you or the user, would show the result is right.

Then rewrite the prompt to ask for exactly that. Leave the user’s choices open.
