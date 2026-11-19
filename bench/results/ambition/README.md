# Ambition benchmark data

Refs: old = `4ee3b10` (main before PR 6), new = `bf166ae`. GPT (`gpt-6.2-sol`, low reasoning) runs every task. Claude (Opus 5.5 subagents, one per task) grades the answers blind: the packets shuffle responses and hide the condition, and `claude-grades/key.json` maps each response id back to it.

| File | What it holds |
|---|---|
| `runs-gpt-mstack-mode-with-hook.json` | 5 ambition tasks x none/old/new x 6 runs, with the scoper hook text in the system prompt as real sessions have it. Full answer text, files read, and the GPT judge's grades. |
| `runs-gpt-scoper-only.json` | 4 ambition prompts with only scoper loaded (no mstack-mode), old vs new, 6 runs each. Answer text and files read. |
| `dataset.json` | Everything in one file: tasks, prompts, assertions, every answer, files read, GPT grades, Claude grades with a one-sentence rationale, and the exact skill text each condition saw. |
| `report.html` | Browsable report over `dataset.json` (open it next to that file). |
| `SCORES.txt` | Claude-graded score per task and condition. |
| `grading-packets/` | The blind packets the Claude graders read (shuffled, condition hidden). |
| `claude-grades/*.out.json`, `*.rationale.json` | Claude's pass/fail per assertion, and the same with rationale. |
| `claude-grades/key.json` | Response id to condition (`none`, `old`, `new`, `scoper-old`, `scoper-new`). |
| `aggregate.py` | Rebuilds `SCORES.txt` from the grades and key. |
| `build_dataset.py`, `run_scoper_only.py` | Scripts that built `dataset.json` and ran the scoper-only condition (paths point at the scratch dir they ran in). |
| `reference-reads.txt` | How often runs opened files beyond the injected SKILL.md, including `code-is-cheap.md`. |
| `SOURCES.md` | The research behind the change. |

Older full-suite runs (GPT judge) are in `../tasks-gpt-6.2-sol.json`, `../tasks-gpt-6.2-sol-recheck.json` and `../REPORT.md`. Task prompts and assertions are in `bench/tasks/tasks.json` (ids starting `ambition-`).
