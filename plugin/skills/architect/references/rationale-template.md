Prose with type sketch. One page; sentence-case headings; no boilerplate. Replace italics with content.

## Problem
One paragraph: goal and why constraints make shape non-obvious. Name [Phase A](../SKILL.md#phase-a-ground) constraints: interop types, unbreakable callers, cross-boundary invariants.

## Usage (caller's view)
Write first: README/quickstart + 2–3 realistic call sites. The sketch in [Shape](#shape) must derive from this; if they diverge, reconcile to usage. Caller experience is the spec.

## Shape
Data structures first, then data flow through signatures. State load-bearing decisions; encode invariants in types; state where validation lives. Define interface depth: what the public surface hides/exposes and why it’s minimal.

## Synthesis decision
Filled in by [arena](../../arena/SKILL.md): base candidate and why; what was adapted; what was rejected and why.

## Tradeoffs accepted
- We accept X for Y.
Include anything that could look like oversight (e.g., premature optimization/simplification).

## Alternatives considered
Required: at least one. Judge by interface depth, not implementation ease. 2–3 if real contenders. No flavors; design alternatives only.

## Open questions and risks
What needs human judgment and risks before implementation. Phrase as questions.

## Next implementation step
One sentence: the first thing to build after synthesis (or after Phase C sign-off, if opted).
