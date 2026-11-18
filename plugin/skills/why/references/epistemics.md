# Epistemics

Reason about confidence when evidence is historical, fragmentary, and contradictory, and report it without false certainty. Code shows what it does, not why it exists.

## Confidence Tiers

Every claim sits in exactly one tier, which sets its section and phrasing.

### 1. Direct

An author explicitly *wrote* why (PR description, ticket, code comment, design doc, author's chat message), e.g. a comment "// clamp to 100 because the upstream API rejects larger values". "The code does X so the author wanted X" is not Direct.

Phrasing: confident, present tense, cited. "This exists because X."

### 2. Supported

Several indirect pieces converge, none explicit, e.g. PR title "improve performance", ticket labeled "perf", surrounding commits all touching the same hot path.

Phrasing: confident but derived, citing each piece. "The evidence points strongly to X: [the pieces]."

### 3. Inferred

Your reasonable interpretation, unsupported explicitly, e.g. the error was in production (per incident channel timing) and the fix merged same day, so likely a hotfix.

Phrasing: hedged, chain explicit. "Given A and B, C seems likely because D."

### 4. Speculative

Plausible on thin evidence, with alternatives fitting equally. Present it (the user may know) but mark it a guess. Usually in Competing Hypotheses.

Phrasing: "One possibility is X, but we have no direct evidence."

### 5. Unknown

You looked and couldn't find out: a valid outcome. Name exactly what you searched: "We searched the ticket tracker with keywords A and B, scanned the 6 PRs that touched this file since 2023, and grep'd the repo for string literals matching the threshold. None surfaced a rationale."

## Phrasing Guide

- **Confidence words** need an adjacent citation and never carry inferences: "because", "the reason is", "was designed to" (author intent), "fixes" / "addresses" / "solves" (achieved its goal), "the team decided" (a group decision).
- **Hedges** go freely in What We Can Reasonably Infer: "appears to", "seems to", "likely", "suggests", "is consistent with", "one reading is", "plausibly", "may have been", "the evidence points toward".
- **Avoid:** "obviously", "clearly", "of course", dismissive "just", and "I think" / "I believe" (write "the evidence suggests").

## Avoid Rationalization

Don't retrofit a clean rationale onto messy history, assume the author did the "right" thing, read copy-paste consistency as intent, or treat absence of evidence as evidence of absence ("no one mentioned security, so it wasn't a concern"). Reasons may no longer apply or may have been wrong then.

## The Sycophancy Trap

A user's embedded hypothesis ("I assume it's for performance?") is one candidate to check independently, not a conclusion to confirm. Supported: say so with citations. Not: say so and give what the evidence does support.

## When Evidence Contradicts

Surface both sources with citations; don't pick the tidier narrative (e.g. ticket says compliance for customer X, PR says tech-debt cleanup: both may be true, or one wrong). The user decides.

## When Evidence Is Missing

An honest "we don't know" tells the user to ask a human (author, product owner, team lead) or drop the question; a confident guess in its place harms them because they act on it. Name each gap: the question, sources searched, what you searched for in each, what you found (nothing or only tangential).

## Before Finalizing

The synthesizer checks every claim in "What We Found" and "What We Can Reasonably Infer":
- It has a citation, or moves to Inferred or Hypotheses.
- Its phrasing matches its tier.
- It doesn't use code as evidence of its own intent (remove or reclassify).
- A "What We Don't Know" section exists; none listed is suspicious (unusually complete evidence, or something swept under the rug).
