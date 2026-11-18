---
name: architect
description: "Use before non-trivial code whose shape isn't obvious: sketch types, signatures and modules first. Triggers: 'architect this', 'design this'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Architect

Sketch types, signatures and module boundaries with `not implemented` bodies, pick the best of several sketches, then implement against it.

Open a todolist: Ground, Sketch, Agree, Implement, Scrap.

## Phase A: Ground the problem

Run `how` (`<mstack>/skills/how/SKILL.md`) over every subsystem the new code touches; naming a file isn't grounding. If the design changes ownership or layering, also run `why` (`<mstack>/skills/why/SKILL.md`) so the existing shape's rationale becomes a constraint. Skip only for greenfield code with no surrounding system.

## Phase B: Sketch

Run `arena` (`<mstack>/skills/arena/SKILL.md`) with the design-sketch task and Phase A artifacts, passing `references/runner-prompt.md` as each runner's prompt.

Runners: the `architect runners` line in `~/.claude/rules/mstack-models.md` (not `arena runners`), else two on `claude-opus-5-5`.

Get at least two structurally different candidates, even when the first looks good enough (Exhaust the design space, `principles`).

Screen every candidate against [`references/design-red-flags.md`](references/design-red-flags.md). Among the survivors, prefer the one hiding the most complexity behind the smallest public surface. Arena's synthesis decision fills the rationale's "Synthesis decision" section.

## Phase C: Agree (opt-in)

Go straight to implementation unless the user asked to see the design first ("with checkpoint", "show me before implementing"); then show it and wait. The sketch can land as its own scaffold commit. For adversarial pressure, run `interrogate` on the sketch.

Pushback on the shape, now or later, is new Phase A evidence: re-ground and redo Phase B before writing more code.

## Phase D: Implement against the sketch

Fill in the bodies. The sketch is the contract: report every deviation. When a function needs a parameter the sketch lacks, decide whether the sketch was wrong, a requirement was missed, or the implementation is overreaching.

## Phase E: Scrap when the architecture is wrong

When implementation keeps fighting the sketch, throw the sketch out rather than bolting fixes on (Converge on the target, `principles`). The signal is a pattern:
- The same workaround shape recurring across unrelated code.
- Several unrelated edge cases each needing special-case branches.
- Types needing escape hatches (`any`, casts, optional fields always set in practice) to compile.
- The "we need a lock" reflex when the sketch said state wasn't shared.
- Callers needing the abstraction's internal rules to use it.
- Two or more independent same-shaped Phase D deviations.

A few edge cases don't condemn a design; complex data is not a complex design.

To scrap: re-run `how` over what's built, redesign as if the new constraints were known on day one, make the new sketch smaller than the old before it grows (`scoper`), and redo Phase B.

## Outputs

Caller's usage first, then the type sketch derived from it: one file of types and signatures for a small change, a module map plus types for larger work. Ship the rationale alongside, per `references/rationale-template.md`.
