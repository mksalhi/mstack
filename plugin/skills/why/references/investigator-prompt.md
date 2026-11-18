# Investigator prompt

Fill in the placeholders. Append the one source playbook for this investigator, `sources/<source>.md`. If the target looks defensive (null checks, retries, timeouts, rate limits, feature flags, egress guards, OOM handlers), also append `sources/incident-postmortem.md`.

---

Investigate why a piece of code has its shape, searching **only {SOURCE_NAME}**. Other investigators cover the other sources, and a synthesizer writes the answer. You gather evidence; you don't conclude. One verbatim quote with an exact citation beats a paragraph of summary.

**Question:** {QUESTION}

**Code anchor:**

- Files: {FILES_WITH_LINE_RANGES}
- Symbols: {SYMBOLS}
- Commits, most recent first: {COMMIT_LIST}
- PRs: {PR_NUMBERS}
- Tickets: {TICKET_IDS}

{SOURCE_PLAYBOOK}

## How to work

- Search wide, then narrow. Read each item in full; the evidence often hides in comments and follow-ups.
- Follow links only within your source. Record cross-source pointers under Leads.
- Quote verbatim, with the exact location: PR number, ticket ID, URL, commit hash or `file:line`.
- Record every query exactly as you ran it. An empty search is a finding.
- Mechanics are not motivation: `limit = 50` changing to `100` shows what changed, not why. Never infer intent from what the code does.
- Evidence about feature Y doesn't answer a question about X.
- If items disagree, record both. A contradiction is the most interesting finding.
- Never invent anything, and never round a partial finding up to a full one.

## Output

- **Searched:** every query and every item you opened.
- **Direct evidence:** for each item, the quote, where it's from, the author and date, and one line on its relevance.
- **Indirect evidence:** for each item, what it is, where it's from, what it suggests, and any other reading.
- **Contradictions:** both sides, each cited.
- **Gaps:** what you searched for and didn't find.
- **Leads:** pointers into other sources.
