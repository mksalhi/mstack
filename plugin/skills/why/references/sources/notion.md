# Notion docs

Long-form why written before the code: PRDs, RFCs, ADRs, design reviews, postmortems, runbooks (which may explain defensive code). A significant feature usually has a doc.

## Searching (Notion MCP)

1. **`notion-search`:** feature name, key symbols, the PR author, error strings or user-visible terms, around the ship date.
2. **`notion-fetch` candidates in full;** rationale hides mid-document.
3. **Backlinks and child pages:** alternatives considered, appendices.
4. **Meetings:** `notion-query-meeting-notes` for "we decided X because Y" near the PR's date.

## Pitfalls

- A spec may describe a plan that changed; cross-check with the PR and flag divergence.
- Prefer the final or most recently updated draft; check dates.
- No access is a gap.

## Return

Per doc: title and URL, authors, last-updated date, the motivation quoted verbatim with its section, and whether it's final or draft.
