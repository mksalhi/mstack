Fill in placeholders. Append sources/<source>.md. If target looks defensive (null checks, retries, timeouts, rate limits, feature flags, egress guards, OOM handlers), also append sources/incident-postmortem.md.

Investigate code shape, search only {SOURCE_NAME}. Evidence only; no conclusions. One verbatim quote with exact citation beats summary.

Question: {QUESTION}

Code anchor:
- Files: {FILES_WITH_LINE_RANGES}
- Symbols: {SYMBOLS}
- Commits, most recent first: {COMMIT_LIST}
- PRs: {PR_NUMBERS}
- Tickets: {TICKET_IDS}

{SOURCE_PLAYBOOK}

How to work
- Search wide then narrow.
- Follow links only within source; cross-source pointers under Leads.
- Quote verbatim with exact location (PR/ticket/URL/commit/file:line).
- Record every query exactly (empty searches count).
- Don't infer intent or round up partial findings.

Output
- Searched: queries and items opened.
- Direct: quote, source, author/date, relevance.
- Indirect: what it is, source, what it suggests.
- Contradictions.
- Gaps.
- Leads.
