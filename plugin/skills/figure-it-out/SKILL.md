---
name: figure-it-out
description: "Use for a large migration or ambitious multi-part change no playbook covers: design an auditable plan and hypothesis loop."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Figure it out

Open a todolist; first item: read `<mstack>/skills/principles/SKILL.md`.

## Phase A: Frame

- Done as a falsifiable predicate.
- Scope (rough effort/units) and blockers.
- Rigor: bias high for one-way doors.

Reversible work proceeds (Never block on the human, `principles`).

## Phase B: Design the workflow

Riskiest unknown first.
- Build the verification harness first; capture a pre‑change “old vs new” baseline.
- Run `architect` for one‑way‑door decisions; skip for settled mechanical work.
- Add steps to the todolist between Phase C and Phase D.
Run each under Phase C; log Phase D as steps land.

## Phase C: Run the loop

Per unit: hypothesis → smallest change → measure on the real artifact against the predicate; keep if it moved; else revert; verify before the next.
- Inspect the artifact, never a self‑report; suspect easy passes.
- Delegate + judge; if gaming, reset + harden; if the check is wrong, fix it in its own change (never route around).
- Verdicts: VERIFIED, NOT VERIFIED, INCONCLUSIVE.

## Phase D: Keep the audit trail

Log with `decision-log`.

## Phase E: Verify and hand back

Verify against the Phase A predicate. Turn repeats into a check, lint rule, or script (Encode lessons in structure, `principles`).

Reply: the playbook, rigor level and why, the trail’s path, what is verified against the predicate, and what is still open.
