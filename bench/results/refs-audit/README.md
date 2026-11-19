# Reference-file audit benchmark

Question: do models open linked reference files, and does moving must-follow rules out of them into `SKILL.md` change answer quality?

Change under test: d9be350 ("Move must-follow rules out of nested reference files into SKILL.md"). Base: addedb4.

## Method

- Full task suite (`bench/tasks/tasks.json`, 39 tasks), 3 runs per task per condition, `gpt-6.2-sol` at low reasoning effort, scoper body in the system prompt (`--hook`).
- Conditions: `none` (no skills), `old` (addedb4 skills), `new` (d9be350 skills). Every file the model opened is logged in `reads`.
- Grading: 6 Claude graders read shuffled packets with the condition hidden (`grading-packets/`). Each check gets pass or fail plus a one-line reason (`claude-grades/group*.out.json`). `claude-grades/key.json` maps each response id to its condition and run.

## Results

| | old | new |
|---|---|---|
| Claude blind grade (check pass rate) | 363/393 (92.4%) | 366/393 (93.1%) |
| GPT judge plus regex score | 0.881 | 0.903 |
| Runs that opened any file | 45/117 | 45/117 |
| Reference or playbook files opened | 72 | 57 |
| Files opened per run | 0.90 | 0.74 |

Per-task Claude grades: `SCORES.txt`. Differences per task are 1 to 3 checks out of 9 to 12 and go both ways. The three drops (arena-frame, how-explain, ambition-rewrite) fail checks whose rule text this change did not touch; read the reasons in `claude-grades/`.

Reading: quality held while 20 reference files were deleted and must-follow rules moved inline. Models still open a linked file in about 38% of runs, so links now carry optional detail only.

## Files

- `runs-gpt.json`: every run with task, condition, checks, judge result, token usage, files opened and the full answer text.
- `grading-packets/`: the exact packets and brief the Claude graders saw.
- `claude-grades/`: grader output with reasons, plus the condition key.
- `SCORES.txt`: per-task Claude grades, old versus new.
