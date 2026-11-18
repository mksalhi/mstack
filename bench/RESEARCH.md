# How agents consume skills, and what that means for mstack

Sources, read 2026-11-18:

- **Claude Code 2.1.327 itself.** I read the skill loader, the listing budget and the compaction code by extracting strings from the installed binary (`/opt/claude-code/bin/claude`). This is the ground truth for Claude Code; where it disagrees with the docs, it wins.
- **Anthropic's docs:**
  - [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
  - [authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
  - [Claude Code skills](https://code.claude.com/docs/en/skills)
  - the [engineering post](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- **The [Agent Skills spec](https://agentskills.io/specification)** and its guides on [descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) and [evaluation](https://agentskills.io/skill-creation/evaluating-skills).
- **[Codex skills](https://learn.chatgpt.com/docs/build-skills).**
- **Example skills:** anthropics/skills, openai/skills and obra/superpowers.

## 1. What is in context, and when

| What | When it costs tokens | Limit (Claude Code source) |
|---|---|---|
| Skill listing: `name` plus `description` plus ` - ` plus `when_to_use` | Every turn, every session, every subagent with the Skill tool | The whole listing gets `contextWindow × 4 chars × 0.01`: 8,000 characters at 200k context, 40,000 at 1M. Each entry is cut at 1,536 characters (`skillListingMaxDescChars`). |
| `SKILL.md` body | From the turn the skill fires until the session ends | Prefixed with `Base directory for this skill: <dir>`. Files over 1 MB are skipped. |
| `SKILL.md` after compaction | Every turn after compaction | Each invoked skill keeps its first 5,000 tokens; all invoked skills together keep 25,000, most recent first. Anything cut gets `[... skill content truncated for compaction; use Read on the skill path if you need the full text]`. |
| Any other file in the skill folder | Only when the model decides to `Read` it | None. Nothing is preloaded, and Codex is the same. |
| Scripts | Only their output, when run | None |
| mstack's SessionStart and SubagentStart hooks | Every session and every subagent, before anything else | mstack-specific: the filtered `scoper/SKILL.md`, 897 tokens after this PR. |

**When the listing is over budget, Claude Code doesn't cut every description evenly.**

- Bundled skills always keep their full entries.
- Every other skill is ranked by usage: usage count × 0.5^(days since last use / 7).
- Skills are added back in that order until the budget runs out. Whatever doesn't fit is listed by name only, and it logs `Skill listing over budget`.

So for a user with several plugins, the skills they haven't touched lately lose their descriptions first, and a name alone rarely routes.

**Codex uses a different budget.** It lists skills up to 2% of context or 8,000 characters, and loads a skill by reading `SKILL.md` through the shell.

## 2. Frontmatter fields that change cost (Claude Code)

The binary's schema has these fields; the docs list most of them.

- `when_to_use`: appended to the description in the listing. It counts against the same 1,536-character cap.
- `paths`: glob patterns. The skill is a **conditional skill**: it stays out of the listing until the model touches a matching file. mstack doesn't use this anywhere.
- `disable-model-invocation: true`: the skill is listed by name only and the model can't call it. It's for user-only commands.
- `context: fork` plus `agent`: the skill runs as a subagent instead of expanding into the conversation, so its body never enters the main context.
- `allowed-tools`, `model`, `hooks`.

## 3. What follows

1. **Every word in a `SKILL.md` body is paid for as long as the session lasts, and anything past 5,000 tokens is lost at compaction.** Bodies should hold only what every run of the skill needs.
2. **A reference file costs nothing until it's read, and is useless if it isn't.** Each reference needs a pointer in `SKILL.md` that says when to read it. Nesting matters because the model reads from the file it's in. Anthropic reports partial reads (`head -100`) on files two hops down, so link every file directly from `SKILL.md`.
3. **The folder name is only a convention.** The spec lists `scripts/`, `references/` and `assets/` as optional. Anthropic's own skills keep `REFERENCE.md` and `FORMS.md` beside `SKILL.md`, while OpenAI's curated skills use `references/`. Keep `references/`; it's what mstack already does.
4. **Cut what the model already knows.** Anthropic: "Claude is already very smart. Only add context Claude doesn't already have." The test for each paragraph is whether the agent would get it wrong without it.
5. **Descriptions route; they don't instruct.**
   - Say what the skill is for and when to use it, with the trigger words first.
   - Don't summarize the workflow. Superpowers found that agents act on a workflow summary in the description and skip loading the skill.
   - mstack's 31 descriptions total about 5,600 characters. That fits an 8,000-character budget alone, but not next to a few other plugins.
6. **Test with evals, not intuition.**
   - Run the task with no skill first, then with the old and the new skill.
   - Check triggering with should-fire and near-miss prompts, over several runs, with a held-out split.
   - `bench/` does all of this.

## 4. How this PR applies it

- **Prose.** I rewrote every markdown file to keep only what a capable model would get wrong: numbers, non-default opinions, gotchas, and steps tied to this repo's scripts. General design, accessibility and writing advice the model already follows was deleted, not moved.
- **Structure.**
  - Kept `SKILL.md` plus `references/`, with every reference linked from `SKILL.md` under a read-when condition.
  - Flattened the nested chain.
  - Deleted orphan files.
- **Bodies.** No body is over 5,000 tokens, so none loses its tail at compaction.
- **Listing.**
  - Descriptions stay short, with triggers first.
  - `write-swift` gets `paths: ["**/*.swift"]`, so it's only listed when Swift is in play.
