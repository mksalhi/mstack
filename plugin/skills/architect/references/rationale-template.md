# Rationale template

Prose shipped with the type sketch. One page, sentence-case headings, no boilerplate. Replace the italic notes with content.

## Problem

*One paragraph: the goal, and what in the existing system or constraints makes the shape non-obvious. Name constraints [Phase A](../SKILL.md#phase-a-ground-the-problem) surfaced (types to interop with, callers we can't break, invariants crossing our boundary).*

## Usage (caller's view)

*Write first, before the type sketch: the README or quickstart the consumer reads, plus two or three realistic call sites (imports, calls, return values). The sketch in [Shape](#shape) derives from this; when they diverge, reconcile the sketch to the usage. The caller's experience is the spec.*

## Shape

*The recommended architecture: data structures first, then data flow through the signatures. Name load-bearing decisions, invariants encoded in types, where validation lives, and what the system deliberately does not do. Judge interface depth: what the public surface hides, what stays exposed, why it is no larger than needed. Cite the principle behind each decision (e.g., "per Boundary discipline"); don't restate it.*

## Synthesis decision

*Filled in by [arena](../../arena/SKILL.md): which candidate became the base and why, what was adapted from each other one, what was rejected and why.*

## Tradeoffs accepted

*One bullet each: "we accept X in exchange for Y." Name anything a future reader might mistake for an oversight, including apparent premature optimization or simplification.*

## Alternatives considered

*Required. At least one concrete alternative shape, one line on why it lost, judged on interface depth (complexity exposed vs hidden), not implementation simplicity alone. Two or three when there were real contenders; one is fine when constraints forced the answer ("the only viable shape because..."). No flavors of the same shape. Design alternatives only, not other runner candidates.*

## Open questions and risks

*What the human must weigh in on and risks to flag before implementation. Phrase as questions so the answer is the resolution.*

## Next implementation step

*One sentence: the first thing to build after synthesis (or after Phase C sign-off, if a checkpoint was opted into).*
