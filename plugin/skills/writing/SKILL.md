---
name: writing
description: "Use for any prose: docs, RFCs, READMEs, PR or commit text, agent docs (skills, AGENTS.md, CLAUDE.md); cutting AI tells ('unslop', 'sounds like AI'); sharpening a prompt ('sharpen'); or plain words ('bro', 'in English', 'ELI5')."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Writing

Write so a tired engineer understands on the first read. Pick the request, then apply every layer below.

- **A doc, PR, commit, or other prose:** all layers, then the unslop pass in [unslop.md](unslop.md).
- **Unslop ('unslop', 'sounds like AI'):** scan and rewrite with [unslop.md](unslop.md).
- **Agent docs** (a skill, `AGENTS.md`, `CLAUDE.md`, or a doc reached by a pointer): also read [agents.md](agents.md); for a skill, [SKILL-MECHANICS.md](SKILL-MECHANICS.md) too.
- **Plain words ('bro', 'in English', 'ELI5'):** restate your last message in the voice set by the **Voice** paragraph of `<mstack>/skills/how/teach.md`.
- **Sharpen a prompt:** see [Sharpen a prompt](#sharpen-a-prompt).

## Three rules

- **Cut every word that does no work.** "In order to" is "to". "It is important to note that" is nothing.
- **Use the short, everyday word.** "Use", not "utilize"; "help", not "facilitate"; "do", not "perform". A long word must buy its length with precision.
- **When a rule makes a sentence worse, fix it another way or leave it.** A sentence that obeys every rule and sounds machine-written has failed.

The codebase is the word list: write the real symbol, file, flag, or command name, not a synonym.

Don't invent jargon. Use words a developer says out loud: "move", "delete", "a budget that only decreases", not "evacuate", "ratchet", or "endgame". A named pattern is fine if defined on first use. To add an offender to rule 26 (abstract metaphor nouns) in `unslop.md`, propose it with its replacement in your reply, with the diff; don't edit that file.

## Vary the rhythm

- Mix sentence lengths: short ones land a point; longer ones carry a fact with its condition or consequence. Split a sentence carrying two thoughts; keep a long one carrying one.
- Have a view where the mode allows: explanation says what you make of trade-offs instead of listing pros and cons. Reference stays dry.
- Specific over sterile: not "schema changes can cause issues" but "a column rename fails the build".

## Pick the mode first (Diátaxis)

One document, one mode. Action or understanding? Learning or work? Action + learning: **tutorial**. Action + work: **how-to**. Understanding + work: **reference**. Understanding + learning: **explanation**. The compass applies to a whole document or one sentence.

- **Tutorial.** The learner's success is your job. Open with what they will build, not "learn". Every step yields a visible result early and often; say what they should see (output, prompt change, log line). Explanation: one clause and a link. Concrete, "we", commands: "First, do x. Now, do y."
- **How-to.** Solve a person's problem, not a machine operation. Assume competence. Action only: link background, digressions, completeness. Allow forks: "If you want x, do y." Name by task: "How to calibrate the radar array", not "Radar array calibration".
- **Reference.** Only describe: no instruction, persuasion, or opinion. Dry, complete, sure; state facts, options, limits, errors without hedging. Mirror the structure of the thing described; put material where readers expect it. Generate from code where possible.
- **Explanation.** One bounded topic, readable away from the product; titles tolerate an implicit "About...". Anchor on a real why question. Give design decisions, history, constraints, alternatives. Opinion is allowed here only.

Don't mix modes (no reference tables in tutorials, no hand-holding in reference, no arguing in how-tos). Split and link. Source: diataxis.fr, 2026-07-18.

## Write sentences to the reader (Google developer style)

- "You", present tense; "will" only for genuinely later events.
- Name the actor: "the compiler checks", not "is checked". Passive only when the actor is unknown or irrelevant.
- Instructions as commands ("Click Submit."); facts plainly; never "should be done".
- Condition before instruction: "To delete the document, click Delete." Common case first, exceptions after.
- Knowledgeable friend: no buzzwords, figurative language, or "please" in instructions; never "simply", "easy", or "quickly" in a procedure.
- No pre-announcing ("we will soon support..."); don't start consecutive sentences with the same phrase.
- Link text says where it goes (page title or short description), never "click here". Prefer a sentence of context over a link off the page.
- Headings carry the point ("Pick the mode first", not "Modes"), sentence case. Task heading: bare verb phrase ("Create an instance"). Concept heading: noun phrase. One h1, no skipped levels.
- Numbered lists for sequences, bullets otherwise; introduce with a complete sentence; parallel items.
- Code in code font, UI elements bold, serial commas. Drop "etc."; say up front a list is partial.

Source: developers.google.com/style, 2026-07-18.

## Make statements load one at a time (STE)

- One instruction per sentence; one thought per sentence elsewhere.
- Split instructions over about 20 words and other sentences over about 25.
- Warning or condition before the step it guards: "If hot oil touches your skin, injuries can occur."
- Keep "the" and "a": "Remove backup file" reads two ways; "Remove the backup file" one.
- One meaning and one job per word, kept throughout. One word per action ("start", not also "initiate").
- Procedures as direct commands, never narration or passive: "Install the component".
- Avoid "-ing" words where you can.

Source: asd-ste100.org (Issue 9, 2025), 2026-07-18; numbered rules and dictionary are in the spec PDF.

## Leave no sentence open to two readings (Global English)

- Keep "only" and "not" next to the word they change: "only fails on growth" differs from "fails only on growth".
- Break noun strings: "the proto import budget check script" becomes "the script that checks the proto-import budget".
- Every "it", "they", "this" points at one obvious thing; repeat the noun when in doubt. Never "this" or "which" for a whole clause.
- Don't drop verbs: "Phase 1 moves the converters and Phase 2 the runtime" leaves Phase 2 without one.
- Keep structural small words ("Ensure that the switch is off"). Never trade clarity for word count.
- Repeat the article in a series when it prevents a misread: "the client and the host" for two things.
- Show what "and"/"or" joins when grouping is ambiguous; use "both...and", "either...or", "if...then".
- Periods, not semicolons. Replace an em dash with a new sentence.
- Parenthesized text is a full grammatical unit or its own sentence. No "(s)" plurals.
- No slashes: "a, b, or both", not "a/b" or "and/or".
- One name per thing everywhere ("the gate", "the ratchet", "the budget check" for one thing teaches three). Don't churn what didn't change.
- No idioms, colloquialisms, Latin abbreviations, or metaphors.

Source: Kohl, The Global English Style Guide (SAS Press), 2026-07-18.

## Repo specifics

- PR descriptions and commit messages: every layer except Diátaxis applies. A PR body is a briefing readable in under a minute; link swarm logs, SHA lists, and metric tables, don't paste them.
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
