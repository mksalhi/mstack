# Skill benchmark

Measures whether a change to `plugin/skills` makes skills cheaper, easier to find, and more useful. Every script takes git refs, so the "before" side can be measured after the edits.

| Script | Measures | Needs |
|---|---|---|
| `static.py [REF]` | Tokens always loaded (descriptions, the scoper hook), tokens loaded when a skill fires, reference files more than one link from `SKILL.md`, orphan files, broken links, spec lint, text duplicated across skills | nothing (`--exact` uses the Anthropic token counter) |
| `trigger/run.py` | Whether a model picks the right skill from the listing alone: 116 prompts in `trigger/queries.jsonl` (101 where an mstack skill is an acceptable pick, 15 that belong to another skill or to none), against all mstack skills plus 18 distractors from other plugins. Claude gets a Claude Code style `Skill` tool, GPT a Codex style listing with file paths. 40% of prompts are a held-out `val` split. | API key |
| `tasks/run.py` | Task outcomes for 12 skills with no skill, the old skill and the new skill: regex checks plus a judge model that never sees the condition, with tokens and reference reads per run | API key |

The prompts and tasks were committed before any skill edit, so the edits can't be fitted to them.

```bash
bench/run_all.sh origin/main HEAD    # writes bench/results/ and REPORT.md
bench/versions.sh origin/main c1b557a HEAD   # every version on the same tasks; charts and VERSIONS.md in bench/results/versions/
```

Set `BENCH_CLAUDE`, `BENCH_GPT` and `BENCH_RUNS` to change models or repeats.
