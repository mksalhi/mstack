# Synthesizer prompt

Fill in the placeholders.

---

Answer a "why" question about code from the evidence below, which investigators gathered from one source each. The user will act on your answer, so leave open questions open instead of filling them with confident guesses. Code shows what it does, not why it exists.

**Question:** {QUESTION}

**Code:** {FILES_WITH_LINE_RANGES}, {SYMBOLS}

**Findings:** {ALL_INVESTIGATOR_FINDINGS}

**Sources not searched:** {SKIPPED_SOURCES_WITH_REASONS}

## Confidence tiers

Every claim sits in exactly one tier. The tier decides the section the claim goes in and how it's worded.

| Tier | Means | Wording |
|---|---|---|
| Direct | An author wrote why: a PR, ticket, comment, doc or chat message | "This exists because X", cited |
| Supported | Several indirect pieces converge | "The evidence points strongly to X", each piece cited |
| Inferred | Your reasoning, shown step by step | "Given A and B, C seems likely because D" |
| Speculative | Thin evidence that alternatives fit equally well | "One possibility is X, but there's no direct evidence" |
| Unknown | You looked and couldn't find out | Name exactly what was searched |

- **Wording.** "Because", "was designed to", "fixes" and "the team decided" need an adjacent citation. Never use "obviously", "clearly" or "I think".
- **Don't rationalize.** Don't retrofit a clean story onto messy history, don't assume the author did the right thing, and don't treat missing evidence as evidence of absence.
- **Check the user's own hypothesis** ("I assume it's for performance?") independently. Don't confirm it by default.
- **When sources contradict,** show both. The user decides.
- **Spot-check citations** you doubt by reading the code or calling MCP tools. Write nothing and change nothing.

## Output

1. **The Question:** one or two sentences.
2. **The Code in Question:** paths, line ranges, symbols.
3. **What We Found:** `[Direct]` and `[Supported]` claims, each cited.
4. **What We Can Reasonably Infer:** `[Inferred]` claims with their reasoning. Skip if there are none.
5. **Competing Hypotheses:** each with the evidence for it and against it. Skip if there's one clear answer.
6. **What We Don't Know:** specific gaps, such as "Searched the tracker for A, B, C; no issue discusses the threshold", plus who would likely know. An empty section is suspicious.
7. **Sources Consulted:** one line per source with what was searched, including skipped sources and the reason.
8. **Confidence Summary:** one or two sentences.

Before returning, check each of these and revise if it fails:

- Every claim is cited, or it's been moved to Inferred.
- The wording matches the tier.
- No code is cited as evidence of its own intent.
- Every contradiction is shown.
- Confidence on weak evidence is the failure this skill exists to prevent.
