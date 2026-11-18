# Linear tickets

The product and business layer ("customer X asked", "the Q3 compliance initiative"): issues, comments, parent and sub-issues, project docs (PRDs, specs), labels, linked PRs.

## Searching (Linear MCP)

1. **Linked tickets first:** IDs in seed commits or PRs (`ENG-1234`) via `get_issue`, then `list_comments`.
2. **Keywords:** `list_issues` with the feature name, a key symbol or the business term; try several phrasings.
3. **Parents:** from a sub-issue fetch its parent; parents often carry the why.
4. **Project docs:** `get_project` and its documents, where specs and rationale usually live.
5. **Labels and milestones** (`customer-request`, `incident-followup`, `compliance`, a deadline) hint at the motivation.

## Pitfalls

- Scope changes on reopen; read the whole history.
- A boilerplate "Why" ("improve user experience") isn't an answer.
- Compare ticket dates with the ship date; follow duplicate-of links to the canonical ticket.
- No access is a gap, never a guess.

## Return

Per ticket: ID and title, the motivation quoted verbatim, labels, parent and project, author, created and closed dates, link.
