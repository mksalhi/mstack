# What is loaded when (Claude Code)
- Skill listing, every turn: `description` + `when_to_use`, capped at 1,536 characters per skill. Listing gets 1% of the context window (8,000 characters at 200k). Over budget: rank by recent use; the rest are listed by name only.
- `SKILL.md` body: from the turn it fires to session end. After compaction only its first 5,000 tokens survive.
- Any other file: only when the agent decides to `Read`. Nothing is preloaded.

## Pointers
- Always-loaded line naming material and when to reach it. Must-follow rules go inline: benchmark runs opened a linked file on 30 to 55% of runs and a two-hop file almost never. Links carry optional detail only.
- Lead with the trigger word. One trigger per branch; synonyms for one branch collapse to one.
- Say when to use it, not how it works.
- Name the near-miss when a neighbouring skill shares its words.

## Layout
- Name scripts to run, not read. Chains (`SKILL.md` to a.md to b.md) get partial reads.
- Keep a concept’s definition, rules and caveats under one heading.

## Steps
- If the agent rushes a step, sharpen its completion criterion first; split only across a real context boundary (a subagent or a handoff).

## Words
- Use leading words; define coined words.
- State the positive target; use prohibitions only as a hard guardrail, paired with the positive target.

## Pruning
- Delete no-ops and weak verbs. Don’t restate the environment; write what looking can’t find (unwritten conventions, reasons, gotchas). Delete stale lines.

## Invocation (skills)
- Model-invoked (default): keeps a description; costs listing space every turn.
- User-invoked: `disable-model-invocation: true` (listed by name only; no other skill can fire it).
- Split off a new model-invoked skill only for a distinct trigger word, or when another skill must reach it.
- `context: fork` runs the skill as a subagent so its body never enters the main context. `paths` globs hide a skill until a matching file is touched.
