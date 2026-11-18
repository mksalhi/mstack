# Sentry Error History

## How to search it

Use the Sentry MCP.

1. **Orient** (unknown org or project slug): `find_organizations`, `find_projects`.
2. **Search issues:** `search_issues` in natural language (e.g. "errors in PaymentService timeout", "unhandled exceptions in uploadFile"), built from the exception classes the target handles, its function or class name, error strings it checks, and its file path.
3. **Narrow by release and time:** `search_issue_events` (release, time, environment, trace ID, tags), `get_issue_tag_values` (distribution across versions, users, environments). Check **first/last seen** (does the stop match the target's ship date?), **affected releases** (which saw it, which fixed it), **frequency trajectory** (spike, then resolved?).
4. **Full event:** `get_sentry_resource` (Sentry URL or type+ID). Does the stack trace pass through the target? Do tags and breadcrumbs match the conditions it defends against?
5. **Nearby releases:** `find_releases` around the target's commit date; cross-reference version with the PR merge date.
6. **Seer sparingly:** `analyze_issue_with_seer` output is a hypothesis (inference), not authority. Events and stack traces are the primary evidence.

## What to return

Per relevant issue: ID and title; project and org; first/last seen; event count (and sampling rate if known); affected releases; a verbatim stack trace excerpt showing relevance to the target; first/last-seen correlation with the ship date; link; author comments or resolution notes.
