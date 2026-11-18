---
name: architect
description: "Use before non-trivial code whose shape isn't obvious: sketch types, signatures and modules first. Triggers: 'architect this', 'design this'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Architect

Sketch types, signatures, and module boundaries with not implemented bodies; pick the best of several sketches, then implement strictly against it.

Open a todolist: Ground, Sketch, Agree, Implement, Scrap.

## Phase A: Ground
- Run how (<mstack>/skills/how/SKILL.md) for every subsystem touched; naming a file isn’t grounding.
- If ownership/layering changes, also run why (<mstack>/skills/why/SKILL.md).
- Skip only for true greenfield.

## Phase B: Sketch
- Run arena (<mstack>/skills/arena/SKILL.md) with the design-sketch task and Phase A artifacts, passing [references/runner-prompt.md](references/runner-prompt.md) as each runner’s prompt.
- Use the architect runners in ~/.claude/rules/mstack-models.md (not arena runners); else two on claude-opus-5-5.
- Produce at least two structurally different candidates.
- Screen each against [references/design-red-flags.md](references/design-red-flags.md); pick the survivor that hides the most complexity behind the smallest public surface.

## Phase C: Agree (opt-in)
- Show the sketch only if the user asks; then wait.
- Any pushback is new Phase A evidence: re-ground and redo Phase B.

## Phase D: Implement
- Fill bodies; the sketch is the contract. Report every deviation.
- If a function needs a missing parameter, decide: sketch wrong, missed requirement, or overreach.

## Phase E: Scrap
- Scrap on: recurring workarounds; cascading edge-case branches; escape-hatch types (any/casts/“optional but always set”); “we need a lock” vs. non-shared-state sketch; callers needing internals; multiple independent Phase D deviations.
- To scrap: re-run how (<mstack>/skills/how/SKILL.md), redesign with new constraints, make the new sketch smaller first (scoper), then redo Phase B.

## Outputs
- Caller usage first, then the type sketch. Ship the rationale per [references/rationale-template.md](references/rationale-template.md).
- Small change: one file of types/signatures. Larger: module map plus types.
