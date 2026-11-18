# Synthesizer Prompt Template

Fill in the placeholders.

---

Answer a "why" question about code by synthesizing findings from investigators who each searched one historical source. Produce a confidence-weighted, cited narrative that says honestly what the evidence supports and what it doesn't. The user will act on it: leave open questions open rather than fill them with confident guesses.

## The Question

> {QUESTION}

## The Code Anchor

**Target files:** {FILES_WITH_LINE_RANGES}

**Key symbols:** {SYMBOLS}

## Investigator Findings

{ALL_INVESTIGATOR_FINDINGS}

## Sources That Weren't Searched

{SKIPPED_SOURCES_WITH_REASONS}

## Epistemics Framework

You MUST read `references/epistemics.md` in full before writing and follow it: every claim sits in one tier (**Direct**, **Supported**, **Inferred**, **Speculative**, **Unknown**), which sets its section, phrasing, and citation.

## Instructions

1. **Weigh all findings yourself**: investigators gathered evidence, not conclusions.
2. **Merge overlaps**: one authoritative reference per PR, ticket, or doc.
3. **Surface contradictions**: show both sides.
4. **Calibrate each claim** to its tier: Direct stated plainly and cited, Inferred hedged with the chain shown, Speculative marked, no evidence goes to gaps.
5. **Spot-check citations** you doubt by reading the codebase or calling MCP tools. Write no files, commit nothing, modify no external state.

## Output Format

Write for the user, in this exact structure:

---

### The Question

Restate the question in one or two sentences.

### The Code in Question

File paths, line ranges, key symbols: two or three lines for a cold reader.

### What We Found

Claims with textual evidence, quoted or paraphrased and cited precisely. `[Direct]`: single-source explicit evidence. `[Supported]`: several indirect items converging.

- **[Direct]** {Claim}. Source: [PR #123](url) / ticket ID / file:line. {Brief quote or paraphrase.}
- **[Supported]** {Claim}. Evidence: {list of items and what each contributes}.

### What We Can Reasonably Infer

Claims stated nowhere but well supported, each hedged and showing its chain ("Given A and B, it's likely that C"). Skip if none.

- **[Inferred]** {Hedged claim}. Reasoning: {the specific evidence and the inference step}.

### Competing Hypotheses

When the evidence fits several stories, present each without forcing a winner. Skip if one clear answer.

- **Hypothesis:** {one-sentence statement}
- **Evidence for:** {specific items}
- **Evidence against or missing:** {what would need to be true but isn't, or counter-signals}

### What We Don't Know

Specific gaps ("We searched the issue tracker for [query1], [query2], [query3] and found no issue discussing the rate-limit threshold", not "We don't know why"): unanswered questions, empty searches, unavailable sources and why (e.g. no real-time team chat MCP), people who would likely know but can't be asked.

### Sources Consulted

What was actually searched, so the user can judge coverage:

- **Source control history**: {file paths}, {number of commits reviewed}, PRs #{numbers}, and code comments searched. Or "Not searched. This should not happen because git and `gh` are always expected."
- **Issue / ticket tracker**: {ticket IDs and keyword searches}.
- **Long-form documents**: {page titles and search queries}.
- **Real-time team chat**: {channels searched, date ranges, queries}.
- **Infrastructure observability**: {dashboards, monitors, metrics, logs, traces, or incidents searched}.
- **Error / exception tracking**: {issues, events, or releases searched}.
- **Product analytics warehouse**: {fully-qualified tables queried, time windows, and the numeric summaries (counts, percentiles, first/last-seen timestamps) that bore on the question}.

Any non-git source not searched: "Not searched. No matching MCP available in this environment."

### Confidence Summary

One or two sentences, e.g.:

> "The core rationale (A) is well-supported by direct PR and ticket evidence. The specific threshold value (100) is inferred from the surrounding context but not explicitly documented. The question of whether this was driven by a customer request could not be answered. No relevant issue tracker or long-form doc content surfaced, and real-time team chat search was unavailable."

---

## Quality Check Before Returning

Revise if any fails:

1. Every "What We Found" claim cited, or moved to "Inferred" or "Hypotheses".
2. Phrasing matches tier ("because" for Direct, never Inferred).
3. Every noticed contradiction surfaced, not quietly resolved.
4. "What We Don't Know" names specific gaps; empty is suspicious.
5. Any embedded hypothesis checked, not rubber-stamped.
6. No code cited as evidence of its own intent.
7. Tone calibrated: confident on weak evidence is the failure this skill exists to prevent.

Optimize for honesty, not authority: a reader taking this to the author, a lead, or a PM should know what's known, inferred, and missing.
