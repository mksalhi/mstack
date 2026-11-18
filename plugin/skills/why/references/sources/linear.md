# Linear Tickets

## What this source contains

The product/business layer ("customer X asked", "the Q3 compliance initiative"): issues and their motivation, attached project docs (PRDs, specs), parent/sub-issue trees, comments (clarifications, scope changes, rationale), labels (`compliance`, `customer-request`, `perf`), status updates, attachments, linked GitHub PRs.

## How to search it

Use the Linear MCP.

1. **Linked tickets first:** IDs in seed commits or PRs (e.g. `ENG-1234`, `[BUG-567]`) via `get_issue`; read the full issue and comments.
2. **Keyword search:** `list_issues` text search for the feature name, key symbol, or business term; try several phrasings.
3. **Walk the tree:** from a sub-issue fetch its parent; parents often carry the why.
4. **Project docs:** `get_project` and its attached docs, where specs and rationale most often live.
5. **Labels and milestones:** labels hint at the motivation type (customer-request, incident-followup, compliance); milestone deadlines often reveal motivation.

## What good evidence looks like here

- A description stating the business problem: "Customer Acme needs X because of their SOC2 audit".
- A comment recording a decision and its reason.
- An initiative-style parent ("Q3 Enterprise Readiness"), an attached PRD or spec, labels like `customer:acme`, `incident-followup`, `perf-regression`.

## Common pitfalls

- **Scope drift:** tickets closed and reopened with new scope; read the whole history.
- **Boilerplate "Why" sections** ("improve user experience") aren't answers.
- **Stale tickets:** compare dates with the code's ship date.
- **Duplicate chains:** follow duplicate-of links to the canonical ticket.
- **No access:** record a gap, never guess.

## What to return

Per relevant ticket: ID and title; the motivation quoted verbatim (the synthesizer cites exact text); labels, parent, project; author, created and closed dates; link.
