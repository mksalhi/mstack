---
name: decision-log
description: "Use on long, autonomous or multi-phase work a human reviews later: keep a TSV log of each decision with its evidence."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Decision log

One log of decisions and their evidence, for a human reviewing long or autonomous work later. Other skills point here instead of restating the format.

## Format

One TSV file, one row per decision, single-line cells. Columns, as in `references/decision-log-template.tsv`:

- **ts.** ISO8601 timestamp.
- **phase.** Phase or workstream.
- **decision.** What was chosen or done, one line.
- **why.** The reason in plain words.
- **evidence.** Commit SHA, PR number, `file:line`, or artifact, trace, or screenshot path. Never a paragraph.
- **result.** Outcome or predicate state: `tests green`, `reverted`, `pixel-diff 0`, `INCONCLUSIVE`, `open`.

Write rows as you'd tell a teammate.

```
ts	phase	decision	why	evidence	result
2026-05-24T11:15:00Z	widget	moved the widget styles over without changing how it looks	keep the change small and the result identical	commit 7c21e0a, pixel-diff 0	looks identical, tests pass
2026-05-24T12:30:00Z	widget	threw out a helper's work because its screenshots were blank	checked the real files instead of trusting its summary	worktree reset	reverted, tightened the instructions for next time
```

## Log a row

Run `scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>`. It stamps `ts`, writes the header on first use, strips tabs and newlines, and quotes cells starting with `=`, `+`, `-` or `@` so spreadsheets don't run them.

Log decision points, not every action: a fork chosen, a unit finished with its verification result, a pivot or revert and its trigger, a blocker, a gate fixed. In a loop, one row per iteration.

A run is one agent conversation; a pickup, replacement agent or new chat is a new run. When your run writes to a log that already has rows, or that another run wrote to since your last row, first read the last rows, then write a row with phase `start` whose decision names the `ts` range you didn't write and whose evidence names your run (e.g. agent id). Use `start` for nothing else.

## Where it lives

Default: uncommitted, at `decisions.tsv` in the work dir, or `.audit/<task-slug>.tsv` when several efforts run at once. Commit it only when a reviewer needs the trail to trust the result.

## Rules

- Append-only. Supersede a wrong call with a new row; never edit or delete history.
- Prefer evidence from committed scripts over one-off commands.

## Before handing back

### Audit the log against the transcript

Read this run's transcript (per `<mstack>/skills/mstack-mode/references/transcripts.md`; never glob `~/.claude/projects/*/`) against the rows this run wrote:

- Every row maps to a real decision or action.
- Every evidence pointer resolves and shows what it claims.
- An unlogged fork, pivot or abandoned approach that shaped the work is a gap: add it.

Never edit or remove a row, even a wrong one: add a superseding row. Other runs' rows are not yours to audit, but supersede one if your work shows it wrong.

### Cross-model review of the trail

Spawn a subagent on a different model family from yours. It reads the trail and transcript and flags, without redoing the work:

- Decisions with weak or absent evidence.
- Verification skipped or claimed without proof in the transcript.
- Choices risky in hindsight (premature, scope-creeping, papering over a symptom).
- Gaps a casual skim would miss.

End every reply for a run with a trail with an "Attention" section: first line `reviewed by <model>`, then each flag with the rows it concerns, or "No flags".

## Reviewing the trail

GitHub renders a committed TSV as a table; `column -s$'\t' -t decisions.tsv` renders it in a terminal.
