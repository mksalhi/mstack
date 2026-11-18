---
name: figure-it-out
description: "Use for a large migration or ambitious multi-part change no playbook covers: design an auditable plan and hypothesis loop."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Figure it out

When no playbook fits, design one. Before any code, the deliverable is the workflow: phases whose rigor fits the task, run as experiments, leaving a decision trail a human can audit.

Open a todolist whose first item is reading `<mstack>/skills/principles/SKILL.md`, then add the phases below.

## Phase A: Frame

Don't start until you can state:

- Done, as a predicate that can come out false (Prove it works, `principles`).
- Scope in rough units and effort, plus blockers you found while grounding.
- Rigor, biased high: more gates and artifacts for one-way doors and wide blast radius, fewer for reversible low-stakes steps.

Show the framing and tradeoffs. Reversible work proceeds without waiting (Never block on the human, `principles`), but a multi-hour run gets one checkpoint.

## Phase B: Design the workflow

Split into small units that land independently, riskiest unknown first, verification before features.

- Build the verification harness first and capture a baseline from the pre-change state, so every check reads "old value vs new value".
- Run `architect` for one-way-door design decisions. Skip it for mechanical work with a settled shape.
- Fan out only across real seams, one worktree or branch per worker. Don't over-fan.
- Write the phase list down; it is what the human reviews.

Add the steps to the todolist between the Phase C and Phase D entries. Run each under Phase C, logging a Phase D row as each step lands.

## Phase C: Run the loop

Each unit is an experiment: hypothesis, smallest change, measure against the predicate on the real artifact, keep it if it moved the predicate, else revert. Verify each unit before starting the next.

- Inspect the artifact, never a self-report. If a check passes too easily, suspect the check.
- Pair delegated work with a judge. A worker gaming a check: reset it and harden the brief. A wrong check: fix it in its own change, never route around it.
- Verdicts are VERIFIED, NOT VERIFIED or INCONCLUSIVE. Inconclusive is not a pass.

## Phase D: Keep the audit trail

Log the run with `decision-log`. Usually commit the trail so the reviewer reads it with the diff.

## Phase E: Verify and hand back

Check the whole against the Phase A predicate on the real product, not just the harness. Turn any correction you made twice into a check, lint rule or script (Encode lessons in structure, `principles`).

**Reply:** the playbook you designed, the rigor level and why, the trail's path, what is verified against the predicate, and what is still open.
