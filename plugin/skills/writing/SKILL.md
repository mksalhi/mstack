---
name: writing
description: "Use for any prose: docs, RFCs, READMEs, PR or commit text, agent docs (skills, AGENTS.md, CLAUDE.md); cutting AI tells ('unslop', 'sounds like AI'); sharpening a prompt ('sharpen'); or plain words ('bro', 'in English', 'ELI5')."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Writing

Write so a tired engineer understands on the first read. Find the request below, then apply every section.

- **A doc, PR, commit, or other prose:** all sections, then the unslop pass in [unslop.md](unslop.md). For a whole document (README, guide, RFC, reference page), first pick its mode with [diataxis.md](diataxis.md).
- **Unslop ('unslop', 'sounds like AI'):** scan and rewrite with [unslop.md](unslop.md).
- **Agent docs** (a skill, `AGENTS.md`, `CLAUDE.md`, or a doc reached by a pointer): also read [agents.md](agents.md).
- **Plain words ('bro', 'in English', 'ELI5'):** restate your last message in the voice set by the **Voice** paragraph of `<mstack>/skills/how/teach.md`.
- **Sharpen a prompt:** see [Sharpen a prompt](#sharpen-a-prompt).

## Rules

Most plain-English advice you already follow. These are the ones that slip:

- Write the real symbol, file, flag or command name, not a synonym. Use words a developer says out loud ("move", "delete", "a budget that only decreases", not "evacuate", "ratchet" or "endgame"). Define a named pattern on first use. To add a word to rule 26 in `unslop.md`, propose it in your reply; don't edit that file.
- One name per thing everywhere; "the gate", "the ratchet" and "the budget check" for one thing teaches three. Don't churn names that didn't change.
- Specific over sterile: not "schema changes can cause issues" but "a column rename fails the build". Have a view where the mode allows; reference stays dry.
- "You", present tense, name the actor. Instructions are commands; condition before instruction ("To delete it, click **Delete**."); common case first. One instruction per sentence; split instructions over about 20 words, other sentences over about 25.
- Keep "the" and "a", and keep "only" and "not" next to the word they change. Break noun strings ("the proto import budget check script" becomes "the script that checks the proto-import budget"). Every "it", "this" points at one thing; never "this" or "which" for a whole clause.
- Periods, not semicolons; no em dashes; no slashes ("a, b, or both"); no "(s)" plurals, idioms or Latin abbreviations. Drop "etc." and say up front that a list is partial.
- Headings carry the point ("Pick the mode first", not "Modes"), sentence case. Link text names the target, never "click here".
- When a rule makes a sentence worse, fix it another way or leave it. A sentence that obeys every rule and sounds machine-written has failed.

## Repo specifics

- PR descriptions and commit messages skip the Diátaxis mode choice. A PR body is a briefing readable in under a minute; link swarm logs, SHA lists, and metric tables, don't paste them.
- Product UI strings: the `ui` skill's copy area, `<mstack>/skills/ui/references/copy.md`.
- Indent code snippets with tabs. Write real paths. Every count or tree claim must be true at the landing commit, with the command that regenerates it.

Before:

> Configuration of the proto import ratchet budget script parameters is performed via budget.json. Note that it's important to remember that running with --write, which updates the committed budget to reflect the current count, should only be done when lowering it. If exceeded, CI fails.

After:

> `budget.mjs` reads the committed budget from `budget.json` and counts the files that import protos. If the count exceeds the budget, CI fails. Run `budget.mjs --write` only to lower the budget.

## Sharpen a prompt

Ask for a deeper version of the task, not a bigger one. Before rewriting it:

1. Say what a top professional in this field would do here that the prompt doesn't ask for.
2. Name the rawest material they would start from instead of what has already been digested.
3. Name the specific methods and tools they would use.
4. Say what, other than you or the user, would show the result is right.

Then rewrite the prompt to ask for exactly that. Leave the user's choices open.
