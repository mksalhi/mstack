---
name: writing
description: "Use for any prose: docs, RFCs, READMEs, PR or commit text, agent docs (skills, AGENTS.md, CLAUDE.md); cutting AI tells ('unslop', 'sounds like AI'); sharpening a prompt ('sharpen'); or plain words ('bro', 'in English', 'ELI5')."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Writing

Write so a tired engineer understands on the first read. Apply every section, then the Unslop pass.

- Whole document: give it one Diátaxis mode (tutorial, how-to, reference, explanation) and never mix modes. Open [diataxis.md](diataxis.md) when choosing the mode.
- Agent docs: apply Agent docs below.
- Plain words: restate your last message in plain spoken English. State the concrete mechanism. Use sentence case, short sentences and few commas. No framing labels, mirror sentences or tidy closers.
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
- Open <mstack>/skills/ui/references/copy.md when writing product UI strings.
- Indent code snippets with tabs. Write real paths. Every count or tree claim must be true at the landing commit, with the command that regenerates it.

## Unslop pass

Scan the draft, then rewrite it. Keep the meaning and tone.
- Cut filler -ing phrases, vague attributions, chatbot lines, flattery, generic conclusions, and adverbs without a number. Collapse hedges to "may".
- Say "is" or "has", not "serves as" or "boasts". Say "to", not "in order to". Use no AI vocabulary (additionally, crucial, delve, enhance, pivotal, showcase, underscore) and no abstract metaphor nouns (substrate, vector, surface, north star).
- No "not just X, but Y". No "from X to Y" without a real scale. Use a colon only before a list or example. Use straight quotes.
- Use active voice and whole sentences. Spell out arrows and abbreviations.
- Open [unslop.md](unslop.md) when you need the full word lists.

## Agent docs

- Inline what every branch needs. Put what only some branches need in a file that `SKILL.md` links directly, as "Open `x.md` when <situation>". No chains of links.
- Keep `SKILL.md` under about 5,000 tokens. Keep one authoritative place per meaning.
- End every step on a checkable completion criterion.
- Open [agents.md](agents.md) when deciding what loads when, wording a description or trigger, or choosing invocation settings.

## Sharpen a prompt

Ask for a deeper version of the task, not a bigger one.

1. Say what a top professional would do that the prompt does not ask for.
2. Name the rawest material they would start from.
3. Name the specific methods and tools they would use.
4. Say what, other than you or the user, would show the result is right.

Then rewrite the prompt to ask for exactly that. Leave the user’s choices open.
