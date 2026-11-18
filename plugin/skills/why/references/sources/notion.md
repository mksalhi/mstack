# Notion Docs

## What this source contains

Long-form why written before the code: PRDs, specs and RFCs, ADRs, design-review notes, team pages, postmortems, runbooks (may explain defensive code), strategy docs. A significant feature usually has a doc.

## How to search it

Use the Notion MCP.

1. **`notion-search` keywords:** feature name, key symbols or class names, author handles (docs often precede the code), error strings or user-visible terms, time-bounded queries around the ship date.
2. **`notion-fetch` candidates:** read full content, not the preview; rationale hides mid-document.
3. **Backlinks and child pages:** alternatives considered, appendices, implementation notes.
4. **Databases:** `notion-query-data-sources` and `notion-query-meeting-notes` surface meetings that discussed the decision.
5. **Author spaces:** the PR author's personal notebook may hold exploratory thinking.

## What good evidence looks like here

- A PRD "Problem statement" or "Motivation" matching the target's purpose; an "Alternatives considered" section.
- A postmortem naming the target as the fix for an incident.
- Meeting notes recording "we decided X because Y" in the PR's author/date range; a non-trivially filled ADR.

## Common pitfalls

- **Outdated specs / drift:** a doc may describe a plan that changed; cross-check against the PR and flag divergence for the synthesizer.
- **Boilerplate "Why" sections:** look for specificity.
- **Unlinked docs:** broad keyword searches find them.
- **Multiple drafts:** prefer the finalized or most recently updated; check dates.
- **No access:** record a gap.

## What to return

Per relevant doc: title and URL; authors and last-updated date; verbatim motivation with page/section location; relevant linked pages; finalized or draft.
