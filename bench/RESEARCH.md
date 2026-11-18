# What the sources say about skill structure

Read 2026-11-18. Primary sources: Anthropic's [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) and [authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), the [engineering post](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), the [Agent Skills spec](https://agentskills.io/specification) and its guides on [best practices](https://agentskills.io/skill-creation/best-practices), [descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) and [evaluation](https://agentskills.io/skill-creation/evaluating-skills), [Claude Code skills](https://code.claude.com/docs/en/skills), [Codex skills](https://learn.chatgpt.com/docs/build-skills), and the anthropics/skills, openai/skills and obra/superpowers repos.

## Loading

| Level | Loaded | Budget the sources give |
|---|---|---|
| `name` + `description` | every turn, for every installed skill | about 100 tokens a skill; Claude Code caps the listing at 1% of context and each entry at 1,536 characters, Codex at 2% or 8,000 characters. Overflow cuts descriptions from the end. |
| `SKILL.md` body | when the skill fires, then for the rest of the session | under 500 lines and about 5,000 tokens; after compaction Claude Code keeps only the first 5,000 tokens |
| other files | only when read; scripts cost only their output | unbounded |

mstack adds a fourth level the sources don't cover: `hooks/scoper-instructions.js` injects the scoper body into every session and every subagent, so those words cost the most.

## Is SKILL.md plus references/ the right shape?

Yes, with two conditions the sources agree on. The folder name is a convention, not a mechanism: the spec lists `scripts/`, `references/` and `assets/` as optional, Anthropic's own skills put `REFERENCE.md` and `FORMS.md` next to `SKILL.md`, and OpenAI's curated skills use `references/` consistently. What decides whether a reference helps is:

1. **The pointer.** "Read `references/api-errors.md` if the API returns a non-200" beats "see references/". A file nothing points to never loads; a file the agent reads every run belongs inline.
2. **Depth.** Link every file straight from `SKILL.md`. Anthropic reports nested chains get partial reads (`head -100`). For files over 300 lines, put a contents list at the top.

So the split rule is by branch: what every run needs stays in `SKILL.md`, what only some runs need moves to a file behind a conditional pointer. That is already mstack's own rule in `writing/agents.md`; this change applies it where it wasn't (`write-swift`, `writing`), and flattens the one `references/x/references/` chain. `ui` keeps its router-plus-area layout: each area index acts as the area's `SKILL.md`, which is the "domain-specific organization" pattern Anthropic documents.

## What to cut

- Anything the model already does by default ("Claude is already very smart"; "would the agent get this wrong without it? If not, cut it").
- The same rule in two places: one source, others point to it.
- Menus of options; give one default and the escape hatch.
- Canned outputs and persona openers with no effect on the work.
- Time-sensitive phrasing ("current as of").

## Descriptions

Say what the skill is for and when to use it, front-load the main trigger, and name near-misses. Don't summarize the workflow: superpowers found agents follow a workflow summary in the description instead of loading the skill. Test triggering with should-fire and near-miss prompts, several runs each, with a held-out split.

## Evaluation

Run the task without the skill first, then with the old and new versions; grade with checks plus a blind judge; report pass rate next to token cost. `bench/` does this.
