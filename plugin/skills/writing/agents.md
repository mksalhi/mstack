# Writing for agents

For any document an agent reads: a skill, `AGENTS.md` or `CLAUDE.md`, or a doc reached by a pointer. The goal is that the agent takes the same process every run.

## What is loaded when (Claude Code)

- **Skill listing, every turn:** `description` plus `when_to_use`, capped at 1,536 characters per skill. The whole listing gets 1% of the context window (8,000 characters at 200k). Over budget, skills are ranked by recent use and the rest are listed by name only.
- **`SKILL.md` body:** from the turn it fires to the end of the session. After compaction only its first 5,000 tokens survive.
- **Any other file:** only when the agent decides to `Read` it. Nothing is preloaded.

Codex lists skills up to 2% of context or 8,000 characters and reads `SKILL.md` through the shell. Details and sources: `bench/RESEARCH.md` in the mstack repo.

## Pointers

A pointer is an always-loaded line naming material and when to reach it: a skill description, or an `AGENTS.md` line naming a doc. Its wording decides whether the agent reaches the material. If a must-have file is missed, sharpen the pointer first; inline the material only if that fails.

- Lead with the trigger word. One trigger per branch (a distinct case the document handles); synonyms for one branch collapse to one.
- Say when to use it, not how it works. An agent that reads a workflow summary in a description tends to follow the summary and skip the skill.
- Name the near-miss when a neighbouring skill shares its words ("For what changed in this chat, use ketchup").

## Layout

- Inline what every branch needs; put what only some branches need in a file that `SKILL.md` names with its condition ("Read `references/x.md` before Y"). Name scripts to run, not read.
- Link every file from `SKILL.md` directly. Chains (`SKILL.md` to a.md to b.md) get partial reads.
- Keep `SKILL.md` under about 5,000 tokens. Put a contents list at the top of a reference file over 300 lines.
- Keep a concept's definition, rules and caveats under one heading. One authoritative place per meaning.

## Steps

End every step on a completion criterion the agent can check. "Every modified model accounted for" forces work that "produce a change list" doesn't. If the agent rushes a step to reach the next ones, sharpen the criterion first; splitting the sequence only helps across a real context boundary (a subagent or a handoff).

## Words

- A leading word is an existing concept the agent already thinks with (_tight_ loop, _red_ test, _fog of war_). One word recruits a whole behaviour; a coined word recruits nothing and must be defined.
- State the positive target ("write one-line comments"). A prohibition puts the forbidden behaviour in context; use one only as a hard guardrail, paired with the positive target.

## Pruning

- Delete no-ops: sentences the model follows by default. Delete the whole sentence. A word too weak to beat the default (_be thorough_) is a no-op; use a stronger one (_relentless_) or cut it.
- Don't restate the environment (`package.json` scripts, config, `--help`). Write what looking can't find: unwritten conventions, the reason for a choice, gotchas.
- Delete stale lines. Sediment builds because adding feels safe and removing feels risky.

## Invocation (skills)

- **Model-invoked** (default): keeps a description so the agent and other skills can fire it. Costs listing space every turn.
- **User-invoked:** `disable-model-invocation: true`. Listed by name only, and no other skill can fire it. Use it when only a human should start it.
- Split off a new model-invoked skill only when a distinct word you use in prompts should fire it alone, or another skill must reach it.
- `context: fork` runs the skill as a subagent so its body never enters the main context. `paths` globs hide a skill until a matching file is touched.
