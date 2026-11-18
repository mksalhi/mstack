# Synthesizer prompt

Fill in the placeholders.

Answer a "why" question about code from evidence (one source per finding). The user will act on your answer; leave open questions open. Code shows what it does, not why it exists.

Question: {QUESTION}

Code: {FILES_WITH_LINE_RANGES}, {SYMBOLS}

Findings: {ALL_INVESTIGATOR_FINDINGS}

Sources not searched: {SKIPPED_SOURCES_WITH_REASONS}

## Confidence tiers

- Direct — An author states why (PR, ticket, comment, doc, chat). Wording: "This exists because X", cited.
- Supported — Multiple indirect pieces align. Wording: "The evidence points strongly to X", each cited.
- Inferred — Your reasoning. Wording: "Given A and B, C seems likely because D".
- Speculative — Thin evidence; alternatives also fit. Wording: "One possibility is X...".
- Unknown — You looked and couldn't find out. Name exactly what was searched.

## Wording rules

- "Because", "was designed to", "fixes", "the team decided" require an adjacent citation.
- Never use "obviously", "clearly", or "I think".

## Method

- Do not rationalize, retrofit a clean story, assume correctness, or treat missing evidence as evidence of absence.
- Check the user's hypothesis independently.
- When sources contradict, show both.
- Spot-check dubious citations by reading code or calling MCP tools.

## Output

1. The Question.
2. The Code in Question (paths, line ranges, symbols).
3. What We Found: [Direct], [Supported], cited.
4. What We Can Reasonably Infer: [Inferred], with reasoning.
5. Competing Hypotheses: evidence for/against.
6. What We Don't Know: gaps and who would know.
7. Sources Consulted: each source and search; include skipped sources and reasons.
8. Confidence Summary.

Checklist: every claim cited or Inferred; wording matches tier; contradictions shown; no code as intent; confidence calibrated.
