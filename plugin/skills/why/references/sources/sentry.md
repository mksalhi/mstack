# Sentry error history

## Searching (Sentry MCP)

1. **Orient** if the org or project is unknown: `find_organizations`, `find_projects`.
2. **`search_issues`** in natural language, built from the exception classes the target handles, its function name, the error strings it checks and its file path.
3. **Narrow:** `search_issue_events` and `get_issue_tag_values` by release, time and environment. Does last-seen match the ship date? Which release fixed it?
4. **`get_sentry_resource`** for a full event: does the stack trace pass through the target?
5. **`find_releases`** around the commit date to match a version to the PR.
6. **Seer** output is a hypothesis; events and stack traces are the evidence.

## Return

Per issue: ID and title, project, first and last seen, event count, affected releases, a stack trace excerpt through the target, the correlation with the ship date, link.
