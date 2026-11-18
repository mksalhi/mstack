---
name: architect
description: "Use before non-trivial code whose shape isn't obvious: sketch types, signatures and modules first. Triggers: 'architect this', 'design this'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Architect

Sketch types, function signatures, class shapes, and module boundaries with `not implemented` bodies and pseudocode. Synthesize across several model perspectives, then fill in code against the chosen sketch.

Open a todolist with one entry per phase: 1. Ground 2. Sketch 3. Agree 4. Implement 5. Scrap.

## Phase A: Ground the problem

Run `how` (`<mstack>/skills/how/SKILL.md`) over every subsystem the new code touches and produce the architectural explanation it prescribes; naming a file isn't grounding. If the design redefines ownership or layering, also run `why` (`<mstack>/skills/why/SKILL.md`) on the existing shape so its rationale becomes a constraint. Skip only for genuine greenfield with no surrounding system.

## Phase B: Sketch

Run `arena` (`<mstack>/skills/arena/SKILL.md`) with the design-sketch task and Phase A artifacts, passing `references/runner-prompt.md` as each runner's prompt.

Runners come from the `architect runners` line in `~/.claude/rules/mstack-models.md` (not `arena runners`). If the rule or line is missing, use two runners on `claude-opus-5-5`. Alias and rejected entries follow `arena`'s Phase A runner rules.

Design it twice: at least two structurally distinct whole-shape candidates before synthesis, even when the first looks sufficient (Exhaust the design space, `principles`).

Screen every candidate against [`references/design-red-flags.md`](references/design-red-flags.md); reject or revise shallow modules, information leakage, temporal decomposition, and pass-through methods.

Compare viable candidates on interface depth: prefer more complexity hidden behind a smaller, simpler public surface. A rich interface keeps call chains short by concentrating capability.

Arena returns one synthesized package; its synthesis decision fills the rationale's "Synthesis decision" section.

## Phase C: Agree (opt-in)

Default: go straight to implementation, no human checkpoint. Checkpoint only when the invoker asks ("/mstack:architect with checkpoint," "stop and show me before implementing," or similar): surface the synthesized design and pause for sign-off.

Either way the synthesis can ship as its own scaffold-first commit (Model the domain, `principles`). Planned, scoped breakage during fill-in is fine (Converge on the target, `principles`). For adversarial pressure first, run `interrogate` on the sketch.

Human pushback on the shape (at a checkpoint or later) is Phase A evidence: re-ground and re-run Phase B before writing more code.

## Phase D: Implement against the sketch

Replace `not implemented` bodies with code and pseudocode with logic. The sketch is the contract; surface deviations, never absorb them silently. If a function needs an unanticipated parameter, ask: was the sketch wrong, the requirement missed, or the implementation overreaching?

## Phase E: Scrap when the architecture is wrong

If implementation keeps producing friction the sketch can't absorb, throw it out; don't bolt fixes onto a wrong design (Converge on the target, `principles`; `debug`'s "Two fixes failed").

The signal is a *pattern*:
- The same workaround shape recurring across unrelated code.
- Several unrelated edge cases each needing special-case branches.
- Types needing escape hatches (`any`, casts, optional fields always set in practice) to compile.
- The "we need a lock" reflex when the sketch said state wasn't shared.
- Callers needing the abstraction's internal rules to use it.
- Two or more independent same-shaped Phase D deviations.

A few edge cases don't condemn an architecture; complexity in the data is not complexity in the design.

When you scrap:
1. Re-run `how` over what's built.
2. Redesign as if the new constraints were day-one assumptions (Converge on the target, `principles`).
3. Subtract before adding, per `scoper`: the new sketch is smaller than the old before it grows.
4. Return to Phase B and re-run arena.

## Outputs

Caller's usage first, type sketch derived from it. Small changes: one file of new types and signatures. Larger work: module map plus type definitions. The rationale ships alongside per `references/rationale-template.md`, including the usage sketch and synthesis decision.
