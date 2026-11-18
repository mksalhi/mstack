---
name: decision-log
description: "Use on long, autonomous or multi-phase work a human reviews later: keep a TSV log of each decision with its evidence."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Decision log

Keep one canonical log. Other skills route their audit trail here by name; don't restate the columns there.

## Format

One TSV file, one row per decision, single-line cells, evidence as a pointer. Start from `references/decision-log-template.tsv` (header row). Columns:

- **ts.** ISO8601 timestamp.
- **phase.** Phase or workstream.
- **decision.** What was chosen or done, one line.
- **why.** The reason in plain words; name a driving principle plainly, not as a jargon tag.
- **evidence.** Commit SHA, PR number, `file:line`, or artifact, trace, or screenshot path. Never a paragraph.
- **result.** Outcome or predicate state: `tests green`, `reverted`, `pixel-diff 0`, `INCONCLUSIVE`, `open`.

Write rows as you'd tell a teammate: plain words, concrete actions (the unslop pass applies).

```
ts	phase	decision	why	evidence	result
2026-05-24T11:15:00Z	widget	moved the widget styles over without changing how it looks	keep the change small and the result identical	commit 7c21e0a, pixel-diff 0	looks identical, tests pass
2026-05-24T12:30:00Z	widget	threw out a helper's work because its screenshots were blank	checked the real files instead of trusting its summary	worktree reset	reverted, tightened the instructions for next time
```

## Log a row

`scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>` stamps `ts`, writes the header on first use, strips tabs and newlines, and prefixes cells starting with `=`, `+`, `-`, or `@` with a single quote. A bare `printf` works, but handle those bytes for generated or user-supplied cells.

Log decision points and checkpoints, not every action: a fork chosen, a unit completed with its verification result, a pivot or revert with its trigger, a blocker surfaced, a gate fixed. Loop runs: one row per iteration.

A run is one agent conversation, including later turns and summaries of it; a pickup, replacement agent, or new chat is a new run. When a run adds to a log with existing rows, its first row has phase `start`, and so does its first row after another run's `start` row, so a run returning in a later turn first reads the log's last rows. A `start` row names the `ts` range of preceding rows this run did not write; its evidence names this run (e.g. agent id). Use `start` for nothing else.

## Where it lives

Default: an uncommitted working artifact, out of git, at `decisions.tsv` in the work dir, or `.audit/<task-slug>.tsv` when several efforts run at once. Commit it only when a reviewer needs the trail to trust the result.

## Rules

- Append-only. Supersede a wrong call with a new row; never edit or delete history.
- Prefer evidence from committed scripts over hand-made one-offs (Encode lessons in structure, `principles`).

## Before handing back

### Audit the log against the transcript

Read this run's transcript (per `<mstack>/skills/mstack-mode/references/transcripts.md`; never glob ~/.claude/projects/*/) and walk this run's rows. Each stretch starts at one of this run's `start` rows (or the first row if this run created the log) and ends at another run's next `start` row.

- Every row maps to a real decision or action.
- Each row's evidence resolves and shows what it claims.
- An unlogged fork, pivot, or abandoned approach that shaped the work is a gap: add it.

Never edit or remove a row, even an invented one: add a superseding row with what happened and a resolving pointer. Rows outside this run's stretches are not audited, but supersede one if this run's work shows it wrong.

### Cross-model review of the trail

Spawn a subagent on a different model family from the worker (self-review doesn't count). It reads the trail and transcript and flags, without redoing the work:

- Decisions with weak or absent evidence.
- Verification skipped or claimed without proof in the transcript.
- Choices risky in hindsight (premature, scope-creeping, papering over a symptom).
- Gaps a casual skim would miss.

Every reply for a run with a trail ends with an "Attention" section: first line `reviewed by <model>`, then each flag pointing to rows or moments. "No flags" is valid; omitting the model is not.

## Reviewing the trail

Read top to bottom, follow evidence pointers, spot-check. GitHub renders a committed TSV as a table; `column -s$'\t' -t decisions.tsv` renders it in a terminal.
