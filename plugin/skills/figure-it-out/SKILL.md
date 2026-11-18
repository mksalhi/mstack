---
name: figure-it-out
description: "Use for a large migration or ambitious multi-part change no playbook covers: design an auditable plan and hypothesis loop."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Figure it out

When no playbook fits, design one. The deliverable before any code is the workflow: phases that scale rigor to the task, run the scientific method, and leave a decision trail a human can audit later.

Open a todolist whose first item is reading the Principles section of `mstack-mode` (`<mstack>/skills/mstack-mode/SKILL.md`), then add the phases below.

## Phase A: Frame

Ground first. Don't start the run until you can state:
- Definition of done as a falsifiable predicate (Prove it works, `principles`).
- Scope, quantified: rough units and effort, plus blockers grounding surfaced.
- Rigor level, biased high: more for one-way doors and high blast radius, less for reversible low-stakes steps. Rigor is gates and artifacts, not "try harder".

Present the framing and tradeoffs before committing. Reversible work proceeds (Never block on the human, `principles`), but a multi-hour run earns one checkpoint.

## Phase B: Design the workflow

Decompose into atomic, independently landable units, riskiest unknown first; scaffold and verification before features (Prove it works, `principles`, Delivery order).
- Build the verification harness first, baseline captured from the pre-change state, so checks read "old value vs new value".
- One-way-door design decisions: run `architect` (it runs `arena`). Skip for mechanical work whose shape is concrete; a second arena over a settled design is over-engineering (`scoper`).
- Fan out only across seams, each worker in its own worktree or branch (Separate before serializing shared state, `principles`). Don't over-fan.
- Write the phase list down; that is what the human reviews.

Then add its steps to the todolist as concrete items between the Phase C and Phase D entries. Run each under the Phase C loop, logging a Phase D row as each step lands, not all at the end.

## Phase C: Run the loop

Each unit is an experiment: hypothesis, smallest change, measure against the predicate on the real artifact, keep if it advanced, else revert. Verify each unit before the next (Prove it works, `principles`, Per unit).
- Verify by inspecting the artifact, never a self-report. Passing too easily? Suspect the observation method before the system.
- Pair delegated work with a judge. A worker gaming the gate: reset and harden the contract. A wrong gate: fix it in its own change, never route around it.
- Verdicts: VERIFIED, NOT VERIFIED, or INCONCLUSIVE. Inconclusive is not a pass. Don't hide a negative.

## Phase D: Keep the audit trail

Log the run with `decision-log`. Usually commit the trail so the reviewer reads it in the PR; trail plus diff is what earns trust.

## Phase E: Verify and hand back

Check the whole against the Phase A predicate on the real product, not just the harness. Encode any recurring correction as a gate, lint rule, check, or script (Encode lessons in structure, `principles`).

**Reply:** the playbook you designed, rigor level and why, decision-trail path, what's verified against the predicate, what's still open.
