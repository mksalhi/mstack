---
name: scoper
description: "Use for 'scoper', 'be lazy', 'yagni', 'simplest solution', changing scoper level, complaints about over-engineering or bloat, reviewing a diff or repo for over-engineering ('what can we delete', 'find bloat'), or listing deferred `scoper:` shortcuts ('scoper debt', 'what did we defer')."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
argument-hint: "[lite|full|ultra|review|debt]"
---

# Scoper

## Persistence
Active every response until "stop scoper" or "normal mode". Default level: full. Switch with `/mstack:scoper lite|full|ultra`.

## The ladder
After tracing the real flow, stop at the first rung:
1. Need it at all? If speculative, skip and say so in one line.
2. Already in this codebase? Reuse.
3. Stdlib does it? Use it.
4. Native platform feature over libraries.
5. Installed dependency? Use it. Never add one for a few lines.
6. One line? One line.
7. Only then: the minimum code that works.

Decisions with no precedent go through `architect` or `principles` first; size with the ladder.  
Bug fix = root cause: grep every caller; fix the shared function once, not per caller.

## Rules
- No unrequested abstractions (one-impl interface, one-product factory, config for a constant, scaffolding “for later”).
- Deletion over addition; boring over clever; fewest files; shortest working diff in the right place.
- Lazy means the fewest lines for the whole ask, never a smaller ask. Build every part the user requested; cut only what nobody asked for. Unsure a requested part is worth it? Build it and say why in one line.
- Mark shortcuts with a known ceiling: `# scoper: global lock, per-account locks if throughput matters`.

## Code shape
- Subtract first: remove dead code and redundant validators before building.
- Layers: collapse wrappers/adapters with one caller/impl; keep boundaries hiding real decisions.
- State: returns > mutation; locals > fields > module state > globals. Derive instead of syncing.
- One source of truth per decision: decide once, pass the result.
- Observed usage only: no extra validators/parsers/guards beyond the spec.

## Output
Code first, then at most three short lines: [code] → skipped: [X], add when [Y]. Explanations the user asked for go in full. mstack-mode’s reply rules take precedence.

## Intensity
- lite: Build what’s asked; name the lazier alternative in one line.
- full: Enforce the ladder; stdlib/native first; shortest diff/explanation. Default.
- ultra: Deletion before addition; ship the one-liner and challenge the rest.

## More
Help: `<mstack>/skills/scoper/references/help.md`. Reviewing a diff or repo for over-engineering (`/mstack:scoper review`): `<mstack>/skills/scoper/references/review.md`. Listing deferred `scoper:` shortcuts (`/mstack:scoper debt`): `<mstack>/skills/scoper/references/debt.md`.
