---
name: decision-log
description: "Use on long, autonomous or multi-phase work a human reviews later: keep a TSV log of each decision with its evidence."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Decision log

## Format
One TSV file, one row per decision, single-line cells. Columns as in `references/decision-log-template.tsv`.

## Log a row
Run:
```
scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>
```
Log decision points, not every action. In a loop, one row per iteration.

A run is one agent conversation; a pickup, replacement agent, or new chat is a new run. If your run writes to a log that already has rows, or that another run wrote to since your last row: read the last rows, then write a row with phase `start` whose decision names the `ts` range you didn’t write and whose evidence names your run (e.g. agent id). Use `start` for nothing else.

## Where it lives
Default: uncommitted, at `decisions.tsv` in the work dir, or `.audit/<task-slug>.tsv` when several efforts run at once. Commit only when a reviewer needs the trail.

## Rules
- Append-only. Supersede a wrong call with a new row; never edit or delete history.
- Prefer evidence from committed scripts over one-off commands.

## Before handing back

### Audit the log against the transcript
Read this run’s transcript (`~/.claude/projects/<slug>/<session-uuid>.jsonl`, where the slug is the working directory with `/` and `.` turned into `-`; never glob `~/.claude/projects/*/`) against the rows this run wrote:
- Every row maps to a real decision or action.
- Every evidence pointer resolves and shows what it claims.
- Any unlogged fork, pivot, or abandoned approach that shaped the work is a gap: add it.

Never edit or remove a row, even a wrong one: add a superseding row. Other runs’ rows are not yours to audit, but supersede one if your work shows it wrong.

### Cross-model review of the trail
Spawn a subagent on a different model family. It reads the trail and transcript and flags, without redoing the work:
- Weak/absent evidence.
- Verification skipped or claimed without proof.
- Risky choices in hindsight.
- Gaps a casual skim would miss.

End every reply for a run with a trail with an “Attention” section: first line `reviewed by <model>`, then each flag with the rows it concerns, or “No flags”.
